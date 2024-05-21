CREATE TABLE utilisateur(id_user SERIAL PRIMARY KEY,
                        username varchar(255), 
                        login varchar(255)
                        );

CREATE TABLE village(id_village SERIAL PRIMARY KEY, 
                    id_user int,
                    nom_village varchar(255), 
                    nb_bat int,
                    FOREIGN KEY(id_user) REFERENCES utilisateur(id_user)
                    );

CREATE TABLE ressource (id_ressource SERIAL PRIMARY KEY, 
                        nom VARCHAR(255)
                        );

CREATE TABLE batiment (id_village int,
                       id_bat SERIAL PRIMARY KEY, 
                       niveau int, nb_bat int,
                       nom_bat varchar(255), 
                       id_ress int, 
                       FOREIGN KEY(id_ress) REFERENCES ressource(id_ressource),
                       FOREIGN KEY(id_village) REFERENCES village(id_village)
                      );

CREATE TABLE entrepot (id_village int, 
                       niveau int, 
                       id_entrepot SERIAL PRIMARY KEY, 
                       nb_max_bois int, 
                       nb_max_pierre int,
                       nb_max_bouphe int,
                       nb_max_fer int,
                       nb_max_gueux int,
                       
                       FOREIGN KEY(id_village) REFERENCES village(id_village)
                      ); 
                      
CREATE Table stock( id_village int, 
                   FOREIGN KEY(id_village) REFERENCES village(id_village), 
                   id_ress int, 
                   FOREIGN KEY(id_ress) REFERENCES ressource(id_ressource), 
                   nb_ress int
                   );
