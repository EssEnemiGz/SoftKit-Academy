"""
This microservice check if the info exist.
By: EssEnemiGz
"""

from flask_cors import CORS
import microservices.common.db_interpreter as interpreter
from flask import *

supabase = None
existence_bp = Blueprint('existence', __name__)
CORS(existence_bp)

@existence_bp.route('/existence/check', methods=["POST"])
def check(): 
    global db, cursor
    if request.method == "POST":
        dic = {}
        data = request.get_json()
        username = data.get('username')
        
        # USER EXISTENCE
        if username != None:
            user_existence = 1
            query = supabase.table('users').select('username, email').eq('username', username)
            result = interpreter.return_data(query=query, was_be_empty=1)

            if result.output_data() == []:
                user_existence = 0

            if user_existence:
                dic.setdefault('user', True)
                dic.setdefault('email', True)
            else: 
                dic.setdefault('user', False)
                dic.setdefault('email', False)

        response = make_response( jsonify(dic) )
        response.status_code = 200
        return response

