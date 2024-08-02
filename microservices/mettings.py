"""
Microservice than is the meetings manager.
By: EssEnemiGz
"""

from flask import *
import microservices.common.db_interpreter as interpreter

meet_bp = Blueprint('meetings', __name__)
supabase = None

@meet_bp.route("/meet/info", methods=["GET"])
def info():
    query = supabase.table('meetings').select('link, date, hour').eq('user_id', session.get("id"))
    result = interpreter.return_data(query=query, was_be_empty=1)
    result = result.output_data()
    print(result)

    response = make_response( jsonify(result) )
    response.status_code = 200
    return response

@meet_bp.route("/meet/add", methods=["POST"])
def add_meet():
    if session.get("id") == None:
        err = redirect("/form?form=login")
        return err
        
    query = supabase.table('meetings').insert({'user_id':session.get("id"), 'link':''})
    pass