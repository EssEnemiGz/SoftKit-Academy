"""
This microservice create a password with a hash
By: EssEnemiGz
"""

from werkzeug.security import generate_password_hash
from flask_cors import CORS
from flask import *

hash_bp = Blueprint('hash', __name__)
CORS(hash_bp)

@hash_bp.route('/hash/create', methods=["POST"])
def generate():
    head = request.headers
    data = request.get_json()

    # The program use this conditional to reject incorrect request
    if data.get('action') == 'hash-passw' and head.get('Content-Type') and 'application/json' in head.get('Content-Type') : 
        passw = data.get('password') 
        password_hashed = generate_password_hash(passw)
            
        # If I not use responses the server return a error
        response = make_response( jsonify( {'hash-passw':password_hashed} ) )
        response.headers['Content-Type'] = 'application/json'
        response.status_code = 200
        return response

