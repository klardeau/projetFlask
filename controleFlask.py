from flask import Flask, render_template, request, redirect, url_for
#from flask_mysql_connector import MySQL
from flaskext.mysql import MySQL##aucasou
import bcrypt
#import mysql.connector
#from flask_mysqldb import MySQL


app = Flask(__name__)

"""
@app.route('/')
def hello_world():
    return 'Hello, World!'
    #http://127.0.0.1:5000/
"""
#CTRL F5 reinitialise page css web.. parfait

app.secret_key="hello"

app.config['MYSQL_DATABASE_HOST']='127.0.0.1'
app.config['MYSQL_DATABASE_USER']='root'
app.config['MYSQL_DATABASE_PASSWORD']='root'
app.config['MYSQL_DATABASE_DB']='bdVocab'

mysql = MySQL(app)

@app.route('/')
def Home():
    return render_template('index.html')#http://127.0.0.1:5000/



#Permet de se connecter à sa session
@app.route('/', methods=['GET','POST'])
def Autentification():
	if request.method=='POST':
		username = request.form['user']
		password = request.form['pass']
		hashed = bcrypt.hashpw(b'password', bcrypt.gensalt())
		cursor = mysql.connect().cursor()
		cursor.execute('SELECT * FROM Utilisateur WHERE pseudo = %s AND password = %s', (username, hashed))
		data = cursor.fetchone()
		cursor.close()
		if data is None:
			return "Username or Password is wrong ! "
		else:
			return render_template('Home.html')#Home.html

#permet d'établir un lien entre index et nvUtil (creation d'un utilisateur)
@app.route('/nvUtil')
def nvUtil():
	return render_template('nvUtil.html')

#creation d'un utilisateur
@app.route('/nvUtil',methods=['GET','POST'])
def creationUtilisateur():
	if request.method=='POST':
		username = request.form['user']
		password = request.form['pass']
		passwordV=request.form['pass2']
		if password==passwordV:
			hashed=bcrypt.hashpw(b'password', bcrypt.gensalt())
			connection=mysql.connect()#important de garder la connexion sinon il ne commit pas la requete du cursor
			cursor = connection.cursor()
			cursor.execute("INSERT INTO Utilisateur (pseudo, password) VALUES(%s,%s)", (username, hashed))
			#cursor.execute("INSERT INTO Utilisateur (pseudo, password) VALUES('billie','test')")#test ajout
			#mysql.connection.commit()
			connection.commit()
			cursor.close()
			return redirect(url_for('successAjout'))
		return redirect(url_for('errorAjout'))
	return redirect(url_for('errorAjout'))


@app.route('/successAjout')
def successAjout():
	return '<h1>Ajout éffectué ! <a href="/">index</a></h1>'

@app.route('/errorAjout')
def errorAjout():
	return '<h1>Problème lors de l\'ajout, cause possible: manque de caractère <a href="/">nvlUtil</a></h1>'

""" voir les users dans 127.0.0.1/users"""
@app.route('/users')
def users():
	cur=mysql.connect().cursor()
	resultValue=cur.execute("SELECT * FROM Utilisateur")
	if resultValue>0:
		userDetails=cur.fetchall()
		return render_template('users.html',userDetails=userDetails)



if __name__=="__main__":
    app.run(debug=True)