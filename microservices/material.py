"""
Students material managaer.
By: EssEnemiGz
"""

import microservices.common.db_interpreter as db_interpreter
from flask import *
import json

material_bp = Blueprint(__name__, 'material')
db = None

@material_bp.route("/api/add/material")
def add_material():
    if not len(session):
        abort(401)
        
    if session.get("role") not in ["admin", "teacher"]:
        abort(401)
        
    course = request.form.get("course")
    duration = request.form.get("duration")
    description = request.form.get("description")
    id_language = request.form.get("id_language")
    id_teacher = request.form.get("id_teacher")
    course_url = request.form.get("course_url")
    tags = request.form.get("tags")
    pricing = request.form.get("pricing")
    
    if None in [course, duration, description, id_language, id_teacher, course_url, pricing, tags]:
        abort(400)
        
    # Formateo correcto de la información
    try:
        duration = int(duration)
        id_language = int(id_language)
        id_teacher = int(id_teacher)
    except ValueError:
        abort(400)
        
    try:
        pricing = json.loads(pricing)
        if tags != "": tags = json.loads(tags)
    except json.decoder.JSONDecodeError:
        abort(400)
        
    query = db.insert(
        {
            "course":course, 
            "minutes":duration,
            "published":None,
            "description":description,
            "id_language":id_language,
            "id_teacher":id_teacher,
            "url":course_url,
            "tags":tags,
            "pricing":pricing
        }
    )
    result = db_interpreter.no_return(query=query)
    response = make_response("DONE!")
    response.status_code = result.status_code()
    return response