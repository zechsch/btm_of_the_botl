from __future__ import print_function
from flask import *
import hashlib
from werkzeug.utils import secure_filename
import os
import sys

api_home = Blueprint('api_home', __name__)

@api_home.route('/home/', methods=['POST'])
def home_api():
    data = request.get_json()
    print(data)

    print(3)
