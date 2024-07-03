"""
This microservice work in the login.
By: EssEnemiGz
"""

from flask_cors import CORS
from flask import *
import requests

server_url = None
login_bp = Blueprint('login', __name__)
CORS(login_bp)

@login_bp.route('/login/verify', methods=["POST"])
def login():
    if request.method == "POST":
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        email = data.get('email')

        check = requests.post(server_url+"/existence/check", headers={"Content-Type":"application/json", "Accept":"application/json"}, json={'username':username, 'email':email})
        if check.status_code == 500: 
            err = make_response( jsonify({'status':'ERROR'}) )
            err.status_code = 500
            return err

        check = check.json()
        if not check.get('user') and not check.get('email'):
            err = make_response( redirect('/render/form') )
            err.status_code = 401
            return err

        token = requests.post(server_url+"/auth/log", headers={'Content-Type':'application/json', 'Accept':'application/json'}, json={'username':username, 'password':password, 'email':email}) # To confirm the register creating a token
        if token.status_code == 500:
            response = make_response( redirect('/render/form') )
            return response 
        
        info = token.json()
        if info.get('id') == None: 
            err = make_response( jsonify({'status':'ERROR'}) )
            err.status_code = 500
            return err

        response = make_response( jsonify( {'redirect':'/dashboard'} ) )
        response.status_code = 200
        session['id'] =  info.get('id')
        session['username'] = username
        session.permanent = True
        return response
