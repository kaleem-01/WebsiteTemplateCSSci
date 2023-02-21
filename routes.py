#
# Routes
#

from app import app
from flask import session, render_template, request
# import random

# Function to create a unique ID for each visitor
# def add_visitor():
#     visitor_id = session.get("visitor_id")
#     if visitor_id is None:
#         visitor_id = str(random.randint(1000000000, 9999999999))
#         session["visitor_id"] = visitor_id
#     return visitor_id

@app.route('/')
def index():
    visitor_id = request.args.get('uid')
    if visitor_id:
        session["visitor_id"] = visitor_id
    return render_template('index.html')


@app.route('/learn_more')
def learn_more():
    return render_template('learn_more.html')


@app.route('/confirmation')
def confirmation():
    visitor_id = session.get("visitor_id")
    return render_template('done.html', visitor_id = visitor_id)

@app.route('/website_b')
def website_b():
    visitor_id = request.args.get('uid')
    if visitor_id:
        session["visitor_id"] = visitor_id
    return render_template('website_b.html')

@app.route('/learn_more_b')
def learn_more_b():
    return render_template('learn_more_b.html')

@app.route('/confirmation_b')
def confirmation_b():
    visitor_id = session.get("visitor_id")
    return render_template('done_b.html', visitor_id = visitor_id)

