import piwsql as piw

if 1:

    piw.resetDB()

    piw.create_ressource("bois")
    piw.create_ressource("pierre")
    piw.create_ressource("bouphe")
    piw.create_ressource("gens")
 
    piw.create_bat("scierie",piw.get_id_ressource("bois"))
    piw.create_bat("carriere",piw.get_id_ressource("pierre"))
    piw.create_bat("wadko",piw.get_id_ressource("bouphe"))
    piw.create_bat("maison",piw.get_id_ressource("gens"))

    piw.set_cout("scierie", 1, piw.get_id_ressource("bois"), 50)
    piw.set_cout("scierie", 1, piw.get_id_ressource("pierre"), 5)
    piw.set_cout("maison", 1, piw.get_id_ressource("bois"), 20)
    piw.set_cout("maison", 1, piw.get_id_ressource("pierre"), 20)
    piw.set_cout("scierie", 2, piw.get_id_ressource("bois"), 75)
    piw.set_cout("scierie", 2, piw.get_id_ressource("pierre"), 25)
    piw.set_cout("scierie", 2, piw.get_id_ressource("bouphe"), 5)

    piw.create_user("toto","1234")

    piw.create_village(piw.get_user("toto"),"CracklandCity")
    piw.show_village_summary(piw.get_village_id("CracklandCity"))

    piw.upgrade_entrepot(piw.get_village_id("CracklandCity"))
    piw.construire_bat(piw.get_village_id("CracklandCity"),"maison")
    piw.construire_bat(piw.get_village_id("CracklandCity"),"scierie")

    piw.upgrade_bat(piw.get_village_id("CracklandCity"),"scierie")

    piw.show_village_summary(piw.get_village_id("CracklandCity"))

