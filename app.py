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
Requires user_id to be in users table.
Should be taken care of on install and first open.
Adds post to posts database."""
@app.route('/api/new_post', methods=['POST'])
def new_post():
    post = None
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

        return jsonify({'status': 'OK'})
    except:

        return make_response(jsonify({'status': 'failed',
                        'error': str(sys.exc_info()[0])}), 500)



#get posts
#reply
#rate
"""{
'post': postID,
'vote': ['up'/'down']
}"""
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

        return make_response(jsonify({'status': 'ok'}, 200))
    except:
        return

if __name__ == '__main__':
    app.debug = True
    app.run()
