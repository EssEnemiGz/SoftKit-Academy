"""
This microservice work in the login.
By: EssEnemiGz
"""

import microservices.common.user_security as mail
from threading import Thread
from flask_cors import CORS
from flask import *
import requests

server_url, secret_key = None, None
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
        
        if check.status_code == 401:
            err = make_response("Unauthorized")
            err.status_code = 401
            return err
        
        info = check.json()
        if info.get('id') == None: 
            err = make_response( jsonify({'status':'Error setting your password in the database'}) )
            err.status_code = 500
            return err
        
    
        user_ip = "Desconocida"
        if 'X-Forwarded-For' in request.headers:
            user_ip = request.headers['X-Forwarded-For'].split(',')[0]
        
        if 'X-Real-IP' in request.headers:
            user_ip = request.headers.get('X-Real-IP')
            
        print(request.headers.get('X-Real-IP'), request.headers['X-Forwarded-For'].split(',')[0])
            
        user_agent_string = request.headers.get('User-Agent')
        def first_func(): 
            r = mail.logged_warning(secret_key=secret_key, email=info.get("email"), remote_addr=user_ip, user_agent=user_agent_string)
            return r
        
        def executer(first_func, expected):
            mail.infinite_retry(first_func, expected)
            
        Thread(target=executer, args=(first_func, 200)).start()
        
        response = make_response( jsonify( {'redirect':'/students/panel'} ) )
        response.status_code = 200
        session['id'] =  info.get('id')
        session['username'] = username
        session['subscription'] = info.get('subscription')
        session['role'] = info.get('role')
        session.permanent = True
        return response
