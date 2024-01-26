[Lien vers l'application ](http://kerozyn.pythonanywhere.com/)

# SCRAPY
Ce projet utilise Scrapy pour extraire des citations et leurs auteurs du site "https://quotes.toscrape.com/". 
Les données extraites sont ensuite stockées dans une base de données MongoDB à l'aide d'un pipeline personnalisé. 
Un serveur web Flask est utilisé pour afficher aléatoirement les citations stockées dans la base de données.

Fonctionnalités
Extraction de données : Utilisation de Scrapy pour extraire des citations et des informations sur les auteurs.
Stockage des données : Les citations extraites sont stockées dans MongoDB, permettant une récupération et une gestion efficaces.
Affichage Web : Un serveur Flask affiche aléatoirement les citations stockées, avec une fonctionnalité de rafraîchissement pour obtenir une nouvelle citation sans recharger la page.
Installation
Assurez-vous d'avoir Python et MongoDB installés sur votre système. Ensuite, suivez ces étapes pour configurer le projet :

Clonez ce dépôt :
bash
Copy code
git clone https://github.com/k-brunel/SCRAPY.git
Installez les dépendances nécessaires :
Copy code
pip install -r requirements.txt
Assurez-vous que MongoDB est en cours d'exécution sur votre système.
Utilisation
Exécution du Spider Scrapy
Lancez le spider Scrapy pour commencer à extraire des citations :

bash
Copy code
cd chemin/vers/le/spider
scrapy crawl jobs

# FLASK
Lancement du Serveur Flask
Pour démarrer le serveur Flask et afficher les citations :

bash
Copy code
cd chemin/vers/le/serveur/flask
flask run
Accédez à http://127.0.0.1:5000/ dans votre navigateur pour voir une citation aléatoire. Utilisez le bouton "New quote" pour charger une nouvelle citation sans recharger la page.

Configuration
Scrapy: Le spider est défini dans spider.py. Modifiez les URLs ou les sélecteurs XPath/CSS selon vos besoins.
MongoDB: Le pipeline MongoDB est configuré dans pipelines.py. Adaptez les paramètres de connexion à votre configuration MongoDB.
Flask: Le serveur Flask est défini dans app.py. Ajustez les routes ou le port selon vos préférences.


