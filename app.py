# LIBRARYS
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

# Configuracion de la aplicacion web
app = Flask(__name__)
if secret_key == None: secret_key = "ewaiourio32i3ujwlelk"
app.secret_key = secret_key
app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

# Conexion a base de datos
db = supabase.create_client(database, api)
auth_key = db.auth.sign_in_with_password( {'email':admin_email, 'password':admin_passw} )
if auth_key.session:
    token = auth_key.session.access_token
    headers = {
        "Authorization":f"Bearer {token}",
        "apikey":api
    }
else:
    print(f"Error de auth. {auth_key.error}")

@app.route("/", methods=["GET"])
def main():
    return render_template("index.html")

if __name__=="__main__":
    app.run(debug=True)