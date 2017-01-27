from flask import Flask, render_template, session
import api
from flask import session

# Initialize Flask app with the template folder address
app = Flask(__name__)
app.secret_key = 'N5\\A\xa7!\x80\xa0j\xd1\xdf\x19\xc8n\n\x1e)(\xb1Z\x7f?\x07A'
print api
app.register_blueprint(api.api_home, url_prefix="")

# Listen on external IPs
# For us, listen to port 3000 so you can just run 'python app.py' to start the server
if __name__ == '__main__':
    # listen on external IPs
    app.run(host='0.0.0.0', port=5555, debug=True)
