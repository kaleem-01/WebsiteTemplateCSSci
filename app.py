from flask import Flask, request, session
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

# Database model for Website A
class PageView_A(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    visitor_id = db.Column(db.String(10))
    page = db.Column(db.String(255))
    time_spent = db.Column(db.Integer)
    start_time = db.Column(db.DateTime)


# Database model for Website B
class PageView_B(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    visitor_id = db.Column(db.String(10))
    page = db.Column(db.String(255))
    time_spent = db.Column(db.Integer)
    start_time = db.Column(db.DateTime)

# Create all the tables for the databases
with app.app_context():
    db.create_all()

@app.after_request
def track_time(response):
    global start_time
    global previous_path

    # Initiate start time for homepage
    if request.path == '/':
        start_time = datetime.now()
        previous_path = 'HomePage'

    # Adding data for the time spent for website A to database PageView
    if request.path == '/learn_more':
        try:
            time_spent = (datetime.now() - start_time).total_seconds()
            page_view = PageView_A(
                    visitor_id = session.get('visitor_id'),
                    page=previous_path,
                    time_spent=time_spent,
                    start_time=start_time)
            db.session.add(page_view)
            db.session.commit()
        except:
            pass
        finally:
        # Update start_time and previous_path
            start_time = datetime.now()
            previous_path = 'Learn More'

    if request.path == '/confirmation':
        time_spent = (datetime.now() - start_time).total_seconds()
        page_view = PageView_A(
                visitor_id=session.get('visitor_id'),
                page=previous_path,
                time_spent=time_spent,
                start_time=start_time)
        db.session.add(page_view)
        db.session.commit()

        # Delete start_time and previous_path variables
        del start_time, previous_path




    # Adding data for the time spent for website B to database PageView_B
    if request.path == '/website_b':
        # Start Timer for website b
        start_time = datetime.now()
        previous_path = 'HomePage B'

    if request.path == '/learn_more_b':
        try:
            time_spent = (datetime.now() - start_time).total_seconds()
            page_view = PageView_B(
                    visitor_id=session.get('visitor_id'),
                    page=previous_path,
                    time_spent=time_spent,
                    start_time=start_time)
            db.session.add(page_view)
            db.session.commit()
        except:
            pass
        finally:
            # Update global variables
            start_time = datetime.now()
            previous_path = 'Learn More B'

    if request.path == '/confirmation_b':
        time_spent = (datetime.now() - start_time).total_seconds()
        page_view = PageView_B(
                visitor_id=session.get('visitor_id'),
                page=previous_path,
                time_spent=time_spent,
                start_time=start_time)
        db.session.add(page_view)
        db.session.commit()

        del start_time, previous_path

    return response


##################################################################################
from routes import *

if __name__ == '__main__':
    app.run(port=4000, debug = True)
