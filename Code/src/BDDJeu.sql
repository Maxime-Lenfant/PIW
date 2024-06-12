CREATE TABLE utilisateur(id SERIAL PRIMARY KEY,
                        login TEXT UNIQUE NOT NULL CHECK (login != ''),
                        password TEXT NOT NULL CHECK (password != ''),
                        token TEXT
                        );

CREATE TABLE village(id_village SERIAL PRIMARY KEY, 
                    id_user int,
                    nom_village varchar(255),
                    FOREIGN KEY(id_user) REFERENCES utilisateur(id)
                    );

CREATE TABLE ressource (id_ressource SERIAL PRIMARY KEY, 
                        nom VARCHAR(255)
                        );

CREATE TABLE liste_batiment (
                       nom_bat varchar(255), 
                       id_ress int,
                       PRIMARY KEY (nom_bat),
                       FOREIGN KEY(id_ress) REFERENCES ressource(id_ressource)
                      );

CREATE TABLE cout_batiment (nom_bat varchar(255),
                            id_ress int,
                            cout int,
                            niveau int,
                            FOREIGN KEY(id_ress) REFERENCES ressource(id_ressource),
                            FOREIGN KEY(nom_bat) REFERENCES liste_batiment(nom_bat)
                            );

CREATE TABLE batiment (id_village int,
                       niveau int,
                       nom_bat varchar(255), 
                       id_ress int,
                       production int,
                       PRIMARY KEY (id_village, nom_bat),
                       FOREIGN KEY(id_ress) REFERENCES ressource(id_ressource),
                       FOREIGN KEY(id_village) REFERENCES village(id_village),
                       FOREIGN KEY(nom_bat) REFERENCES liste_batiment(nom_bat)
                      );

CREATE TABLE entrepot (id_village int, 
                       niveau int, 
                       FOREIGN KEY(id_village) REFERENCES village(id_village)
                      ); 
                      
CREATE Table stock( id_village int, 
                   FOREIGN KEY(id_village) REFERENCES village(id_village), 
                   id_ress int, 
                   FOREIGN KEY(id_ress) REFERENCES ressource(id_ressource), 
                   nb_ress int,
                   nb_max int
                   );
