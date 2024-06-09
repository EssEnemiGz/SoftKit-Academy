# LIBRARYS
from flask import *
#from flask_cors import CORS
#import psycopg2

app = Flask(__name__)
#CORS(app)

@app.route("/", methods=["GET"])
def main():
    return render_template("index.html")

if __name__=="__main__":
    app.run(debug=True)