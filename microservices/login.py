"""
This microservice work in the login.
By: EssEnemiGz
"""

import microservices.common.db_interpreter as interpreter
import microservices.common.user_security as mail
from threading import Thread
from flask_cors import CORS
from flask import *
import requests

server_url, supabase, secret_key = None, None, None
login_bp = Blueprint('login', __name__)
CORS(login_bp, supports_credentials=True)

@login_bp.route('/api/login/verify', methods=["POST"])
def login():
    if request.method == "POST":
        data = request.get_json()
        if None in data.values(): 
            err = make_response( jsonify({'status':'ERROR'}) )
            err.status_code = 500
            return err
        
        username = data.get('username')
        password = data.get('password')
        email = data.get('email')
        
        check = requests.post(server_url+"/api/existence/check", headers={"Content-Type":"application/json", "Accept":"application/json"}, json={'username':username, "password":password, 'email':email})
        if check.status_code == 500: 
            err = make_response( jsonify({'status':'ERROR'}) )
            err.status_code = 500
            return err
        
        info = check.json()
        if info.get('id') == None: 
            err = make_response( jsonify({'status':'Error setting your password in the database'}) )
            err.status_code = 500
            return err
        
        first_func = lambda: mail.logged_warning(secret_key=secret_key, email=email)
        executer = lambda: mail.infinite_retry(first_func, 200)
        Thread(target=executer).start()
        
        response = make_response( jsonify( {'redirect':'/students/panel'} ) )
        response.status_code = 200
        session['id'] =  info.get('id')
        session['username'] = username
        session['subscription'] = info.get('subscription')
        session['role'] = info.get('role')
        session.permanent = True
        return response
