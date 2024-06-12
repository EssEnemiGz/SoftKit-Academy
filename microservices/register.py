"""
This microservice create a query to register the user.
By: EssEnemiGz
"""
from flask_cors import CORS
import microservices.common.db_interpreter as interpreter
from flask import *
import requests

supabase, server_url = None, None
register_bp = Blueprint('register', __name__)
CORS(register_bp)

@register_bp.route("/register/verify", methods=["POST"])
def register():
    if request.method == "POST":
        data = request.get_json()
        if None in data: 
            err = make_response( jsonify({'status':'ERROR'}) )
            err.status_code = 500
            return err
        
        if 'code' not in data:
            reject = make_response( "No intentes acceder sin el codigo :)" )
            reject.status_code = 401
            return reject
        
        if data.get('code') != 'justaeasypassword':
            reject = make_response( "Codigo incorrecto" )
            reject.status_code = 401
            return reject
    
        username = data.get('username')
        password = data.get('password')
        email = data.get('email')

        check = requests.post(server_url+"/existence/check", headers={'Content-Type':'application/json', 'Accept':'application/json'}, json={'username':username, 'email':email})
        if check.status_code == 500:
            err = make_response( jsonify({'status':'ERROR'}) )
            err.status_code = 500
            return err
        
        check = check.json()

        if check.get('user') and check.get('email'): # USER EXIST
            response = make_response( redirect("/render/form") )
            response.status_code = 409
            return response
        
        serverResponse = requests.post(server_url+"/hash/create", headers={'Content-Type':'application/json', 'Accept':'application/json'}, json={'action':'hash-passw', 'password':password})
        if serverResponse.status_code == 500:
            response = make_response( redirect('/render/form') )
            response.status_code = 500
            return response
        
        password_hashed = serverResponse.json()['hash-passw']
        query = supabase.table('users').insert({'username':username, 'password':password_hashed, 'email':email})
        interpreter.no_return(query=query) 
        
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
        session.permanent = True
        return response