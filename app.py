#!flask/bin/python
from flask import Flask, render_template, request, jsonify, redirect, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_heroku import Heroku
from extensions import *
from authy.api import AuthyApiClient
import os
import sys

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
db = SQLAlchemy(app)
heroku = Heroku(app)
authy_api = AuthyApiClient('268Rr4QalHk9KgYC0BgntMUEXKUsXDtf')

# Set "homepage" to botl-app.com
@app.route('/')
def index():
    return redirect("http://botl-app.com", code=302)

"""
Adds post to posts database."""
@app.route('/api/new_post', methods=['POST'])
def new_post():
    #only allow post method
    if request.method != 'POST':
        return make_response(jsonify({'status': 'failed',
                                      'error': 'Method not allowed'}), 405)
    try:
        data = request.get_json()

        latitude = data['latitude']
        longitude = data['longitude']
        msg = data['message']
        user = data['user_id']

        cmd = "insert into Posts(Latitude, Longitude, Message, UserId) values(%s, %s, %s, %s);"
        db.engine.execute(cmd, (latitude, longitude, msg, user))

        postid = db.engine.execute("select postid from posts where latitude=" + str(latitude) + " and longitude=" + str(longitude) + " and userid=" + str(user) + ";")
        postid = postid.first()['postid']

        return jsonify(status="OK", postid=postid, user=user)
    except:
        return make_response(jsonify({'status': 'failed',
                        'error': str(sys.exc_info()[0])}), 500)

"""
Gets n nearest posts to user. Sorted by post time."""
@app.route('/api/get_posts', methods=['POST'])
def get_posts():
    if request.method != 'POST':
        return make_response(jsonify({'status': 'failed',
                                      'error': 'Method not allowed'}), 405)
    try:
        data = request.get_json()

        dist = data["distance"]
        postNum = data["num_posts"]
        startLat = data["latitude"]
        startLong = data ["longitude"]
        if "sort" in data:
            sort = data["sort"]


            if sort == "time":
                result = db.engine.execute("select * from (select * from (SELECT Message, threadid, PostID, UserID, Ts, Latitude, Rating, Longitude, SQRT(POW(69.1 * " + "(Latitude - " + str(startLat) + "), 2) + POW(69.1 * (" + str(startLong) + " - Longitude) * COS(Latitude / 57.3), 2)) AS distance FROM Posts) as foo where distance < " + str(dist) + " ORDER BY distance fetch first " + str(postNum) + " rows only) as foo1 order by ts desc;")

            elif sort == "distance":
                result = db.engine.execute("select * from (SELECT Message, threadid, PostID, UserID, Ts, Latitude, Rating, Longitude, SQRT(POW(69.1 * " + "(Latitude - " + str(startLat) + "), 2) + POW(69.1 * (" + str(startLong) + " - Longitude) * COS(Latitude / 57.3), 2)) AS distance FROM Posts) as foo where distance < " + str(dist) + " ORDER BY distance fetch first " + str(postNum) + " rows only;")

            elif sort == "rating":
                result = db.engine.execute("select * from (select * from (SELECT Message, threadid, PostID, UserID, Ts, Latitude, Rating, Longitude, SQRT(POW(69.1 * " + "(Latitude - " + str(startLat) + "), 2) + POW(69.1 * (" + str(startLong) + " - Longitude) * COS(Latitude / 57.3), 2)) AS distance FROM Posts) as foo where distance < " + str(dist) + " ORDER BY distance fetch first " + str(postNum) + " rows only) as foo1 order by Rating desc;")
        else:
            result = db.engine.execute("select * from (select * from (SELECT Message, threadid, PostID, UserID, Ts, Latitude, Rating, Longitude, SQRT(POW(69.1 * " + "(Latitude - " + str(startLat) + "), 2) + POW(69.1 * (" + str(startLong) + " - Longitude) * COS(Latitude / 57.3), 2)) AS distance FROM Posts) as foo where distance < " + str(dist) + " ORDER BY distance fetch first " + str(postNum) + " rows only) as foo1 order by ts desc;")

        posts = []
        for row in result:
            post_id = row['postid']
            thread_id = row['threadid']
            user_id = row['userid']
            latitude = row['latitude']
            longitude = row['longitude']
            rating = row['rating']
            msg = row['message']
            posts.append(dict(post_id=post_id, thread_id=thread_id, user_id=user_id, latitude=latitude,
                longitude=longitude, rating=rating, message=msg))

        return jsonify(status='OK', posts=posts)

    except:
        return make_response(jsonify({'status': 'failed',
                        'error': str(sys.exc_info()[0])}), 500)


@app.route('/api/get_thread', methods=['POST'])
def get_thread():
    if request.method != 'POST':
        return make_response(jsonify({'status': 'failed',
                                      'error': 'Method not allowed'}), 405)
    try:
        data = request.get_json()
        post = data['post_id']

        result = db.engine.execute("select * from posts where postid=" + str(post) + ";")
        for row in result:
            thread_id = row['threadid']
            latitude = row['latitude']
            longitude = row['longitude']

        result = db.engine.execute("select Message, rating, UserID from posts" +
            " where threadid=" + str(thread_id) + " order by Ts;")

        thread = []
        for row in result:
            user = row['userid']
            msg = row['message']
            rating = row['rating']
            thread.append(dict(user=user, message=msg, rating=rating))

        return jsonify(status="OK", latitude=latitude, longitude=longitude, thread_id=thread_id, thread=thread)

    except:
        return make_response(jsonify({'status': 'failed',
                        'error': str(sys.exc_info()[0])}), 500)

@app.route('/api/reply', methods=['POST'])
def reply():
    if request.method != 'POST':
        return make_response(jsonify({'status': 'failed',
                                      'error': 'Method not allowed'}), 405)
    try:
        data = request.get_json()

        op = data['thread']
        msg = data['message']
        user = data['user_id']

        thread = db.engine.execute("select threadid from posts where postid=" + str(op) + ";")
        thread = thread.first()['threadid']

        cmd = "insert into posts(Latitude, Longitude, Message, ThreadId, userid) values(-1000, -1000, %s, %s, %s);"
        db.engine.execute(cmd, (msg, thread, user))

        cmd = "select postid from posts where threadid=%s and message=%s and userid=%s;"
        postid = db.engine.execute(cmd, (thread, msg, user))
        postid = postid.first()['postid']

        return jsonify(status="OK", postid=postid)

    except:
        return make_response(jsonify({'status': 'failed',
                        'error': str(sys.exc_info()[0])}), 500)


@app.route('/api/rate_post', methods=['POST'])
def rate_post():

    if request.method != 'POST':
        print(request.method)
        return make_response(jsonify({'status': 'failed',
                                      'error': 'Method not allowed'}), 405)
    try:
        data = request.get_json()
        post_id = data['post']
        vote = data['vote']

        result = db.engine.execute("select rating from Posts where PostID=" + str(post_id) + ";")

        for row in result:
            rating = row[0]
        if vote == 'up':
            rating += 1
        else:
            rating -= 1

        db.engine.execute("update Posts set rating=" + str(rating) + " where PostID=" + str(post_id) + ";")

        return jsonify(status="OK")
    except:
        return jsonify({'status': 'failed',
                        'error': str(sys.exc_info()[0])})

@app.route('/api/verify', methods=['POST'])
def verification():
    if request.method != 'POST':
        return make_response(jsonify({'status': 'failed',
                                      'error': 'Method not allowed'}), 405)
    try:
        data = request.get_json()
        errors = []
        phone = data['phone']
        username = data['username']
        device = data['device']

        results = db.engine.execute("select username from users;")
        for row in results:
            if username.lower() == row['username'].lower():
                errors.append({"message":'This username is taken'})
                break
        results = db.engine.execute('select user_device_id from users;')
        for row in results:
            if device.lower() == row['user_device_id'].lower():
                errors.append({"message":'An account is already associated with this device'})
                break
        # ---------------------------

        if len(errors) != 0:
            return jsonify(errors=errors), 422

        authy_api.phones.verification_start(phone_number=phone, country_code='1', via='sms')
        return jsonify(status="OK")
    except:
        return make_response(jsonify({'status': 'failed',
                        'error': str(sys.exc_info()[0])}), 500)


@app.route('/api/login', methods=['POST'])
def login():

        errors = []

        data = request.get_json()

        username = data['username']
        password = data['password']

        # check if username exists
        valid_username = db.engine.execute('select username from users where username=\'' + username +'\';')
        if valid_username.rowcount == 0:
            er = {"message":"Username does not exist"}
            err=[er]
            status = 404
            return jsonify(errors=err), status
        valid_username = valid_username.first()['username']

        # ---------------
        # check if password is valid (if username exists...)
        # fetch password
        passHash = db.engine.execute('select user_password from users where username=\'' + username + '\';')
        # get the previous salt
        passHash = passHash.first()['user_password']
        salt = passHash.split("$")[1]
        # this is the user's attempt at password
        attempt = encrypt_password(password, salt)
        # check if password matches...
        if passHash != attempt:
            errors.append({"message":'Password is incorrect for the specified username'})

        # If there are errors, redirect to login, with errors
        if len(errors) != 0:
            return jsonify(errors=errors), 422

        # otherwise, log user in and redirect to main page

        return jsonify(username=username,status='OK')

@app.route('/api/register', methods=['POST'])
def register():
    errors = []
    data = request.get_json()
    username = data['username']
    password = data['password']
    device = data['device']
    phone = data['phone']
    verification = data['code']

    # Check for unique username
    cmd = "select %s from users;"

    results = db.engine.execute("select username from users;")
    for row in results:
        if username.lower() == row['username'].lower():
            errors.append({"message":'This username is taken'})
            break

    results = db.engine.execute('select user_device_id from users;')
    for row in results:
        if device.lower() == row['user_device_id'].lower():
            errors.append({"message":'An account is already associated with this device'})
            break

    verification = authy_api.phones.verification_check(phone_number=phone, country_code='1', verification_code=verification)
    if not verification.content['success']:
        errors.append({"message":'verification code not correct.'})
    # ---------------------------

    if len(errors) != 0:
        return jsonify(errors=errors), 422

    # if no errors - create new entry in User table and redirect to /login page
    #encrypt password
    password = encrypt_password(password)
    cmd = "insert into users(username, user_password, user_phone, user_device_id) values(%s, %s, %s, %s);"
    db.engine.execute(cmd, (username, password, phone, device))
    return jsonify(username=username, status="OK")
    # ------------------------------

@app.route('/api/edit_post', methods=['POST'])
def edit():
    if request.method != 'POST':
        return make_response(jsonify({'status': 'failed',
                                      'error': 'Method not allowed'}), 405)


    try:
        data = request.get_json()
        post = data['post_id']
        msg = data['message']
    except KeyError:
        db.engine.execute('delete from posts where postid=' + str(post) + ";")
        return jsonify(status="OK")

    cmd = "update posts set message=%s where postid= %s;"
    db.engine.execute(cmd, (msg, post))
    return jsonify(status="OK")

@app.route('/api/remove_user', methods=['POST'])
def remove_user():
    if request.method != 'POST':
        return make_response(jsonify({'status': 'failed',
                                      'error': 'Method not allowed'}), 405)
    try:
        data = request.get_json()
        username = data['username']

        db.engine.execute('delete from users where username=\'' + username + '\';')
        return jsonify(status='OK')
    except:
        return make_response(jsonify({'status': 'failed',
                        'error': str(sys.exc_info()[0])}), 500)


if __name__ == '__main__':
    app.debug = True
    app.run()
