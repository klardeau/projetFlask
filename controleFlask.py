from flask import Flask, render_template, request, redirect, url_for
#from flask_mysql_connector import MySQL
from flaskext.mysql import MySQL##aucasou
#import bcrypt
import datetime
import uuid
from random import *


app = Flask(__name__)

"""
@app.route('/')
def hello_world():
    return 'Hello, World!'
    #http://127.0.0.1:5000/
"""
#CTRL F5 reinitialise page css web.. parfait
#s
app.secret_key="hello"
#connect to database
app.config['MYSQL_DATABASE_HOST']='127.0.0.1'
app.config['MYSQL_DATABASE_USER']='root'
app.config['MYSQL_DATABASE_PASSWORD']='root'
app.config['MYSQL_DATABASE_DB']='bdVocab'

mysql = MySQL(app)

#la creation de cette objet surprenant permet en réalité de faire voyager l'username(qui est unique) afin de le relier à la creation des tables carnets posseder 
class user:
	def __init__(self, username):
		self.username=username

	def get_username(self):
		return self.username

	def set_username(self,username):
		self.username=username

user=user('root')

@app.route('/')
def Home():
    return render_template('index.html')#http://127.0.0.1:5000/





#Permet de se connecter à sa session-------------------------------------------------------------------------------
@app.route('/', methods=['GET','POST'])
def Autentification():
	try:
		if request.method=='POST':
			username = request.form['user']
			password = request.form['pass']
			cursor = mysql.connect().cursor()
			cursor.execute('SELECT * FROM Utilisateur WHERE pseudo = %s AND password = %s', (username, password))
			data = cursor.fetchone()
			cursor.close()
			if data is None:
				return "Username or Password is wrong ! "
			else:
				username=request.form['user']
				user.set_username(username)
				return render_template('Home.html', username=user.get_username())#Home.html
	except:
		return '<h1> Erreur connection à la base de donnée <a href="/">index</a></h1>'



#permet d'établir un lien entre index et nvUtil (creation d'un utilisateur)
#Les chemins vers les html
@app.route('/nvUtil')
def nvUtil():
	return render_template('nvUtil.html')#TEST ICI DANS TT LES RENDER TEMPLATE AJOUTER USERNAME

@app.route('/Home')
def HomeCo():
	return render_template('Home.html', username=user.get_username())

@app.route('/addCarnet')
def addCarnet():
	return render_template('addCarnet.html', username=user.get_username())


#creation d'un utilisateur-----------------------------------------------------------------------------------------
@app.route('/nvUtil',methods=['GET','POST'])
def creationUtilisateur():
	if request.method=='POST':
		username = request.form['user']
		password = request.form['pass']
		passwordV=request.form['pass2']
		if password==passwordV:#on verifie qu'il est validé son mdp avec le deuxième
			try:
				connection=mysql.connect()#important de garder la connexion sinon il ne commit pas la requete du cursor
				cursor = connection.cursor()
				try:
					cursor.execute("INSERT INTO Utilisateur (pseudo, password) VALUES(%s,%s)", (username, password))
					connection.commit()
					cursor.close()
					return redirect(url_for('successAjout'))
				except:
					cursor.close()
					return '<h1> Username deja pris <a href="/">nvlUtil</a></h1>'
			except:
				return'<h1> Erreur lors de l\'accés à la base de donnée <a href="/">nvlUtil</a></h1>'
		return '<h1> Erreur les mots de passe écrit ne sont pas pareil <a href="/">nvlUtil</a></h1>'
	return redirect(url_for('errorAjout'))


@app.route('/successAjout')
def successAjout():
	return '<h1>Ajout éffectué ! <a href="/">index</a></h1>'

@app.route('/errorAjout')
def errorAjout():
	return '<h1>Problème lors de l\'ajout, cause possible: mot de passe incorecte, pseudo deja existant, pas d\'accès à la bdd <a href="/">nvlUtil</a></h1>'

""" voir les users dans 127.0.0.1/users"""
@app.route('/users')
def users():
	cur=mysql.connect().cursor()
	resultValue=cur.execute("SELECT * FROM Utilisateur")
	if resultValue>0:
		userDetails=cur.fetchall()
		return render_template('users.html',userDetails=userDetails)


#ajoutd'un carnet et du lien posseder entre utilisateur et lui
@app.route('/addCarnet',methods=['GET','POST'])
def ajouteCarnet():
	if request.method=='POST':
		nomCarnet = request.form['nomCarnet']
		numCarnet = uuid.uuid4()
		dateCreation = datetime.datetime.now()
		username = user.get_username()
		try:
			connection=mysql.connect()#important de garder la connexion sinon il ne commit pas la requete du cursor
			cursor = connection.cursor()
			try:
				cursor.execute("INSERT INTO Carnet (numCarnet, nom, dateCreation) VALUES(%s,%s,%s)", (str(numCarnet), nomCarnet,dateCreation))
				connection.commit()
				cursor.execute("INSERT INTO Posseder (pseudo, numCarnet) VALUES(%s,%s)", (username, str(numCarnet)))
				connection.commit()
				cursor.close()
				return redirect(url_for('successAjoutCarnet'))
			except:
				return '<h1> Erreur lors de l\'ajout <a href="/addCarnet">addCarnet</a></h1>'
		except:
			cursor.close()
			return'<h1> Erreur lors de l\'accés à la base de donnée <a href="/addCarnet">addCarnet</a></h1>'
		
	return redirect(url_for('errorAjoutCarnet'))

@app.route('/errorAjoutCarnet')
def errorAjoutCarnet():
	return '<h1>Erreur lors de l\'jout d\'un carnet <a href="/addCarnet">addCarnet</a></h1>'

@app.route('/successAjoutCarnet')
def successAjoutCarnet():
	return '<h1>Ajout éffectué ! <a href="/addCarnet">addCarnet</a></h1>'

#fin partit ajoutCarnet


#partit deleteCarnet------------------------------------------------------------------------------------------
@app.route('/deleteCarnet')
def deleteCarnet():
	cur=mysql.connect().cursor()
	resultValue=cur.execute("SELECT * FROM Carnet inner join Posseder on Carnet.numCarnet=Posseder.numCarnet where Posseder.pseudo=%s", (user.get_username()))
	if resultValue>0:
		carnetDetails=cur.fetchall()
		return render_template('deleteCarnet.html',carnetDetails=carnetDetails)
	else: return '<h1>Vous n\'avez pas de carnet, lien vers la création d\'un carnet <a href="/addCarnet">addCarnet</a></h1>'


@app.route('/deleteCarnet',methods=['GET','POST'])
def suppressionCarnet():
	if request.method=='POST':
		numCarnet=request.form['numCarnet']
		
		try:
			connection=mysql.connect()#important de garder la connexion sinon il ne commit pas la requete du cursor
			cursor = connection.cursor()
			try:
				cursor.execute("DELETE from Posseder where numCarnet = %s", (numCarnet))
				connection.commit()
				resultFr=cursor.execute("SELECT * from VocaFrancais inner join Avoir on VocaFrancais.numMF=Avoir.numMF inner join Liste on Avoir.numListe=Liste.numListe inner join Carnet on Liste.numCarnet=Carnet.numCarnet where Carnet.numCarnet = %s", (numCarnet))
				if resultFr>0:
					frenchId=cursor.fetchall()
				resultAn=cursor.execute("SELECT * from VocaAnglais inner join Avoir on VocaAnglais.numMA=Avoir.numMA inner join Liste on Avoir.numListe=Liste.numListe inner join Carnet on Liste.numCarnet=Carnet.numCarnet where Carnet.numCarnet = %s", (numCarnet))
				if resultAn>0:
					englishId=cursor.fetchall()
				resultAvoir=cursor.execute("SELECT * from Avoir inner join Liste on Avoir.numListe=Liste.numListe inner join Carnet on Liste.numCarnet=Carnet.numCarnet where Carnet.numCarnet = %s", (numCarnet))
				if resultAvoir>0:
					cursor.execute("DELETE from Avoir inner join Liste on Avoir.numListe=Liste.numListe inner join Carnet on Liste.numCarnet=Carnet.numCarnet where Carnet.numCarnet = %s", (numCarnet))
					connection.commit()
				if resultFr>0:
					for rowF in frenchId:
						cursor.execute("DELETE from VocaFrancais where numMF=%s",(rowF[0]))
						connection.commit()
				if resultAn>0:
					for rowA in englishId:
						cursor.execute("DELETE from VocaAnglais where numMA=%s",(rowA[0]))
						connection.commit()
				resultListe=cursor.execute("SELECT * from Liste inner join Carnet on Liste.numCarnet=Carnet.numCarnet where Carnet.numCarnet = %s", (numCarnet))
				if resultListe>0:
					cursor.execute("DELETE from Liste inner join Carnet on Liste.numCarnet=Carnet.numCarnet where Carnet.numCarnet = %s", (numCarnet))
					connection.commit()
				cursor.execute("DELETE from Carnet where numCarnet=%s", (numCarnet))
				connection.commit()
				cursor.close()
				return redirect(url_for('successDeleteCarnet'))#La fonction fonctionne MAIS afficher errorDeleteCarnet :()
			except:
				cursor.close()
				return redirect(url_for('errorDeleteCarnet'))
		except:
			return'<h1> Erreur lors de l\'accés à la base de donnée <a href="/deleteCarnet">deleteCarnet</a></h1>'


@app.route('/errorDeleteCarnet')
def errorDeleteCarnet():
	return '<h1>Erreur lors de la suppression d\'un carnet <a href="/deleteCarnet">deleteCarnet</a></h1>'

@app.route('/successDeleteCarnet')
def successDeleteCarnet():
	return '<h1>Suppression éffectué ! <a href="/deleteCarnet">deleteCarnet</a></h1>'
#fin partit deleteCarnet


#partit ajout LISTE----------------------------------------------------------------------------------------------

@app.route('/addListe')
def addListe():
	cur=mysql.connect().cursor()
	resultValue=cur.execute("SELECT * FROM Carnet inner join Posseder on Carnet.numCarnet=Posseder.numCarnet where Posseder.pseudo=%s", (user.get_username()))
	if resultValue>0:
		carnetDetails=cur.fetchall()
		cur.close()
		return render_template('addListe.html',carnetDetails=carnetDetails)
	else: return '<h1>Vous n\'avez pas de carnet, lien vers la création d\'un carnet <a href="/addCarnet">addCarnet</a></h1>'

'''
@app.route('/addListe',methods=['GET','POST'])
def btnEnvoieSurAjouterListe():
	if request.method=='POST':
		return render_template('ajouterListe.html',numCarnet=request.form['numCarnet'])'''
		#return redirect(url_for('ajouterListe',numCarnet=request.form['numCarnet']))

@app.route('/addListe',methods=['GET','POST'])
def ajouterListeDansBDD():
	if request.method=='POST':
		numCarnet=request.form['numCarnet']
		commentaire=request.form['commentaire']
		nom=request.form['nomListe']
		
		dateCreation = datetime.datetime.now()
		numListe=uuid.uuid4()
		#try:
		connection=mysql.connect()#important de garder la connexion sinon il ne commit pas la requete du cursor
		cursor = connection.cursor()
			#try:
		cursor.execute("INSERT INTO Liste (numListe, nom, dateCreation, commentaire, numCarnet) VALUES(%s,%s,%s,%s,%s)", (str(numListe), nom, dateCreation,commentaire, numCarnet))
		connection.commit()
		cursor.close()
		return '<h1> Succés lors de l\'ajout <a href="/addListe">addListe</a></h1>'
			#except:
				#return '<h1> Erreur lors de l\'ajout <a href="/addListe">addListe</a></h1>'
		#except:
			#cursor.close()
			#return'<h1> Erreur lors de l\'accés à la base de donnée <a href="/addListe">addListe</a></h1>'


#fin partit ajout LISTE



#affListe----------------------------------------------------------------------------------------------------
@app.route('/affListe')
def affListe():
	cur=mysql.connect().cursor()
	resultValue=cur.execute("SELECT Carnet.nom, Liste.nom, Liste.commentaire, Liste.dateCreation FROM Liste inner join Carnet on Liste.numCarnet=Carnet.numCarnet inner join Posseder on Carnet.numCarnet=Posseder.numCarnet WHERE Posseder.pseudo=%s Order by Carnet.nom", (user.get_username()))
	if resultValue>0:
		userDetails=cur.fetchall()
		return render_template('affListe.html',userDetails=userDetails)
	return '<h1> Erreur avez-vous bien créer une Liste et un Carnet avant? <a href="/addListe">addListe</a></h1>'

#finaffliste

#delete Liste--------------------------------------------------------------------------------------------------------------------------------------------------------------------------
@app.route('/deleteListe')
def deleteListe():
	
	cur=mysql.connect().cursor()
	resultValue=cur.execute("SELECT Carnet.nom, Liste.numListe, Liste.nom, Liste.commentaire, Liste.dateCreation FROM Liste inner join Carnet on Liste.numCarnet=Carnet.numCarnet inner join Posseder on Carnet.numCarnet=Posseder.numCarnet WHERE Posseder.pseudo=%s Order by Carnet.nom", (user.get_username()))
	if resultValue>0:
		listeDetails=cur.fetchall()
		return render_template('deleteListe.html',listeDetails=listeDetails)
	else: return '<h1>Vous n\'avez pas de liste, lien vers la création d\'un carnet <a href="/addListe">addListe</a></h1>'


@app.route('/deleteListe',methods=['GET','POST'])
def suppressionListe():
	if request.method=='POST':
		numListe=request.form['numListe']
		try:
			connection=mysql.connect()#important de garder la connexion sinon il ne commit pas la requete du cursor, il y'a un ordre avant de delete une liste
			cursor = connection.cursor()
			try:
				resultFr=cursor.execute("SELECT * from VocaFrancais inner join Avoir on VocaFrancais.numMF=Avoir.numMF where Avoir.numListe = %s", (numListe))
				if resultFr>0:
					frenchId=cursor.fetchall()
				resultAn=cursor.execute("SELECT * from VocaAnglais inner join Avoir on VocaAnglais.numMA=Avoir.numMA where  Avoir.numListe = %s", (numListe))
				if resultAn>0:
					englishId=cursor.fetchall()
				resultAvoir=cursor.execute("SELECT * from Avoir where Avoir.numListe = %s", (numListe))
				if resultAvoir>0:
					cursor.execute("DELETE from Avoir where Avoir.numListe = %s", (numListe))
					connection.commit()
				if resultFr>0:
					for rowF in frenchId:
						cursor.execute("DELETE from VocaFrancais where numMF=%s",(rowF[0]))
						connection.commit()
				if resultAn>0:
					for rowA in englishId:
						cursor.execute("DELETE from VocaAnglais where numMA=%s",(rowA[0]))
						connection.commit()
				cursor.execute("DELETE from Liste where numListe=%s", (numListe))
				connection.commit()
				cursor.close()
				return redirect(url_for('successDeleteListe'))
			except:
				cursor.close()
				return redirect(url_for('errorDeleteListe'))
		except:
			return'<h1> Erreur lors de l\'accés à la base de donnée <a href="/deleteListe">deleteListe</a></h1>'

@app.route('/errorDeleteListe')
def errorDeleteListe():
	return '<h1>Erreur lors de la suppression d\'une liste <a href="/deleteListe">deleteListe</a></h1>'

@app.route('/successDeleteListe')
def successDeleteListe():
	return '<h1>Suppression éffectué ! <a href="/deleteListe">deleteListe</a></h1>'
#fin delete Liste

#AjouterMotAnglaisETFrancais-------------------------------------------------------------------------------------------------------------------------------------------------------------------------
@app.route('/addMotAF')
def addMotAF():
	cur=mysql.connect().cursor()
	resultValue=cur.execute("SELECT Liste.numListe, Carnet.nom, Liste.nom, Liste.commentaire, Liste.dateCreation FROM Liste inner join Carnet on Liste.numCarnet=Carnet.numCarnet inner join Posseder on Carnet.numCarnet=Posseder.numCarnet WHERE Posseder.pseudo=%s Order by Carnet.nom", (user.get_username()))
	if resultValue>0:
		listeDetails=cur.fetchall()
		cur.close()
		return render_template('addMotAF.html',listeDetails=listeDetails)
	else: return '<h1>Vous n\'avez pas de liste, lien vers la création d\'une liste <a href="/addListe">addListe</a></h1>'


@app.route('/addMotAF',methods=['GET','POST'])
def ajouterMotAF():#il faut ajouter le lien Avoir après les mots Anglais et Français
	if request.method=='POST':
		numListe=request.form['numListe']
		lblFr=request.form['lblFr']
		lblAn=request.form['lblAn']
		
		numFrAn=uuid.uuid4()#l'un n'est rien sans l'autre donc autant mettre le meme id cela servira plus tard pour retrouver les deux avec 1 seul des deux id
		try:
			connection=mysql.connect()#important de garder la connexion sinon il ne commit pas la requete du cursor
			cursor = connection.cursor()
			try:
				cursor.execute("INSERT INTO VocaAnglais (numMA, libelle) VALUES(%s,%s)", (str(numFrAn), lblAn))
				connection.commit()
				cursor.execute("INSERT INTO VocaFrancais (numMF, libelle) VALUES(%s,%s)", (str(numFrAn), lblFr))
				connection.commit()
				cursor.execute("INSERT INTO Avoir (numMA, numMF, numListe) VALUES(%s,%s,%s)", (str(numFrAn), str(numFrAn), numListe))#la table Avoir pour relier les deux mots mais SURTOUT les mettres dans la liste
				connection.commit()
				cursor.close()
				return '<h1> Succés lors de l\'ajout <a href="/addMotAF">addMotAF</a></h1>'
			except: '<h1> Erreur lors de l\'ajout <a href="/addMotAF">addMotAF</a></h1>'
		except: return '<h1> Erreur de connexion à la base de donnée <a href="/addMotAF">addMotAF</a></h1>'
#FinAjout

#delete mot-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
@app.route('/deleteMotAF')
def deleteMotAF():
	cur=mysql.connect().cursor()
	resultValue=cur.execute("SELECT VocaFrancais.numMF, VocaFrancais.libelle, VocaAnglais.libelle, Liste.nom FROM VocaFrancais inner join Avoir on VocaFrancais.numMF=Avoir.numMF inner join Liste on Avoir.numListe=Liste.numListe inner join Carnet on Liste.numCarnet=Carnet.numCarnet inner join Posseder on Carnet.numCarnet=Posseder.numCarnet inner join VocaAnglais on Avoir.numMA=VocaAnglais.numMA WHERE Posseder.pseudo=%s Order by Liste.nom", (user.get_username()))
	if resultValue>0:
		motDetails=cur.fetchall()
		return render_template('deleteMotAF.html',motDetails=motDetails)
	else: return '<h1>Vous n\'avez pas de Mot, lien vers la création de mots <a href="/addMotAF">addMotAF</a></h1>'


@app.route('/deleteMotAF',methods=['GET','POST'])
def suppressionMotAF():
	if request.method=='POST':
		numAF=request.form['numMotAF']
		try:
			connection=mysql.connect()#important de garder la connexion sinon il ne commit pas la requete du cursor
			cursor = connection.cursor()
			try:
				cursor.execute("DELETE from Avoir where Avoir.numMF = %s", (numAF))#on delete Avoir le lien avant les voca Fr et An
				connection.commit()
				cursor.execute("DELETE from VocaFrancais where numMF=%s",(numAF))
				connection.commit()
				cursor.execute("DELETE from VocaAnglais where numMA=%s",(numAF))
				connection.commit()
				cursor.close()
				return redirect(url_for('successDeleteMots'))
			except:
				cursor.close()
				return redirect(url_for('errorDeleteMots'))
		except:
			return'<h1> Erreur lors de l\'accés à la base de donnée <a href="/deleteMotAF">deleteMotAF</a></h1>'

@app.route('/errorDeleteMots')
def errorDeleteMots():
	return '<h1>Erreur lors de la suppression d\'un mot <a href="/deleteMotAF">deleteMotAF</a></h1>'

@app.route('/successDeleteMots')
def successDeleteMots():
	return '<h1>Suppression éffectué ! <a href="/deleteMotAF">deleteMotAF</a></h1>'
#delete mot

#Reviser mot liste---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
@app.route('/reviserMotAF')
def reviserMotAF():
	cur=mysql.connect().cursor()
	resultValue=cur.execute("SELECT * FROM Liste inner join Carnet on Liste.numCarnet=Carnet.numCarnet inner join Posseder on Carnet.numCarnet=Posseder.numCarnet WHERE Posseder.pseudo=%s", (user.get_username()))
	if resultValue>0:
		listeDetails=cur.fetchall()
		return render_template('reviserMotAF.html',listeDetails=listeDetails)
	else: return '<h1>Vous n\'avez pas de Mot, lien vers la création de mots <a href="/addMotAF">addMotAF</a></h1>'


@app.route('/reviserMotAF',methods=['GET','POST'])
def revisionsMotAF():
	if request.method=='POST':
		numListe=request.form['numListe']
		cur=mysql.connect().cursor()
		resultValue=cur.execute("SELECT VocaAnglais.libelle, VocaFrancais.libelle FROM VocaAnglais inner join Avoir on VocaAnglais.numMA=Avoir.numMA inner join VocaFrancais on Avoir.numMF=VocaFrancais.numMF WHERE Avoir.numListe=%s", (numListe))
		if resultValue>0:
			affMot=cur.fetchall()
			return render_template('afficherMotAF.html',affMot=affMot)
		else: return '<h1>Vous n\'avez pas de Mot, lien vers la création de mots <a href="/addMotAF">addMotAF</a></h1>'
#fin reviser mot liste


#passer test random

class test:#permet de créer un objet test qui sera innitialisé à chaque fois qu'on entre dans passer test
	def __init__(self, numFRAN, libFr, libAn):
		self.numFRAN=numFRAN
		self.libFr=libFr
		self.libAn=libAn

	def get_numFRAN(self):
		return self.numFRAN

	def get_libFr(self):
		return self.libFr

	def get_libAn(self):
		return self.libAn

	def set_numFRAN(self,numFRAN):
		self.numFRAN=numFRAN

	def set_libFr(self,libFr):
		self.libFr=libFr

	def set_libAn(self,libAn):
		self.libAn=libAn

test=test('num','fr','an')
@app.route('/passerTest')
def passerTest():
	cur=mysql.connect().cursor()
	resultValue=cur.execute("SELECT VocaFrancais.numMF, VocaFrancais.libelle, VocaAnglais.libelle FROM VocaFrancais inner join Avoir on VocaFrancais.numMF=Avoir.numMF inner join Liste on Avoir.numListe=Liste.numListe inner join Carnet on Liste.numCarnet=Carnet.numCarnet inner join Posseder on Carnet.numCarnet=Posseder.numCarnet inner join VocaAnglais on Avoir.numMA=VocaAnglais.numMA WHERE Posseder.pseudo=%s", (user.get_username()))
	if resultValue>0:
		i=0
		listeDetails=cur.fetchall()
		for result in listeDetails:
			i+=1
		n=randint(1,i)#je mets un voca aux hasards
		j=0
		for result in listeDetails:
			j+=1
			if n==j:
				test.set_numFRAN(result[0])
				test.set_libFr(result[1])
				test.set_libAn(result[2])
		return render_template('passerTest.html',test=test)
	else: return '<h1>Vous n\'avez pas de Mot, lien vers la création de mots <a href="/addMotAF">addMotAF</a></h1>'




@app.route('/passerTest',methods=['GET','POST'])
def passationDeTest():
	if request.method=='POST':
		lblAn=request.form['lblAn']
		if lblAn==test.get_libAn():#vérifie le resultat inscris et la bonne réponse
			return '<h1> Bien joué ! vous avez la bonne réponse. <a href="/passerTest">passerTest</a></h1>'
		return '<h1> FAUX la bonne réponse est {{'+test.get_libAn()+'}} <a href="/passerTest">passerTest</a></h1>'
#fin passer test
if __name__=="__main__":
    app.run(debug=True)