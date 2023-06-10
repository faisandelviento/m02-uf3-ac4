# -*- coding: utf-8 -*-
"""
Created on February 2023

@author: Albert ETPX
"""

# Importación de módulos externos
import mysql.connector
from flask import Flask,render_template,request;

# Funciones de backend #############################################################################

# connectBD: conecta a la base de datos users en MySQL
def connectBD():
    db = mysql.connector.connect(
        host = "localhost",
        user = "root",
        passwd = "Princesa165",
        database = "users"
    )
    return db

# initBD: crea una tabla en la BD users, con un registro, si está vacía
def initBD():
    bd=connectBD()
    cursor=bd.cursor()
    
    # cursor.execute("DROP TABLE IF EXISTS users;")
    # Operación de creación de la tabla users (si no existe en BD)
    query="CREATE TABLE IF NOT EXISTS users(\
            user varchar(30) primary key,\
            password varchar(30),\
            name varchar(30), \
            surname1 varchar(30), \
            surname2 varchar(30), \
            age integer, \
            genre enum('H','D','NS/NC')); "
    cursor.execute(query)
            
    # Operación de inicialización de la tabla users (si está vacía)
    query="SELECT count(*) FROM users;"
    cursor.execute(query)
    count = cursor.fetchall()[0][0]
    if(count == 0):
        query = "INSERT INTO users \
            VALUES('user01','admin','Ramón','Sigüenza','López',35,'H');"
        cursor.execute(query)

    bd.commit()
    bd.close()
    return

# checkUser: comprueba si el par usuario-contraseña existe en la BD
def checkUser(user,password):
    bd=connectBD()
    cursor=bd.cursor()

    query=f"SELECT user,name,surname1,surname2,age,genre FROM users WHERE user=s%\
            AND password=s%"
    values= (user,password)
    print(query)
    cursor.execute(query,values)
    userData = cursor.fetchall()
    bd.close()
    
    if userData == []:
        return False
    else:
        return userData[0]

def UsuarioNoExiste(user):
    bd=connectBD()
    cursor=bd.cursor()
    query=f"SELECT user FROM users WHERE user=%s;"
    values= (user, )
    print(query)
    cursor.execute(query,values)
    userData = cursor.fetchall()
    bd.close()
    if userData == []:
        return True
    else:
        return False

# cresteUser: crea un nuevo usuario en la BD
def createUser(user,password,name,surname1,surname2,age,genre): ###Cristina
    ##comprobar usuario no esta en uso aun
    if(UsuarioNoExiste(user)):
        bd=connectBD()
        cursor=bd.cursor()
        ##insertar datos en BD
        query=f"INSERT INTO users VALUES (%s,%s,%s,%s,%s,%s,%s);"
        print(query)
        values= (user,password,name,surname1,surname2,age,genre)
        cursor.execute(query,values)
        ##commit para que los datos de la BD se actualicen antes de hacer siguiente consulta
        bd.commit() 

        #comprobamos que user existe en BD y seleccionamos los datos
        query2= f"SELECT user,name,surname1,surname2,age,genre FROM users WHERE user=%s"
        values2= (user, )
        cursor.execute(query2,values2)
        userData = cursor.fetchall()
        bd.close()
        if userData == []:
            return False #"El usuario no se ha podido registrar"
        else:
            return userData[0]
    else:
        return False #"este nombre de usuario ya existe"

# Secuencia principal: configuración de la aplicación web ##########################################
# Instanciación de la aplicación web Flask
app = Flask(__name__)

# Declaración de rutas de la aplicación web
@app.route("/")
def home():
    return render_template("home.html")

@app.route("/login")
def login():
    initBD()
    return render_template("login.html")

@app.route("/signin")
def signin():
    return render_template("signin.html")

@app.route("/newUser",methods=('GET', 'POST'))
def newUser():
    print("LLEGAMOS A NEW USER")
    if request.method == ('POST'):
        formData = request.form
        user=formData['user']
        password=formData['password']
        name=formData['name']
        surname1=formData['surname1']
        surname2=formData['surname2']
        age=formData['age']
        genre=formData['genre']
        userData = createUser(user,password,name,surname1,surname2,age,genre)

        if userData == False:
            return render_template("signinresults.html",login=False)
        else:
            return render_template("signinresults.html",login=True,userData=userData)

@app.route("/results",methods=('GET', 'POST'))
def results():
    if request.method == ('POST'):
        formData = request.form
        user=formData['usuario']
        password=formData['contrasena']
        userData = checkUser(user,password)

        if userData == False:
            return render_template("results.html",login=False)
        else:
            return render_template("results.html",login=True,userData=userData)
        
# Configuración y arranque de la aplicación web
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.run(host='localhost', port=5000, debug=True)