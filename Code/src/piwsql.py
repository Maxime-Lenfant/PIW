import psycopg2

con = psycopg2.connect(host='localhost', user='dieu', password='OhGodPleaseYes', dbname='piw')

cr = con.cursor()

def resetDB():
    """
    Reset la base de donnée en supprimant toutes les tables et en executant le fichier sql BDDJeu.sql contenu dans le répertoire
    """
    sql : str = """
        DROP TABLE utilisateur,village,ressource,batiment,liste_batiment,cout_batiment,entrepot,stock;
    """
    cr.execute(sql)
    with open('BDDJeu.sql', 'r') as sql_file:
        sql_script = sql_file.read()
    cr.execute(sql_script)

def get_user(username:str,) -> int:
    """
    Retourne l'identifiant de l'utilisateur dont le surnom (username) est passé en argument
    """
    sql: str ="SELECT id FROM utilisateur WHERE login = %(login)s;"
    cr.execute(sql, {   
        "login" : username
    })
    return cr.fetchone()

def create_user(login, password):
    """
    Créé un utilisateur avec le surnom passé en argument
    """
    sql: str = "INSERT INTO utilisateur(login, password) VALUES (%(login)s, %(password)s);"
    cr.execute(sql,{
        "login": login,
        "password" : password,
    })

def get_id_ressource(nom: str) -> int:
    """
    Retourne l'identifiant de la ressources nommé en paramètre
    """
    sql: str ="SELECT id_ressource FROM ressource WHERE nom = %(var)s;"
    cr.execute(sql, {   
        "var" : nom
    })
    res = cr.fetchone()[0]
    return res

def get_ress_prod(nom: str) -> int:
    """
    Retourne l'identifiant de la ressources nommé en paramètre
    """
    sql: str ="SELECT id_ress FROM liste_batiment WHERE nom_bat = %(var)s;"
    cr.execute(sql, {   
        "var" : nom
    })
    res = cr.fetchone()[0]
    return res

def create_ressource(nom: str):
    """
    Créé une ressource avec pour argument son nom, elle est commune a toute la BDD
    """
    sql : str = "INSERT INTO ressource(nom) VALUES (%(nom)s);"
    cr.execute(sql,{
        "nom": nom
    })

def get_nb_ress() -> str:
    """
    Retourne le nombre de ressource
    """
    sql:str = """SELECT * FROM ressource"""
    cr.execute(sql,{})
    return len(cr.fetchall())

def get_stock(id_village, id_ressource):
    sql: str ="""SELECT nb_ress FROM stock 
                WHERE id_village = %(id_village)s AND id_ress = %(id_ressource)s;"""
    cr.execute(sql, {   
        "id_village" : id_village,
        "id_ressource": id_ressource,
    })
    res = cr.fetchone()[0]
    return res

def get_stock_max(id_village, id_ressource):
    sql: str ="""SELECT nb_max FROM stock 
                WHERE id_village = %(id_village)s AND id_ress = %(id_ressource)s;"""
    cr.execute(sql, {   
        "id_village" : id_village,
        "id_ressource": id_ressource,
    })
    res = cr.fetchone()[0]
    return res

def update_stock_max(id_village, id_ressource, nb_max):
    
    sql = "UPDATE stock SET nb_max = %(nb_max)s WHERE id_village = %(id_village)s AND id_ress = %(id_ressource)s;"
    cr.execute(sql, {
        "id_village" : id_village,
        "id_ressource" : id_ressource,
        "nb_max" : nb_max,
    })

def create_village(user_id, name): 
    sql :str = """INSERT INTO village(id_user, nom_village) VALUES (%(user_id)s,%(name)s);
    SELECT id_village FROM village;
    """
    cr.execute(sql, {
        "user_id": user_id,
        "name" : name
    })

    selection = cr.fetchone()


    sql ="""INSERT INTO entrepot(id_village,niveau)
        VALUES(%(selection)s, 1);
    
        INSERT INTO stock(id_village,id_ress,nb_ress,nb_max) 
            VALUES (%(selection)s,%(bois)s,500,1000),
            (%(selection)s,%(pierre)s,500,1000),
            (%(selection)s,%(bouphe)s,500,1000),
            (%(selection)s,%(gens)s,100,100);
        """
    cr.execute(sql,{
        "selection" : selection,
        "pierre" : get_id_ressource('pierre'),
        "bois" : get_id_ressource('bois'),
        "bouphe" : get_id_ressource('bouphe'),
        "gens" : get_id_ressource('gens')
    })

def get_village_id(nom):
    sql: str ="SELECT id_village FROM village WHERE nom_village = %(var)s;"
    cr.execute(sql, {   
        "var" : nom
    })
    return cr.fetchone()

def show_village_summary(village_id):
    sql = """
    SELECT nom_village FROM village WHERE id_village = %(village_id)s;
    """
    cr.execute(sql, {
        "village_id": village_id
    })
    nom = cr.fetchone()
    print("Nom du village : {0}".format(nom))
    sql = """
    SELECT * FROM stock WHERE id_village = %(village_id)s;
    """
    cr.execute(sql, {
        "village_id": village_id,
    })  
    stock = cr.fetchall()
    print(stock)
    sql = """
    SELECT * FROM batiment WHERE id_village = %(village_id)s;
    """
    cr.execute(sql, {
        "village_id": village_id,
    })
    batiment = cr.fetchall()
    print(batiment)

def update_quantite(id_village, id_ressource, quantite):
    
    sql = "UPDATE stock SET nb_ress = %(quantite)s WHERE id_village = %(id_village)s AND id_ress = %(id_ressource)s;"
    cr.execute(sql, {
        "id_village" : id_village,
        "id_ressource" : id_ressource,
        "quantite" : quantite
    })

def get_cout(nom_batiment, niveau, id_ressource):
    sql:str = """SELECT cout FROM cout_batiment 
                 WHERE nom_bat = %(nom_batiment)s AND niveau = %(niveau)s AND id_ress = %(id_ressource)s
                 """
    cr.execute(sql,{
        "nom_batiment": nom_batiment, 
        "niveau" : niveau, 
        "id_ressource": id_ressource
        })
    res = cr.fetchone()[0]
    return res

def paye(id_village, nom_batiment, niveau, id_ressource):
    stock = get_stock(id_village, id_ressource)
    cout = get_cout(nom_batiment,niveau,id_ressource)
    if stock >= cout:
        stock -= cout
        update_quantite(id_village, id_ressource, stock)
        return True
    return False

#uniquement pour l'entrepot
def cost(id_village, id_ressource, cout):
    sql: str = "SELECT nb_ress FROM stock WHERE id_village = %(id_village)s AND id_ress = %(id_ressource)s; "
    cr.execute(sql, {
        "id_village" : id_village,
        "id_ressource" : id_ressource,
    })
    stock = cr.fetchone()[0]
    if(stock >= cout):
        stock -= cout
        update_quantite(id_village, id_ressource, stock)
        return True
    return False
    
    # verif de la ressource
    # retrait de la ressource avec update quantité

def upgrade_entrepot(id_village):
    sql: str = "SELECT niveau FROM entrepot WHERE id_village = %(var)s;"
    cr.execute(sql, {"var": id_village})
    niveau = cr.fetchone()[0]
    print(niveau)
    if niveau < 5:
        sql = """UPDATE entrepot SET niveau = %(niveau)s WHERE id_village = %(var)s;
                """
        cr.execute(sql, {
            "var": id_village,
            "niveau" : niveau+1,
            })
        cost(id_village, get_id_ressource("bois"), cout=50)
        cost(id_village, get_id_ressource("pierre"), cout=50)
        cost(id_village, get_id_ressource("bouphe"), cout=20)
        for i in range(1,get_nb_ress()+1):
            update_stock_max(id_village, i,(get_stock_max(id_village, i)*1.2)+10)        
        return True
    if (niveau >= 5) & (niveau < 10) :
        sql = """UPDATE entrepot SET niveau = %(niveau)s WHERE id_village = %(var)s;
                """
        cr.execute(sql, {
            "var": id_village,
            "niveau" : niveau+1,
            })
        cost(id_village, id_ressource=0, cout=100)
        cost(id_village, id_ressource=1, cout=100)
        cost(id_village, id_ressource=2, cout=50)
        for i in range(1,get_nb_ress()+1):
            update_stock_max(i,(get_stock_max(id_village, i)*1.4)+10)        
        return True
    if (niveau >=10) & (niveau <15) :
        sql = """UPDATE entrepot SET niveau = %(niveau)s WHERE id_village = %(var)s;
                """
        cr.execute(sql, {
            "var": id_village,
            "niveau" : niveau+1,
            })
        cost(id_village, id_ressource=0, cout=300)
        cost(id_village, id_ressource=1, cout=300)
        cost(id_village, id_ressource=2, cout=150)
        for i in range(1,get_nb_ress()+1):
            update_stock_max(i,(get_stock_max(id_village, i)*1.6)+10)        
        return True
    
    return False

def construire_bat(id_village, nom_batiment, niveau=0):
    #selection des ressources et de leur quantite 
    # la fonction cost recupere sans parametres la qte de ressource du bat en fonction du lvl
    # et se charge de verifier et payer
    sql: str = """ SELECT id_ress, niveau FROM cout_batiment 
            WHERE nom_bat = %(nom)s AND niveau = %(niveau)s;
            """
    cr.execute(sql,{
        "nom" : nom_batiment,
        "niveau" : niveau,
    })
    cout_total = cr.fetchall()

    for i in range(len(cout_total)):
        paye(id_village, nom_batiment, niveau, cout_total[0][i])

    prod = 5*niveau+10

    sql = """INSERT INTO batiment(id_village, niveau, nom_bat, id_ress, production)
    VALUES (%(id_village)s, 1, %(nom)s, %(id_ress)s, %(prod)s);
    """
    cr.execute(sql,{
        "id_village" : id_village,
        "nom": nom_batiment,
        "id_ress" : get_ress_prod(nom_batiment), 
        "prod" : prod,
    })


def upgrade_bat(id_village, nom_batiment):
    #recupere le niveau actuel du batiment
    sql: str = """SELECT niveau FROM batiment 
                WHERE id_village = %(id_village)s AND nom_bat = %(nom)s;
                """
    cr.execute(sql,{"id_village" : id_village,
                    "nom" : nom_batiment,})
    niveau = cr.fetchone()[0]
    new_niveau = niveau + 1
    prod = 5*(new_niveau)+10
    fdata = {
        "nom" : nom_batiment,
        "niveau" : niveau,
        "id_village" : id_village,
        "prod" : prod,
        "new_niveau" : new_niveau,
    }
    #selection des ressources et de leur quantite 
    # la fonction cost recupere sans parametres la qte de ressource du bat en fonction du lvl
    # et se charge de verifier et payer
    sql: str = """ SELECT id_ress, niveau FROM cout_batiment 
            WHERE nom_bat = %(nom)s AND niveau = %(niveau)s;
            """
    cr.execute(sql,{
        "nom" : nom_batiment,
        "niveau" : niveau,
    })
    cout_total = cr.fetchall()

    for i in range(len(cout_total)):
        paye(id_village, nom_batiment, niveau, cout_total[0][i])


        sql = """UPDATE batiment SET niveau = %(new_niveau)s, production = %(prod)s
            WHERE id_village = %(id_village)s AND nom_bat = %(nom)s;
            """
        cr.execute(sql,fdata)

#create_bat et set_cout sont utile pour la creation de la BDD pas pdt le jeu
def create_bat(nom, id_ressources=None):
    #créé les templates des batiments
    sql = """INSERT INTO liste_batiment(nom_bat, id_ress)
        VALUES (%(nom_bat)s, %(id_ress)s);
        """
    cr.execute(sql,{
        "nom_bat": nom,
        "id_ress" : id_ressources, 
    })

def set_cout(nom_batiment, niveau, id_ressource, qte):
    #sert a set up les couts des upgrades de batiments (1 ligne par ressource) de manière generale (pas par village)
    sql:str = """INSERT INTO cout_batiment(nom_bat, niveau, id_ress, cout)
            VALUES(%(nom_bat)s,%(niveau)s ,%(id_ress)s,%(cout)s);
            """
    cr.execute(sql,{
        "nom_bat": nom_batiment,
        "niveau" : niveau, 
        "id_ress" : id_ressource,
        "cout" : qte,
    })

def is_crendential_correct(login: str, hashed_password: str) -> bool:
    sql: str = """SELECT id, login
                FROM users
                WHERE login = %(login)s AND password = %(hashed_password)s;"""
    cr.execute(sql,{
        "login" : login,
        "hashed_password" : hashed_password,
        })
    res = cr.fetchall()
    return len(res) == 1
    
def voir():
    sql: str = """SELECT * FROM users;"""
    cr.execute(sql, {})
    a = cr.fetchall()
    print(a) 


if 0:
    baseMax = 50
    create_ressource('bois', baseMax)
    create_ressource('pierre',baseMax)
    create_ressource('bouphe',baseMax+100)
    create_ressource('fer',baseMax-30)
    create_ressource('gens',baseMax+200)


    create_user("GuerrierTacosMagiqueDemoniaque")
    id_user=get_user('GuerrierTacosMagiqueDemoniaque')
    create_village(id_user,'TacosCity')
    id_village = get_village_id('TacosCity')
    show_village_summary(id_village)
    update_quantite(id_village, get_id_ressource("bois"),1000)
    show_village_summary(id_village)
