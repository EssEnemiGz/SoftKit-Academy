"""
Microservicio de renderizacion general
"""

from flask import *
import microservices.common.db_interpreter as interpreter
import os

supabase = None
render_bp = Blueprint('render_bp', __name__)

@render_bp.route('/api/dashboard/califications', methods=["GET"])
def califications():
    user_id = session.get('id')
    username = session.get('username')

    query = supabase.table('califications').select('week, task, point').eq('user_id', user_id)
    result = interpreter.return_data(query=query, was_be_empty=1)

    if result.status_code == 500: return result.flask_response()
    result = result.output_data()
    result.insert(0, username)

    return result

@render_bp.route('/api/render/students', methods=["GET"])
def students():
    query = supabase.table('users').select('id, username').eq('role', 'student')
    db_response = interpreter.return_data(query=query, was_be_empty=1)

    if db_response.status_code == 500: return db_response.flask_response()
    final = db_response.output_data()
    return final

@render_bp.route('/api/render/languages', methods=["GEt"])
def languages():
    pass

@render_bp.route("/api/render/courses", methods=["GET"])
def courses():
    query = supabase.table("")
    pass

@render_bp.route("/api/render/components", methods=["GET"])
def components():
    component = request.args.get("component")
    
    if component == None:
        abort(400)
        
    if component not in os.listdir("templates/components"):
        abort(404)
        
    return send_from_directory("templates/components", component)