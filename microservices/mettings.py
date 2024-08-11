"""
Microservice than is the meetings manager for the SoftKit Academy Database.
By: EssEnemiGz
"""

from flask import *
import microservices.common.db_interpreter as interpreter
import requests

meets_bp = Blueprint('meetings', __name__)
supabase, server_url = None, None

@meets_bp.route("/meet/info", methods=["GET"])
def info():
    query = supabase.table('meetings').select('link, date').eq('user_id', session.get("id")).eq("status", 1)
    result = interpreter.return_data(query=query, was_be_empty=1)
    result = result.output_data()

    response = make_response( jsonify(result) )
    response.status_code = 200
    return response

@meets_bp.route("/meet/add", methods=["POST"])
def add_meet():
    if session.get("id") == None:
        err = redirect("/form?form=login")
        return err
        
    data = request.get_json()
    if None in data.values():
        err = make_response("Falta informacion")
        err.status_code = 500
        return err
    
    resume = data.get("error_concept")
    github = data.get("github_link")
    description = data.get("description")
    query = supabase.table('meetings').insert({'user_id':session.get("id"), 'status':0, 'description':description, 'github':github, 'concept':resume})
    interpreter.no_return(query=query)
    
    response = make_response("Evento en espera de confirmacion")
    response.status_code = 200
    return response

@meets_bp.route("/meet/confirm", methods=["POST"])
def confirm_meet():
    if session.get("id") == None:
        err = redirect("/form?form=login")
        return err
    
    data = request.get_json()
    if None in data.values():
        err = make_response("ERROR")
        err.status_code = 500
        return err
    
    info = {
        "error_concept":data.get("error_concept"),
        "github_link":data.get("github_link"),
        "description":data.get("description"),
        "start":data.get("start"),
        "end":data.get("end")
    }
    
    calendar_request = requests.post(server_url+"/calendar/add/event", headers={"Content-Type":"application/json", "Accept":"application/json"}, json=info)
    if calendar_request.status_code == 200:
        query = supabase.table("meeting").update({"date":data.get("start"), "status":1})
        db = interpreter.no_return(query=query)
        if db.status_code() != 200:
            err = make_response("Error escribiendo la reunion en la base de datos")
            err.status_code = 500
            return err
        
        response = make_response( "Calendar updated" )
        response.status_code == 200
        return response