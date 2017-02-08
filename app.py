#!flask/bin/python
from flask import Flask, render_template, request, jsonify, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_heroku import Heroku
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
db = SQLAlchemy(app)
heroku = Heroku(app)

create table blacklist
    (
        blacklist_user_id number not null,
        blacklist_device_id varchar2(32) not null,
        blacklist_phone varchar2(10) not null,
        blacklist_penalty varchar2(10) not null,
        blacklist_created dateTime not null,
        constraint blklsitpk primary key (blacklist_user_id),
        constraint userfk foreign key (blacklist_user_id) references users
class Blacklist(db.Model):
    __tablename__ = "blacklist"
    blacklist_user_id = db.Column(db.Integer, ForignKey("users.user_id"), primary_key=True)
    

# Create our database model
class User(db.Model):
    __tablename__ = "users"
    user_id = db.Column(db.Integer, Sequence('user_id_seq'), primary_key=True)
    username = db.Column(db.String(8), default='') #enforce with username password must exist
    user_password = db.Column(db.String(16), default='') #enforce with username password must exist
    user_device_id = db.Column(db.String(32), nullable=False)
    user_karma = db.Column(db.Integer, default=0)
    user_photo = db.Column(db.String(32), default='')
    user_phone = db.Column(db.String(10), unique=True, nullable=False)

    def __init__(self, username, password, device_id, karma, photo, phone):
        self.username = username
        self.user_password = password
        self.user_device_id = device_id
        self.user_karma = karma
        self.user_photo = photo
        self.user_phone = phone

    def __r epr__(self):
        return '<user_id %r, user_phone %r>' % self.email, self.user_phone




# Set "homepage" to index.html
@app.route('/')
def index():
    return redirect("http://zechsch.github.io", code=302)
    return render_template('index.html')

# Save e-mail to database and send to success page
#@app.route('/prereg', methods=['POST'])
#def prereg():
#    email = None
#    if request.method == 'POST':
#        email = request.form['email']
#        # Check that email does not already exist (not a great query, but works)
#        if not db.session.query(User).filter(User.email == email).count():
#            reg = User(email)
#            db.session.add(reg)
#            db.session.commit()
#            return render_template('success.html')
#    return render_template('index.html')


tasks = [
    {
        'id':1,
        'task':'this is first task'
    },
    {
        'id':2,
        'task':'this is another task'
    },
    {
        'id':3,
        'task':'task 3'
    }
]

@app.route('/todo/api/v1.0/tasks', methods=['GET'])
def get_tasks():
    return jsonify({'tasks': tasks})

if __name__ == '__main__':
    app.debug = False
    app.run()
