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

# LIBRARYS
from datetime import timedelta
from flask import *
from dotenv import load_dotenv
import supabase
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
app.config['SESSION_COOKIE_SAMESITE'] = None
app.config['SESSION_COOKIE_DOMAIN'] = f".{server_url}"
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
auth.supabase, exist.supabase, register.supabase, render.supabase, insert.supabase, meetings.supabase = db, db, db, db, db, db
login.server_url, register.server_url, meetings.server_url = server_url, server_url, server_url
insert.server_code, register.server_code = server_code, server_code

app.register_blueprint(auth.auth_bp)
app.register_blueprint(exist.existence_bp)
app.register_blueprint(hash.hash_bp)
app.register_blueprint(login.login_bp)
app.register_blueprint(register.register_bp)
app.register_blueprint(render.render_bp)
app.register_blueprint(insert.insert_bp)
app.register_blueprint(meetings.meets_bp)
app.register_blueprint(calendar.calendar_bp)

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
    """if lang not in SUPPORTED_LANGUAGES:
        abort(404)
    elif lang == "":
        return render_template(f"es/dashboard.html")
        """
    if len(session):
        return render_template("es/dashboard.html")
    else:
        return redirect( '/form?form=login' )
    
@app.route("/form", methods=["GET"])
def form():
    if len(session):
        return redirect("/dashboard")
    else:
        return render_template("es/form.html")
    
@app.route('/admin/insert', methods=["GET"])
def insert_route():
    if not len(session): return redirect('/form?form=login')

    elif session.get('username') != 'biscenp': return redirect('/dashboard')

    else: return render_template('es/insert.html')
    
@app.route('/robots.txt')
@app.route('/sitemap.xml')
def static_from_root():
    return send_from_directory("static/seo", request.path[1:])

if __name__=="__main__":
    app.run(debug=True, port=5000)