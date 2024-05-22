import psycopg2

con = psycopg2.connect(host='localhost', user='dieu', password='OhGodPleaseYes', dbname='piw')

cr = con.cursor()

def resetDB():
    sql : str = """
        DROP TABLE utilisateur,village,ressource,batiment,entrepot,stock;
    """
    cr.execute(sql)
    with open('jeu.sql', 'r') as sql_file:
        sql_script = sql_file.read()
    cr.execute(sql_script)

def get_user(var:str,):
    sql: str ="SELECT id_user FROM utilisateur WHERE username = %(var)s;"
    cr.execute(sql, {   
        "var" : var
    })
    return cr.fetchone()

def create_user(username):
    sql: str = "INSERT INTO utilisateur(username) VALUES (%(username)s);"
    cr.execute(sql,{
        "username": username
    })

def create_ressource(name, nb_max):
    sql : str = "INSERT INTO ressource(nom, nb_max) VALUES (%(name)s, %(nb_max)s);"
    cr.execute(sql,{
        "name": name,
        "nb_max": nb_max
    })

def get_id_ressource(nom):
    sql: str ="SELECT id_ressource FROM ressource WHERE nom = %(var)s;"
    cr.execute(sql, {   
        "var" : nom
    })
    return cr.fetchone()

def create_village(user_id, name): 
    sql :str = """INSERT INTO village(id_user, nom_village, nb_bat) VALUES (%(user_id)s,%(name)s,1);
    INSERT INTO entrepot(niveau)
    VALUES(0);
    SELECT id_village FROM village;
    """
    cr.execute(sql, {
        "user_id": user_id,
        "name" : name
    })

    selection = cr.fetchone()

    sql ="""INSERT INTO stock(id_village,id_ress,nb_ress) 
            VALUES (%(selection)s,%(bois)s,50),
            (%(selection)s,%(pierre)s,50),
            (%(selection)s,%(bouphe)s,50),
            (%(selection)s,%(fer)s,0),
            (%(selection)s,%(gens)s,10);
        """
    cr.execute(sql,{
        "selection" : selection,
        "pierre" : get_id_ressource('pierre'),
        "bois" : get_id_ressource('bois'),
        "bouphe" : get_id_ressource('bouphe'),
        "fer" : get_id_ressource('fer'),
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
    batiment = cr.fetchone()
    print(batiment)

def update_quantite(id_village, id_ressource, quantite):
    
    sql = "UPDATE stock SET nb_ress = %(quantite)s WHERE id_village = %(id_village)s AND id_ress = %(id_ressource)s;"
    cr.execute(sql, {
        "id_village" : id_village,
        "id_ressource" : id_ressource,
        "quantite" : quantite
    })

def cost():
    pass

def upgrade_entrepot(id_village):
    sql: str = "SELECT niveau FROM entrepot WHERE id_village = %(var)s;"
    cr.execute(sql, {"var": id_village})
    niveau = cr.fetchone()
    if niveau <18:
        updateSQL = """UPDATE entrepot SET niveau = %(niveau)s WHERE id_village = %(var)s;
                """
        cr.execute(sql, {
            "var": id_village,
            "niveau" : niveau+1,
            })
        
        return True
    return False

def create_bat(id_village, nom, id_ressources=None):
    sql = """INSERT INTO batiment(id_village, niveau, nom_batiment, id_ress)
        VALUES (%(id_village)s, 1, %(nom_bat)s, %(id_ress)s);
        """
    cr.execute(sql,{
        "id_village" : id_village,
        "nom_bat": nom,
        "id_ress" : id_ressources, 
    })
    #Coute de l'argent

    #prod


resetDB()

if 1:
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
