"""
This microservice check if the info exist.
By: EssEnemiGz
"""

from flask_cors import CORS
import microservices.common.db_interpreter as interpreter
from flask import *
import requests

supabase, server_url = None, None
existence_bp = Blueprint('existence', __name__)
CORS(existence_bp)

@existence_bp.route('/api/existence/check', methods=["POST"])
def check(): 
    if request.method == "POST":
        dic = {}
        data = request.get_json()
        username = data.get('username')
        password = data.get("password")
        email = data.get("email")
        operation = data.get("operation")
        
        if None in [username, password, email]:
            err = make_response()
            err.status_code = 500
            return err
        
        # USER EXISTENCE
        if username != None:
            user_existence = 1
            query = supabase.table('users').select('id, username, email, subscription, role').eq('username', username)
            result = interpreter.return_data(query=query, was_be_empty=1)

            if result.output_data() == []:
                user_existence = 0
                
            if user_existence == 0:
                dic.setdefault("status", user_existence)
                response = make_response( jsonify(dic) )
                response.status_code = 200
                return response
            
            result = result.output_data()[0]
            if email != result.get("email"): 
                err = make_response( "Auth error" )
                err.status_code = 401
                return err
            
            dic.update(result)
            dic.setdefault("status", user_existence)
            
        if operation == None:
            token = requests.post(server_url+"/api/auth/log", headers={'Content-Type':'application/json', 'Accept':'application/json'}, json={'username':username, 'password':password}) # To confirm the register creating a token
            if token.status_code == 401:
                response = make_response( "Auth error" )
                response.status_code = 401
                return response 
        
        response = make_response( jsonify(dic) )
        response.status_code = 200
        return response

