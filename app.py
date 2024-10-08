# MICROSERVICES
import microservices.auth as auth
import microservices.existence as exist
import microservices.hash as hash
import microservices.login as login
import microservices.register as register
import microservices.render as render
import microservices.insert as insert
import microservices.mettings as meetings
import microservices.calendar as calendar
import microservices.tracker as tracker
import microservices.material as material

# LIBRARYS
import microservices.common.render_components as components
from datetime import timedelta
from flask import *
from dotenv import load_dotenv
import supabase
import requests
import os

# Carga de variables de entorno del .env
load_dotenv()
api = os.getenv("SUPABASE_KEY")
database = os.getenv("SUPABASE_URL")
secret_key = os.getenv("SECRET_KEY")
admin_email = os.getenv("EMAIL")
admin_passw = os.getenv("PASSW")
server_url = os.getenv("SERVER")
server_code = os.getenv('SERVER_CODE')

# Configuracion de la aplicacion web
app = Flask(__name__)
app.secret_key = secret_key
app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = "Lax"
app.config['SESSION_COOKIE_DOMAIN'] = ".softkitacademy.com"
app.permanent_session_lifetime = timedelta(weeks=52) # Sesion con duracion de 52 semanas o 1 año
app.url_map.strict_slashes = False

ACCESS_LEVELS = {"free":0, "basic":1, "standard":2, "premium":3}
SUPPORTED_LANGUAGES = ['es', 'en']

# Conexion a base de datos
db = supabase.create_client(database, api)
auth_key = db.auth.sign_in_with_password( {'email':admin_email, 'password':admin_passw} )
if auth_key.session:
    token = auth_key.session.access_token
    pass
else:
    print(f"Error de auth. {auth_key.error}")

# BLUEPRINTS
auth.supabase, exist.supabase, register.supabase, render.supabase, insert.supabase, meetings.supabase, tracker.supabase, material.db = db, db, db, db, db, db, db, db
login.server_url, register.server_url, meetings.server_url, render.server_url, exist.server_url = server_url, server_url, server_url, server_url, server_url
insert.server_code, register.server_code = server_code, server_code
render.secret_key, login.secret_key = secret_key, secret_key
render.ACCESS_LEVELS = ACCESS_LEVELS

app.register_blueprint(auth.auth_bp)
app.register_blueprint(exist.existence_bp)
app.register_blueprint(hash.hash_bp)
app.register_blueprint(login.login_bp)
app.register_blueprint(register.register_bp)
app.register_blueprint(render.render_bp)
app.register_blueprint(insert.insert_bp)
app.register_blueprint(meetings.meets_bp)
app.register_blueprint(calendar.calendar_bp)
app.register_blueprint(tracker.track_bp)
app.register_blueprint(material.material_bp)

@app.route("/", methods=["GET"])
def index():
    return render_template(f"es/index.html")

@app.route("/<lang>", methods=["GET"])
def main(lang):
    if lang not in SUPPORTED_LANGUAGES and lang != "":
        abort(404)
    elif lang == "":
        return render_template(f"es/index.html")
    else:
        return render_template(f"{lang}/index.html")

@app.route("/dashboard", methods=["GET"])
def dashboard():
    if len(session):
        return render_template("es/dashboard.html")
    else:
        return redirect( '/form?form=login' )
    
@app.route("/form", methods=["GET"])
def form():
    return render_template("es/form.html")

@app.route("/form/<lang>", methods=["GET"])
def form_with_lang(lang):
    if lang not in SUPPORTED_LANGUAGES and lang != "":
        abort(404)
    elif lang == "":
        return render_template("es/form.html")
    else: 
        return render_template(f"{lang}/form.html")
    
@app.route("/register", methods=["GET"])
def register():
    return render_template("es/register.html")

@app.route("/register/<lang>", methods=["GET"])
def register_with_lang(lang):
    if lang not in SUPPORTED_LANGUAGES and lang != "":
        abort(404)
    elif lang == "":
        return render_template("es/register.html")
    else: 
        return render_template(f"{lang}/register.html")
    
@app.route('/admin/insert', methods=["GET"])
def insert_route():
    if not len(session): return redirect('/form?form=login')

    elif session.get('role') == 'student': return redirect('/dashboard')

    else: return render_template('es/insert.html')
    
@app.route("/students/panel", methods=["GET"])
def students_panel_default():
    if not len(session):
        abort(401)
        
    r = requests.get(server_url+f"/api/render/courses", headers={"Content-Type":"application/json", "Accept":"application/json", "Authorization":f"Bearer {components.generate_jwt({'subscription':session.get("subscription")}, secret_key=secret_key)}"})
    response = lambda: components.get_component(session=session, component="header.html", secret_key=secret_key, server_url=server_url)
    result, status = components.retry(response, 3, 200)
    if r.status_code == 200 and status == 200:
        return render_template("es/students-panel.html", data=r.json(), header=result)    
    else: 
        abort(500)
    
@app.route("/students/panel/<lang>", methods=["GET"])
def students_panel(lang):
    if not len(session):
        abort(401)
        
    if lang not in SUPPORTED_LANGUAGES and lang != "":
        abort(404)
    elif lang == "":
        return render_template("es/students-panel.html")

    r = requests.get(server_url+f"/api/render/courses?subscription={session.get('subscription')}", headers={"Content-Type":"application/json", "Accept":"application/json", "Authorization":f"Bearer {components.generate_jwt({'subscription':session.get("subscription")}, secret_key=secret_key)}"})
    response = lambda: components.get_component(session=session, component="header.html", secret_key=secret_key, server_url=server_url)
    result, status = components.retry(response, 3, 200)
    if r.status_code == 200 and status == 200:
        return render_template("es/students-panel.html", data=r.json(), header=result)    
    else: 
        abort(500)
    
@app.route("/students/task", methods=["GET"])
def students_task_default():   
    if not len(session):
        abort(401)
        
    course_id = request.args.get("course_id")
    if course_id == None:
        abort(400)
        
    r = requests.get(server_url+f"/api/render/course?course_id={course_id}", headers={"Content-Type":"application/json", "Accept":"application/json", "Authorization":f"Bearer {components.generate_jwt({'subscription':session.get("subscription")}, secret_key=secret_key)}"})
    response = lambda: components.get_component(session=session, component="header.html", secret_key=secret_key, server_url=server_url)
    result, status = components.retry(response, 3, 200)
    if r.status_code == 200 and status == 200:
        return render_template("es/students-task.html", data=r.json(), description=r.json().get("description"), header=result)    
    else: 
        abort(500)
    
@app.route("/students/task/<lang>", methods=["GET"])
def students_task(lang):
    if not len(session):
        abort(401)
        
    if lang not in SUPPORTED_LANGUAGES and lang != "":
        abort(404)
    elif lang == "":
        return render_template("es/students-task.html")
        
    course_id = request.args.get("course_id")
    if course_id == None:
        abort(400)
        
    r = requests.get(server_url+f"/api/render/course?course_id={course_id}", headers={"Content-Type":"application/json", "Accept":"application/json", "Authorization":f"Bearer {components.generate_jwt({'subscription':session.get("subscription")}, secret_key=secret_key)}"})
    response = lambda: components.get_component(session=session, component="header.html", secret_key=secret_key, server_url=server_url)
    result, status = components.retry(response, 3, 200)
    if r.status_code == 200 and status == 200:
        return render_template("es/students-task.html", data=r.json(), header=result)    
    else: 
        abort(500)
        
@app.route("/dashboard/class", methods=["GET"])
def dashboard_students_class():
    if not len(session):
        abort(401)
    
    if session.get("role") == "student":
        abort(401)
    
    r = requests.get(server_url+f"/api/render/courses?subscription={session.get('subscription')}", headers={"Content-Type":"application/json", "Accept":"application/json", "Authorization":f"Bearer {components.generate_jwt({'subscription':session.get("subscription")}, secret_key=secret_key)}"})
    response = lambda: components.get_component(session=session, component="horizontal-header.html", secret_key=secret_key, server_url=server_url)
    result, status = components.retry(response, 3, 200)
    if r.status_code != 200 or status != 200:
        abort(500)
        
    return render_template("es/dashboard_class.html", data=r.json(), header=result)
        
@app.route("/dashboard/class/<class_courses>", methods=["GET"])
def dashboard_students_specific_class(class_courses):
    if not len(session):
        abort(401)
    
    r = requests.get(server_url+f"/api/render/courses?subscription={session.get('subscription')}", headers={"Content-Type":"application/json", "Accept":"application/json", "Authorization":f"Bearer {components.generate_jwt({'subscription':session.get("subscription")}, secret_key=secret_key)}"})
    response = lambda: components.get_component(session=session, component="horizontal-header.html", secret_key=secret_key, server_url=server_url)
    result, status = components.retry(response, 3, 200)
    if r.status_code != 200 or status != 200:
        abort(500)
        
    return render_template("es/dashboard_class_section.html", data=r.json(), header=result)
    
@app.route("/dashboard/add/material", methods=["GET"])
def dashboard_add_material():
    if not len(session):
        abort(401)
        
    if session.get("role") not in ["admin", "teacher"]:
        abort(401)
        
    return render_template("es/material.html")
    
@app.route('/robots.txt')
@app.route('/sitemap.xml')
def static_from_root():
    return send_from_directory("static/seo", request.path[1:])

@app.route('/favicon.ico')
def favicon():
    return send_from_directory("static/icons", "favicon.ico")

if __name__=="__main__":
    app.run(debug=True, host="127.0.0.1", port=5000, reloader_type="watchdog")