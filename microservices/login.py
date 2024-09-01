"""
This microservice work in the login.
By: EssEnemiGz
"""

import microservices.common.db_interpreter as interpreter
from flask_cors import CORS
from flask import *
import requests

server_url, supabase = None, None
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
        
        check = requests.post(server_url+"/api/existence/check", headers={"Content-Type":"application/json", "Accept":"application/json"}, json={'username':username, 'email':email})
        if check.status_code == 500: 
            err = make_response( jsonify({'status':'ERROR'}) )
            err.status_code = 500
            return err
        
        check = check.json()
        print(username, password, email)
        if not check.get('user') and not check.get('email'):
            print(check.get("user", check.get("email")))
            err = make_response( redirect('/render/form') )
            err.status_code = 401
            return err

        token = requests.post(server_url+"/api/auth/log", headers={'Content-Type':'application/json', 'Accept':'application/json'}, json={'username':username, 'password':password, 'email':email}) # To confirm the register creating a token
        if token.status_code == 500:
            response = make_response( redirect('/render/form') )
            return response 
        
        info = token.json()
        if info.get('id') == None: 
            err = make_response( jsonify({'status':'Error setting your password in the database'}) )
            err.status_code = 500
            return err
        
        query = supabase.table("users").select("subscription, role").eq("id", info.get("id"))
        result = interpreter.return_data(query=query, was_be_empty=1)
        
        if not len(result.output_data()):
            err = make_response( "Error getting user info!" )
            err.status_code = 500
            return err
        
        response = make_response( jsonify( {'redirect':'/students/panel'} ) )
        response.status_code = 200
        session['id'] =  info.get('id')
        session['username'] = username
        session['subscription'] = result.output_data()[0].get('subscription')
        session['role'] = result.output_data()[0].get('role')
        session.permanent = True
        return response
