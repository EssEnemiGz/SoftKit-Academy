"""
This microservice create a query to register the user.
By: EssEnemiGz
"""
from flask_cors import CORS
import microservices.common.db_interpreter as interpreter
from flask import *
import requests

supabase, server_url, server_code = None, None, None
register_bp = Blueprint('register', __name__)
CORS(register_bp, supports_credentials=True)

@register_bp.route("/api/register/verify", methods=["POST"])
def register():
    if request.method == "POST":
        data = request.get_json()
        if None in data.values(): 
            err = make_response( jsonify({'status':'ERROR'}) )
            err.status_code = 500
            return err
    
        username = data.get('username')
        password = data.get('password')
        email = data.get('email')

        check = requests.post(server_url+"/api/existence/check", headers={'Content-Type':'application/json', 'Accept':'application/json'}, json={'username':username, "password":password, 'email':email, 'operation':'register'})
        if check.status_code == 500:
            err = make_response( "Error Registering Your User" )
            err.status_code = 500
            return err
        
        info = check.json()
        if info.get("status") == 1:
            err = make_response("User Already Exists")
            err.status_code = 500
            return err
        
        serverResponse = requests.post(server_url+"/api/hash/create", headers={'Content-Type':'application/json', 'Accept':'application/json'}, json={'action':'hash-passw', 'password':password})
        if serverResponse.status_code == 500:
            response = make_response( redirect('/render/form') )
            response.status_code = 500
            return response
        
        password_hashed = serverResponse.json()['hash-passw']
        query = supabase.table('users').insert({'username':username, 'password':password_hashed, 'email':email, "subscription":"free"})
        interpreter.no_return(query=query)
        
        check = requests.post(server_url+"/api/existence/check", headers={'Content-Type':'application/json', 'Accept':'application/json'}, json={'username':username, "password":password, 'email':email})
        if check.status_code == 500:
            err = make_response( "Error Registering Your User" )
            err.status_code = 500
            return err
        
        info = check.json() 
        response = make_response( jsonify( {'redirect':'/students/panel'} ) )
        response.status_code = 200
        session['id'] =  info.get('id')
        session['username'] = username
        session['subscription'] = "free"
        session['role'] = "student"
        session.permanent = True
        return response