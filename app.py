# MICROSERVICES
import microservices.auth as auth
import microservices.existence as exist
import microservices.hash as hash
import microservices.login as login
import microservices.register as register
import microservices.render as render
import microservices.insert as insert

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

# Configuracion de la aplicacion web
app = Flask(__name__)
if secret_key == None: secret_key = "ewkwerkajeklewropewpoiewrop309-490i3ujwlelk"
app.secret_key = secret_key
app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.permanent_session_lifetime = timedelta(weeks=52) # Sesion con duracion de 52 semanas o 1 año

# Conexion a base de datos
db = supabase.create_client(database, api)
auth_key = db.auth.sign_in_with_password( {'email':admin_email, 'password':admin_passw} )
if auth_key.session:
    token = auth_key.session.access_token
    pass
else:
    print(f"Error de auth. {auth_key.error}")

# BLUEPRINTS
auth.supabase, exist.supabase, register.supabase, render.supabase, insert.supabase = db, db, db, db, db
login.server_url, register.server_url = server_url, server_url

app.register_blueprint(auth.auth_bp)
app.register_blueprint(exist.existence_bp)
app.register_blueprint(hash.hash_bp)
app.register_blueprint(login.login_bp)
app.register_blueprint(register.register_bp)
app.register_blueprint(render.render_bp)
app.register_blueprint(insert.insert_bp)

@app.route("/", methods=["GET"])
def main():
    return render_template("index.html")

@app.route("/dashboard", methods=["GET"])
def dashboard():
    if len(session):
        return render_template("dashboard.html")
    else:
        return redirect( '/form?form=login' )
    
@app.route("/form", methods=["GET"])
def form():
    if len(session):
        return redirect("/dashboard")
    else:
        return render_template("form.html")
    
@app.route('/admin/insert', methods=["GET"])
def insert_route():
    if not len(session):
        redirect('/form?form=login')
    
    if session.username != 'biscenp':
        redirect('/')
    
    return render_template('insert.html')

if __name__=="__main__":
    app.run(debug=True)