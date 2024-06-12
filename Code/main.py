from flask import Flask, render_template, request, session, redirect, jsonify
import hashlib
import psycopg2
import random
import datetime
import src.piwsql as piwsql

con = psycopg2.connect(host='localhost', user='dieu', password='OhGodPleaseYes', dbname='piw')

cr = con.cursor()

app = Flask(__name__)
app.secret_key = 'the random string'

batimentOuvert : str = ""
villageOuvert : int = piwsql.get_village_id("CracklandCity")

@app.route("/")
def index():
    if not logged_in():
# Si non alors on le redirige sur la page de connexion
        return redirect("/login")
# Sinon on peux lui renvoyer le contenu de notre page.
    return render_template("jeusupergenial.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/cecinestpasunebackdoor")
def backdoor():
    return render_template("jeusupergenial.html")

@app.route("/register")
def register():
    return render_template("login.html")

@app.route("/setBDD")
def setBDD():
    with open('src/BDDlogin.sql', 'r') as sql_file:
        sql_script = sql_file.read()
    cr.execute(sql_script)
    return redirect("/register")

@app.route("/register/auth", methods=["POST"])
def register_auth():
# On note que l'on utilise form dans une requête POST et args dans une requêtes GET
    login: str = request.form["login"]
    password: str = request.form["password"]
    hashed_password: str = hash_sha512(password)
    print(f"login = {login}, password = {password}, hashed_password = {hashed_password}")
    
    piwsql.add_user(login, hashed_password)
    return redirect("/login")

@app.route("/login/auth", methods=["POST"])
def login_auth():
# On note que l'on utilise form dans une requête POST et args dans une requêtes GET
    print("OH")
    print(request)
    print(request.form)
    login: str = request.form["login"]
    print(login)
    password: str = request.form["password"]
    """
    hashed_password: str = hash_sha512(password)
    auth_ok: bool = is_crendential_correct(login, hashed_password)
    if auth_ok:
        user_token: str = token_for(login)
        set_token(login, user_token)
        session["token"] = user_token
        return "Auth success !"
    else:"""
    return render_template("auth.html")

#test route post get
@app.route('/infoBat', methods=['GET'])
def nomBatPopUp():
    nom_bat = request.args.get('nom_bat')
    print(nom_bat)
    batimentOuvert = nom_bat
    return jsonify({'nom_bat': nom_bat, "niveau_bat": 1})

@app.route('/ameliorerBat', methods=['GET'])
def ameliorerBat():
    batimentOuvert = request.args.get("batimentOuvert")
    temp = piwsql.upgrade_bat(villageOuvert,batimentOuvert)
    if  temp[0] == True:
        return jsonify({'ameliore':True,'nom_bat':batimentOuvert,"niveau_bat":temp[1]})
    else :
        return jsonify({'ameliore':False,'nom_bat':batimentOuvert,"niveau_bat":temp[1]})
    
@app.route('/infoRessources', methods=['GET'])
def infoRessources():
    return jsonify({'nbGens':piwsql.get_stock(villageOuvert,piwsql.get_id_ressource("Gens")),'nbKayou':piwsql.get_stock(villageOuvert,piwsql.get_id_ressource("Kayou")),"nbBois":piwsql.get_stock(villageOuvert,piwsql.get_id_ressource("Bois")),"nbBouphe": piwsql.get_stock(villageOuvert,piwsql.get_id_ressource("Bouphe"))})



def hash_sha512(value: str) -> str:
    h = hashlib.sha512()
    h.update(value.encode())
    return h.hexdigest()   

def random_number() -> int | float:
    rand: str= random.random()*random.uniform(100,1000)
    return rand

def current_datetime() -> str:
    date_as_str: str = datetime.datetime.now()
    return date_as_str.strftime('%Y%m%H%M%S')

def token_for(login: str) -> str:
    token_content: str = ""
    r_num = random_number()
    str_num: str = str(r_num)
    token_content += hash_sha512(str_num)
    c_date: str = current_datetime()
    token_content += hash_sha512(c_date)
    token_content += hash_sha512(login)
    return hash_sha512(token_content)

def set_token(login: str, token: str):
    sql: str = """UPDATE users SET token = %(token)s WHERE login = %(login)s"""
    cr.execute(sql, {"token" : token, "login" : login})
    piwsql.voir()

def check_token_validity(token: str) -> bool:
    sql: str = """SELECT * FROM users WHERE token = %(token)s"""
    cr.execute(sql,{"token": token})
    res = cr.fetchall()
    return len(res)

def logged_in() -> bool:
    token: str = session.get("token", None)
    if token:
        token_valid: bool = check_token_validity(token)
        if token_valid:
            return True
    return False

if 1:
    piwsql.resetDB()
    piwsql.create_ressource("bois")
    piwsql.create_ressource("pierre")
    piwsql.create_ressource("bouphe")
    piwsql.create_ressource("gens")
 
    piwsql.create_bat("scierie",piwsql.get_id_ressource("bois"))
    piwsql.create_bat("carriere",piwsql.get_id_ressource("pierre"))
    piwsql.create_bat("wadko",piwsql.get_id_ressource("bouphe"))
    piwsql.create_bat("maison",piwsql.get_id_ressource("gens"))

    piwsql.set_cout("scierie", 1, piwsql.get_id_ressource("bois"), 50)
    piwsql.set_cout("scierie", 1, piwsql.get_id_ressource("pierre"), 5)
    piwsql.set_cout("maison", 1, piwsql.get_id_ressource("bois"), 20)
    piwsql.set_cout("maison", 1, piwsql.get_id_ressource("pierre"), 20)
    piwsql.set_cout("scierie", 2, piwsql.get_id_ressource("bois"), 75)
    piwsql.set_cout("scierie", 2, piwsql.get_id_ressource("pierre"), 25)
    piwsql.set_cout("scierie", 2, piwsql.get_id_ressource("bouphe"), 5)

    piwsql.create_user("toto","1234")

    piwsql.create_village(piwsql.get_user("toto"),"CracklandCity")
    piwsql.show_village_summary(piwsql.get_village_id("CracklandCity"))


app.run(host="0.0.0.0", debug=True)
