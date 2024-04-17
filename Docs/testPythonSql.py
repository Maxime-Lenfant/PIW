# coding: utf-8

import psycopg2

# Pensez a adapter les parametre ci-dessous à votre environnement
# Votre base de donnee doit etre creer avant de lancer ce script
con = psycopg2.connect(host='ipaddress_to_psql', user='psql__user', password='psql_password', dbname='psql_db_name')


def build_select_login(user: str, pswd: str) -> (str, dict):
    sql: str = "SELECT login FROM users WHERE login = %(user)s AND pssword = %(pswd)s"
    fdata: dict = {
        "user": user,
        "pswd": pswd,
    }
    return sql, fdata


def execute_sql(sql: str, fdata: dict):
    cr = con.cursor()
    res = cr.execute(sql, fdata)
    return res

def login(user: str, pswd: str) -> bool:
    sql, fdata = build_select_login(user, pswd)
    res = execute_sql(sql, fdata)
    if res == None:
        return False
    return True


print(login("toto", "toto"))

"""
CREATE TABLE users (
  name VARCHAR(30),
  first_name VARCHAR(30),
  login VARCHAR(30) PRIMARY KEY,
  pssword VARCHAR(30)
);
"""

print("Si ce message apparait, votre environnement postgresql + python est pret ^^)")