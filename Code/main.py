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

def create_ressource(name):
    sql : str = "INSERT INTO ressource(nom, nb_max) VALUES (%(name)s, %(nb_max)s);"
    cr.execute(sql,{
        "name": name,
    })

def get_nb_ress():
    sql:str = """SELECT * FROM ressource"""
    cr.execute(sql,{})
    return len(cr.fetchall)

def get_id_ressource(nom):
    sql: str ="SELECT id_ressource FROM ressource WHERE nom = %(var)s;"
    cr.execute(sql, {   
        "var" : nom
    })
    return cr.fetchone()

def get_stock(id_village, id_ressource):
    sql: str ="""SELECT nb_ress FROM ressource 
                WHERE id_village = %(id_village)s AND id_ressource = %(id_ressource)s;"""
    cr.execute(sql, {   
        "id_village" : id_village,
        "id_ressource": id_ressource,
    })
    return cr.fetchone()

def get_stock_max(id_village, id_ressource):
    sql: str ="""SELECT nb_max FROM ressource 
                WHERE id_village = %(id_village)s AND id_ressource = %(id_ressource)s;"""
    cr.execute(sql, {   
        "id_village" : id_village,
        "id_ressource": id_ressource,
    })
    return cr.fetchone()

def update_stock_max(id_village, id_ressource, nb_max):
    
    sql = "UPDATE stock SET nb_max = %(nb_max)s WHERE id_village = %(id_village)s AND id_ress = %(id_ressource)s;"
    cr.execute(sql, {
        "id_village" : id_village,
        "id_ressource" : id_ressource,
        "quantite" : nb_max,
    })

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

def cost(id_village, id_ressource, cout):
    sql: str = "SELECT nb_ress FROM stock WHERE id_village = %(id_village)s AND id_ress = %(id_ressource)s; "
    cr.execute(sql, {
        "id_village" : id_village,
        "id_ressource" : id_ressource,
    })
    stock = cr.fetchone()
    if(stock >= cout):
        stock -= cout
        update_quantite(id_village, id_ressource, stock)
        return True
    return False
    
    # verif de la ressource
    # retrait de la ressource avec update quantité

    pass

def get_cout(nom_batiment, niveau, id_ressource):
    sql:str = """SELCT cout FROM cout_batiment 
                 WHERE nom_batiment = %(nom_batiment)s AND niveau = %(niveau)s AND id_ressource = %(id_ressource)s
                 """
    cr.execute(sql,{
        "nom_batiment": nom_batiment, 
        "niveau" : niveau, 
        "id_ressource": id_ressource
        })
    return cr.fetchone()

def verif_qte(id_village, nom_batiment, niveau, id_ressource):
    if get_stock(id_village, id_ressource) > get_cout(nom_batiment,niveau,id_ressource):
        return True
    return False

def upgrade_entrepot(id_village):
    #il manque d'update les ressources max dans la table ressource
    sql: str = "SELECT niveau FROM entrepot WHERE id_village = %(var)s;"
    cr.execute(sql, {"var": id_village})
    niveau = cr.fetchone()
    if niveau <5:
        sql = """UPDATE entrepot SET niveau = %(niveau)s WHERE id_village = %(var)s;
                """
        cr.execute(sql, {
            "var": id_village,
            "niveau" : niveau+1,
            })
        cost(id_village, id_ressource=0, cout=50)
        cost(id_village, id_ressource=1, cout=50)
        cost(id_village, id_ressource=2, cout=20)
        for i in range(1,get_nb_ress()+1):
            update_stock_max(i,(get_stock_max(id_village, i)*1.2)+10)        
        return True
    if (niveau >=5) & (niveau < 10) :
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

def construire_bat(id_village, nom_batiment, prod, id_ressource, niveau=0):
    isok = 1
    sql: str = """ SELECT id_ressource, cout, niveau FROM cout_batiment 
            WHERE nom_bat = %(nom)s AND niveau = %(niveau)s;
            """
    cr.execute(sql,{
        "nom" : nom_batiment,
        "niveau" : niveau,
    })
    cout_total = cr.fetchall()
    for i in range(len(cout_total)):
        if verif_qte(id_village,nom_batiment,niveau,i) == False:
            isok = 0
    if isok == 1:
        for i in range(len(cout_total)):
            cost(id_village,cout_total[0][i],cout_total[1][i])
        prod = 5*niveau+10
        sql = """INSERT INTO batiment(id_village, niveau, nom_batiment, id_ress, production)
        VALUES (%(id_village)s, 1, %(nom)s, %(id_ress)s, %(prod)s);
        """
        cr.execute(sql,{
            "id_village" : id_village,
            "nom": nom_batiment,
            "id_ress" : id_ressource, 
            "prod" : prod,
        })

def upgrade_bat(id_village, nom_batiment, prod, id_ressource, niveau=0):
    isok = 1
    fdata = {
        "nom" : nom_batiment,
        "niveau" : niveau,
        "id_village" : id_village,
        "id_ress" : id_ressource, 
        "prod" : prod,
        "new_niveau" : niveau+1,
    }
    sql: str = """ SELECT id_ressource, cout, niveau FROM cout_batiment 
            WHERE nom_bat = %(nom)s AND niveau = %(niveau)s;
            """
    cr.execute(sql,fdata)
    cout_total = cr.fetchall()
    for i in range(len(cout_total)):
        if verif_qte(id_village,nom_batiment,niveau,i) == False:
            isok = 0
    if isok == 1:
        for i in range(cout_total.size()):
            cost(id_village,cout_total[0][i],cout_total[1][i])
        sql: str = """SELECT niveau FROM batiment 
                WHERE id_village = %(id_village)s AND nom_bat = %(nom)s;
                """
    cr.execute(sql,fdata)
    niveau = cr.fetchone()
    prod = 5*(niveau+1)+10
    sql = """UPDATE batiment SET niveau = %(new_niveau)s AND production = %(prod)s
        WHERE id_village = %(id_village)s AND nom_bat = %(nom_batiment)s;
        """
    cr.execute(sql,fdata)

#create_bat et set_cout sont utile pour la creation de la BDD pas pdt le jeu
def create_bat(id_village, nom, id_ressources=None):
    #créé les templates des batiments
    sql = """INSERT INTO batiment(id_village, niveau, nom_batiment, id_ress,)
        VALUES (%(id_village)s, 1, %(nom_bat)s, %(id_ress)s);
        """
    cr.execute(sql,{
        "id_village" : id_village,
        "nom_bat": nom,
        "id_ress" : id_ressources, 
    })

def set_cout(nom_batiment, niveau, id_ressource, qte):
    #sert a set up les couts des upgrades de batiments (1 ligne par ressource) de manière generale (pas par village)
    sql:str = """INSERT INTO cout_batiment(id_village, nom_bat, niveau, id_ressource, cout)
            VALUES(%(nom_bat)s,%(niveau)s %(id_ress)s,%(cout)s);
            """
    cr.execute(sql,{
        "nom_bat": nom_batiment,
        "niveau" : niveau, 
        "id_ress" : id_ressource,
        "cout" : qte,
    })



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
