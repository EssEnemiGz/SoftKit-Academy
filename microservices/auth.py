"""
This microservice auth the user token and send the session to the client.
By: EssEnemiGz
"""

from werkzeug.security import check_password_hash
import microservices.common.db_interpreter as interpreter
from flask_cors import CORS
from flask import * 

supabase = None
auth_bp = Blueprint('auth', __name__)
CORS(auth_bp)

@auth_bp.route("/auth/log", methods=["GET", "POST"])
def token():
    if request.method == "POST":
        data = request.get_json()
        username = data.get('username')
        passw = data.get('password')

        query = supabase.table('users').select('id, password').eq('username', username)
        result = interpreter.return_data(query=query, was_be_empty=0)
        if result.status == 200: result = result.output_data()
        else: return result.flask_response()

        user_id = result[0].get('id')
        password_hashed = result[0].get('password')
        if check_password_hash(password_hashed, passw): # TRUE: The password is correct
            response = make_response( jsonify({'id':user_id, 'username':username}) )
            response.status_code = 200
            return response
        else: 
            err_response = make_response( jsonify( {'status':'ERROR: Incorrect password', 'user':username} ) )
            err_response.status_code = 401
            return err_response # Unauthorized access

