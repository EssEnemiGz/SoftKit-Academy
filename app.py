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

# LIBRARYS
from datetime import timedelta, datetime
from flask import *
from dotenv import load_dotenv
import supabase
import requests
import jwt
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
if secret_key == None: secret_key = "ewkwer1231231kajeklew3213ropewp21oiewrop312309-490i3u2313jwlelk"
app.secret_key = secret_key
app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = "Lax"
app.config['SESSION_COOKIE_DOMAIN'] = f".{server_url.split('//')[1]}"
app.permanent_session_lifetime = timedelta(weeks=52) # Sesion con duracion de 52 semanas o 1 año

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
auth.supabase, exist.supabase, register.supabase, render.supabase, insert.supabase, meetings.supabase, login.supabase, tracker.supabase = db, db, db, db, db, db, db, db
login.server_url, register.server_url, meetings.server_url, render.server_url = server_url, server_url, server_url, server_url
insert.server_code, register.server_code = server_code, server_code
render.secret_key = secret_key

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

def generate_jwt(data):
    payload = {
        'session': data,
    }
    token = jwt.encode(payload, secret_key, algorithm='HS256')
    return token 

@app.route("/", methods=["GET"])
def index():
    return render_template(f"es/index.html")

@app.route("/<lang>", methods=["GET"])
def main(lang):
    if lang not in SUPPORTED_LANGUAGES:
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
    if len(session):
        return redirect("/students/panel")
    else:
        return render_template("es/form.html")
    
@app.route('/admin/insert', methods=["GET"])
def insert_route():
    if not len(session): return redirect('/form?form=login')

    elif session.get('role') == 'student': return redirect('/dashboard')

    else: return render_template('es/insert.html')
    
@app.route("/students/panel", methods=["GET"])
def students_panel_default():
    if not len(session):
        abort(401)
        
    r = requests.get(server_url+f"/api/render/courses", headers={"Content-Type":"application/json", "Accept":"application/json", "Authorization":f"Bearer {generate_jwt({'subscription':session.get("subscription")})}"})
    if r.status_code == 200:
        print(r.json())
        return render_template("es/students-panel.html", data=r.json())    
    else: 
        abort(500)
    
@app.route("/students/panel/<lang>", methods=["GET"])
def students_panel(lang):
    if not len(session):
        abort(401)
        
    if lang not in SUPPORTED_LANGUAGES:
        abort(404)
    elif lang == "":
        return render_template("es/students-panel.html")

    r = requests.get(server_url+f"/api/render/courses?subscription={session.get('subscription')}", headers={"Content-Type":"application/json", "Accept":"application/json", "Authorization":f"Bearer {generate_jwt({'subscription':session.get("subscription")})}"})
    if r.status_code == 200:
        return render_template("es/students-panel.html", data=r.json())    
    else: 
        abort(500)
    
@app.route("/students/task", methods=["GET"])
def students_task_default():   
    if not len(session):
        abort(401)
        
    course_id = request.args.get("course_id")
    if course_id == None:
        abort(400)
        
    r = requests.get(server_url+f"/api/render/course?course_id={course_id}", headers={"Content-Type":"application/json", "Accept":"application/json", "Authorization":f"Bearer {generate_jwt({'subscription':session.get("subscription")})}"})
    if r.status_code == 200:
        return render_template("es/students-task.html", data=r.json(), description=r.json().get("description"))    
    else: 
        abort(500)
    
@app.route("/students/task/<lang>", methods=["GET"])
def students_task(lang):
    if not len(session):
        abort(401)
        
    if lang not in SUPPORTED_LANGUAGES:
        abort(404)
    elif lang == "":
        return render_template("es/students-task.html")
        
    course_id = request.args.get("course_id")
    if course_id == None:
        abort(400)
        
    r = requests.get(server_url+f"/api/render/course?course_id={course_id}", headers={"Content-Type":"application/json", "Accept":"application/json", "Authorization":f"Bearer {generate_jwt({'subscription':session.get("subscription")})}"})
    if r.status_code == 200:
        return render_template("es/students-task.html", data=r.json())    
    else: 
        abort(500)
        
@app.route("/dashboard/admin/students", methods=["GET"])
def admin_dashboard_students():
    return render_template("es/dashboard_students_section.html")
    
@app.route('/robots.txt')
@app.route('/sitemap.xml')
def static_from_root():
    return send_from_directory("static/seo", request.path[1:])

@app.route('/favicon.ico')
def favicon():
    return send_from_directory("static/icons", "favicon.ico")

if __name__=="__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)