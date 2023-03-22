from flask import Flask, request, session, render_template, redirect
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session

# Configure app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'

# Configure flask session
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database and database models
db = SQLAlchemy(app)


# Database model for Time Spent
class PageView(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    visitor_id = db.Column(db.String(10))
    page = db.Column(db.String(255))
    time_spent = db.Column(db.Integer)
    start_time = db.Column(db.DateTime)

# Database table for the binary variable
class Button(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    visitor_id = db.Column(db.String(10))
    button = db.Column(db.Boolean)


# Create all the tables for the databases
with app.app_context():
    db.create_all()


# Function to log data
def log_data():
    time_spent = (datetime.now() - start_time).total_seconds()
    page_view = PageView(
                    visitor_id = session.get('visitor_id'),
                    page=previous_path,
                    time_spent=time_spent,
                    start_time=start_time)
    db.session.add(page_view)
    db.session.commit()


@app.after_request
def track_time(response):
    global start_time
    global previous_path

    # Initiate start time for homepage
    if request.path == '/':
        try:
            log_data()
        except:
            pass
        finally:
            start_time = datetime.now()
            previous_path = 'HomePage'


    # Adding data for the time spent for website A to database PageView
    if request.path == '/learn_more':
        try:
            log_data()
        except:
            pass
        finally:
        # Update start_time and previous_path
            start_time = datetime.now()
            previous_path = 'Learn More'

    if request.path == '/confirmation':
        try:
            log_data()
        except:
            pass
        # Delete start_time and previous_path variables
        finally:
            del start_time, previous_path

    return response


# @app.after_request
# def remove_variables():
#     global start_time
#     if request.path == '/confirmation':
#         del start_time
    
    

##################################################################################
#
# Routes
#

@app.route('/')
def index():
    # Getting the unique id from the webpage url
    visitor_id = request.args.get('uid')
    if visitor_id:
        # Add ID to session.
        session["visitor_id"] = visitor_id
    session["start_time"] = datetime.now()
    session['previous_path'] = "/"
    return render_template("index.html")

@app.route('/learn_more')
def learn_more():
    session["previous_path"] = "/learn_more"
    session["start_time"] = datetime.now()
    return render_template('learn_more.html')


@app.route('/confirmation')
def confirmation():
    visitor_id = session.get("visitor_id")
    session["previous_path"] = "/confirmation"
    session["start_time"] = datetime.now()
    return render_template('done.html', visitor_id = visitor_id)

@app.route("/log_binary")
def button_tracking():
    global previous_path
    button_click = Button(
                    visitor_id = session.get('visitor_id'),
                    button = True)
    db.session.add(button_click)
    db.session.commit()
    
    return redirect('/')

if __name__ == '__main__':
    app.run(port=3000, debug = True)
