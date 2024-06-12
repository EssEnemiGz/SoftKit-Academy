"""
Microservicio de renderizacion general
"""

from flask import *
import microservices.common.db_interpreter as interpreter

supabase = None
render_bp = Blueprint('render_bp', __name__)

@render_bp.route('/dashboard/califications', methods=["GET"])
def califications():
    user_id = session.get('id')

    query = supabase.table('califications').select('week, task, point').eq('user_id', user_id)
    result = interpreter.return_data(query=query, was_be_empty=1)

    if result.status_code == 500: return result.flask_response()
    result = result.output_data()
    print(result, user_id)

    return result