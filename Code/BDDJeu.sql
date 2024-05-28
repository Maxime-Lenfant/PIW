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
                        nom VARCHAR(255),
                        nb_max int
                        );

CREATE TABLE batiment (id_village int,
                       id_bat SERIAL PRIMARY KEY, 
                       niveau int,
                       nom_bat varchar(255), 
                       id_ress int,
                       production int,
                       FOREIGN KEY(id_ress) REFERENCES ressource(id_ressource),
                       FOREIGN KEY(id_village) REFERENCES village(id_village)
                      );

CREATE TABLE cout_batiment (id_village int,
                            nom_bat varchar(255),
                            id_ressource int,
                            cout int,
                            niveau int,
                            FOREIGN KEY(id_village) REFERENCES village(id_village),
                            FOREIGN KEY(id_ress) REFERENCES ressource(id_ressource),
                            FOREIGN KEY(nom_bat) REFERENCES batiment(nom_bat),
                            FOREIGN KEY(niveau) REFERENCES batiment(niveau),
                            );


CREATE TABLE entrepot (id_village int, 
                       niveau int, 
                       FOREIGN KEY(id_village) REFERENCES village(id_village)
                      ); 
                      
CREATE Table stock( id_village int, 
                   FOREIGN KEY(id_village) REFERENCES village(id_village), 
                   id_ress int, 
                   FOREIGN KEY(id_ress) REFERENCES ressource(id_ressource), 
                   nb_ress int
                   );
