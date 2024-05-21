import psycopg2

con = psycopg2.connect(host='localhost', user='dieu', password='OhGodPleaseYes', dbname='piw')

cr = con.cursor()

def get_user(var:str,)->str:
    sql: str ="SELECT id_user FROM utilisateur WHERE username = %(var)s;"
    cr.execute(sql)
    return cr.fetchone()

def create_user(username):
    id_user = get_user(username)
    sql: str = "INSERT INTO utilisateur(id_user ,username , login) VALUES (%(username)s,'');"
    cr.execute(sql)

def create_ressource(name):
    sql : str = "INSERT INTO ressource(id_ressource, nom) VALUES %(name)s;"
    cr.execute(sql)

#"create_ressource("('bois'),('pierre'),('bouphe'),('fer'), ('gueux')")"   

def create_village(user_id, name): 
    sql :str = """INSERT INTO village(id_village,id_user, nom_village, nb_bat) VALUES ({0},{1},{2});
    INSERT INTO entrepot(id_village, niveau, id_entrepot, nb_max_bois, nb_max_pierre,nb_max_bouphe,nb_max_fer,nb_max_gueux)
    VALUES(0,50,50,50,50,10);
    SELECT id_village FROM village;
    """.format(user_id,name,0)
    cr.execute(sql)
    selection = cr.fetchone()
    sql ="""INSERT INTO stock(id_village,id_ress,nb_ress) 
            VALUES (%(selection)s,0,50),
            (%(selection)s,1,50),
            (%(selection)s,2,50),
            (%(selection)s,3,0),
            (%(selection)s,4,10),
        """
    cr.execute(sql)

def show_village_summary(village_id):
    sql = """
    SELECT nom_village FROM village WHERE id_village = %(village_id)s;
    """
    cr.execute(sql)
    nom = cr.fetchone()
    sql = """
    SELECT * FROM stock WHERE id_village = %(village_id)s;
    """
    cr.execute(sql)
    stock = cr.fetchone()
    sql = """
    SELECT * FROM batiment WHERE id_village = %(village_id)s;
    """
    cr.execute(sql)
    batiment = cr.fetchone()

