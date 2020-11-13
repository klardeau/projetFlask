<!DOCTYPE html>
<html>
<head>
	<title>Login Page</title>
	<link href="../static/style.css" rel="stylesheet" type="text/css"/>
</head>
<header>
<!--problème php à réglé avec flask. include plus simple-->
<ul id="menu-deroulant">
	<li><a href="{{ url_for('Home')}}">Accueil</a>
	</li>
	<li><a href="./?action=xmlConvert">Passer un test</a></li>
	<li><a>Carnet</a>
		<ul>
			<li><a href="./?action=ajouterQuestionnaire">Ajouter</a></li>
			<li><a href="./?action=ajouterQuestion">Supprimer</a></li>
		</ul>
	</li>
	<li><a>Liste d'un carnet</a>
		<ul>
			<li><a href="./?action=modifierQuestionnaire">Ajouter</a></li>
			<li><a href="./?action=modifierQuestion">Supprimer</a></li>
		</ul>
	</li>
	<li><a>Mot Anglais et Français d'une liste</a>
		<ul>
			<li><a href="./?action=supprimerQuestionnaire">Ajouter</a></li>
			<li><a href="./?action=supprimerQuestion">Supprimer</a></li>
		</ul>
	</li>
	
</ul>		
			
		

</header>
<body>
	<div>
		<form action="/" method="POST">
			<p>
				<label>billie</label>
				<input type="text" id="user" name="user"/>
			</p>
			<p>
				<input type="submit" text="Se connecter"/>
			</p>
		</form>
	</div>	
</body>
</html>