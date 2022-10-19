import datetime
from datetime import timedelta
from flask import Flask, make_response, request, jsonify
from functools import wraps
import jwt
from flask_restful import Api, abort, reqparse, Resource

app = Flask(__name__)
app.config['SECRET_KEY'] = '8989'

parser = reqparse.RequestParser()
parser.add_argument('token', type=str, required=True)

USER_SECRETS = {
    'user1': 'password1',
    'user2': 'password2',
}

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        Token = request.args.get('token')
        token = Token

        if not token:
            return jsonify({'message': 'Token is missing!'}), 403
        
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
        
        except:
            return jsonify({'message': 'Token is missing!'}), 403

        return f(*args, **kwargs )
    
    return decorated

@app.route('/unprotected')
def unprotected():
    return jsonify({'message': 'Anyone can view'})

@app.route('/')
def index():
    return 'Hacking JWT tokens'

@app.route('/protected')
@token_required
def protected():
    return jsonify({'message': 'JWT only'})

@app.route('/login')
def login():
    auth = request.authorization
    if auth and auth.password == '8989':
        token = jwt.encode({"user": auth.username, "exp": datetime.datetime.utcnow()+datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])
        return jsonify({'token': token})
    return make_response("Could not verify", 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})

@app.route('/user_secret')
def user_secret():
    data = parser.parse_args()
    user_id = jwt.decode(data['token'], app.config['SECRET_KEY'], algorithms=['HS256'] )['user']
    print(user_id)
    return jsonify({'user_secret': USER_SECRETS[user_id]})


if __name__ == '__main__':
    app.run(debug=True)