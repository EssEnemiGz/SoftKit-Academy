"""
Track the student activity and navegation.
By: EssEnemiGz
"""

from flask import *
import microservices.common.db_interpreter as interpreter
from datetime import datetime

track_bp = Blueprint('Tracker', __name__)
supabase = None

@track_bp.route("/api/tracker/visited", methods=["PUT"])
def visited():
    if not len(session):
        abort(401)
        
    content_id = request.args.get("content_id")
    if content_id == None:
        abort(400)
        
    date = datetime.now()
    query = supabase.table("activity").insert({"user_id":session.get("id"), "content":content_id, "action":"visited", "date":f"{date.day}/{date.month}/{date.year}", "time":f"{date.hour}:{date.minute}:{date.second}"})
    result = interpreter.no_return(query=query)
    if result.status_code() == 200:
        response = make_response( "DONE" )
        response.status_code = 200
        return response
    
    abort(500)
    
@track_bp.route("/api/tracker/readed", methods=["PUT"])
def readed():
    if not len(session):
        abort(401)
        
    content_id = request.args.get("content_id")
    if content_id == None:
        abort(400)
        
    date = datetime.now()
    query = supabase.table("activity").insert({"user_id":session.get("id"), "content":content_id, "action":"readed", "date":f"{date.day}/{date.month}/{date.year}", "time":f"{date.hour}:{date.minute}:{date.second}"})
    result = interpreter.no_return(query=query)
    if result.status_code() == 200:
        response = make_response( "DONE" )
        response.status_code = 200
        return response
    
    abort(500)