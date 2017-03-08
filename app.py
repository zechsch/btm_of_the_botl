#!flask/bin/python
from flask import Flask, render_template, request, jsonify, redirect, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_heroku import Heroku
import os
import sys

app = Flask(__name__)
if os.environ.get('DATABASE_URL') is None:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/Zack'
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
db = SQLAlchemy(app)
heroku = Heroku(app)

# Set "homepage" to index.html
@app.route('/')
def index():
    return redirect("http://botl-app.com", code=302)

"""
Adds post to posts database."""
@app.route('/api/new_post', methods=['POST'])
def new_post():
    if request.method != 'POST':
        return make_response(jsonify({'status': 'failed',
                                      'error': 'Method not allowed'}), 405)
    try:
        data = request.get_json()

        latitude = data['latitude']
        longitude = data['longitude']
        msg = data['message']
        user = data['user_id']



        db.engine.execute("insert into Posts(Latitude, Longitude, Message, UserId) values(" +
            str(latitude) + ", " + str(longitude) + ", \'" + msg + "\', " + str(user) + ");")

        return jsonify(status="OK")
    except:
        return make_response(jsonify({'status': 'failed',
                        'error': str(sys.exc_info()[0])}), 500)


@app.route('/api/get_posts', methods=['POST'])
def get_posts():
    if request.method != 'POST':
        return make_response(jsonify({'status': 'failed',
                                      'error': 'Method not allowed'}), 405)
    try:
        data = request.get_json()
        dist = data["dist"]
        postNum = data["numOfPosts"]
        startLat = data["Lat"]
        startLong = data ["Long"]


        postList = db.engine.execute("""SELECT Message, PostID, UserID, Latitude, Longitude, SQRT(
    POW(69.1 * (Latitude - """ + startLat + """), 2) +
    POW(69.1 * (""" + startLong + """ - Longitude) * COS(Latitude / 57.3), 2)) AS distance
    FROM Posts distance < """ + dist + """ ORDER BY distance fetch first """ + postNum + """;""")

        return jsonify(postList)

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
        result = db.engine.execute("select Message, UserID from posts" +
            " where threadid=" + str(thread_id) + " order by Ts;")
        thread = []
        for row in result:
            user = row['userid']
            msg = row['message']
            thread.append(dict(user=user, message=str(msg)))

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

        thread = data['thread']
        msg = data['message']
        user = data['user_id']


        db.engine.execute("insert into Posts(Latitude, Longitude, Message, ThreadId, UserId)" +
            "values(-1, -1, \'" + msg + "\', " + str(thread) + ", " + str(user) + ");")

        return jsonify(status="OK")

    except:
        return make_response(jsonify({'status': 'failed',
                        'error': str(sys.exc_info()[0])}), 500)


@app.route('/api/rate_post', methods=['POST'])
def reate_post():

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
        return make_response(jsonify({'status': 'failed',
                        'error': str(sys.exc_info()[0])}), 500)

if __name__ == '__main__':
    app.debug = True
    app.run()
