"""
Microservicio encargado de las operaciones de bases de datos que yo necesite.
Disponible solo para administradores.
By: EssEnemiGz
"""

from flask import *
import microservices.common.db_interpreter as interpreter

supabase = None
insert_bp = Blueprint('insert_bp', __name__)

@insert_bp.route("/insert/califications", methods=["POST"])
def califications_insert():
    info = request.get_json()

    if 'server_code' not in info:
        err = make_response("Falta el codigo del servidor")
        err.status_code = 401
        return err
    
    if info.get('server_code') != 'justaeasypassword':
        err = make_response("Codigo incorrecto")
        err.status_code = 401
        return err
    
    user_id = info.get('user_id')
    califications = info.get('califications')
    week = info.get('week')

    for cont, element in enumerate(califications, 1):
        query = supabase.table('califications').insert({'user_id':user_id, 'week':week, 'task':f'Tarea {cont}', 'point':element})
        interpreter.no_return(query=query)
    
    response = make_response()
    response.status_code = 200
    return response
