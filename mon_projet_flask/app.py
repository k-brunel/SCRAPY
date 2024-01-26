# from pymongo.mongo_client import MongoClient
# from pymongo.server_api import ServerApi
# from pymongo import MongoClient
# from flask import Flask, render_template, jsonify
# import random

# app = Flask(__name__)

# # URI de connexion
# uri = "mongodb+srv://kekerozyn:Testmongo@cluster0.u1qejnm.mongodb.net/?retryWrites=true&w=majority"
# # Create a new client and connect to the server
# client = MongoClient(uri, server_api=ServerApi('1'))
# # Send a ping to confirm a successful connection
# try:
#     client.admin.command('ping')
#     print("Pinged your deployment. You successfully connected to MongoDB!")
# except Exception as e:
#     print(e)


# # Connexion à la base de données
# client = MongoClient(uri)

# # Sélectionnez la base de données et la collection
# db = client['SCRAPY']
# collection = db['Citations']

# @app.route('/')
# def index():
#     count = collection.count_documents({})
#     random_index = random.randint(0, count - 1)
#     random_quote = collection.find().skip(random_index).limit(1).next()
#     return render_template('index.html', donnees=random_quote)

# @app.route('/refresh')
# def refresh_data():
#     count = collection.count_documents({})
#     random_index = random.randint(0, count - 1)
#     random_quote = collection.find().skip(random_index).limit(1).nexts()
#     return jsonify({
#         'auteur': random_quote['auteur'],
#         'citation': random_quote['citation']
#     })

# if __name__ == '__main__':
#     app.run(debug=True, port=5000)




from pymongo import MongoClient
from flask import Flask, render_template, jsonify
import random

app = Flask(__name__)
client = MongoClient('mongodb://localhost:27017/')
db = client['DB_SRAPY']  # Assurez-vous d'utiliser le même nom de base de données que dans votre pipeline Scrapy
collection = db['scrapy_citations']  # Remplacez par le nom de votre collection

@app.route('/')
def index():
    count = collection.count_documents({})
    random_index = random.randint(0, count - 1)
    random_quote = collection.find().skip(random_index).limit(1).next()
    return render_template('index.html', donnees=random_quote)
if __name__ == '__main__':
    app.run(debug=True)


@app.route('/refresh')
def refresh_data():
    count = collection.count_documents({})
    random_index = random.randint(0, count - 1)
    random_quote = collection.find().skip(random_index).limit(1).next()
    return jsonify({
        'auteur': random_quote['auteur'],
        'citation': random_quote['citation']
    })

if __name__ == '__main__':
    app.run(debug=True)


# WITH DATA FROM JSON FILE
# from flask import Flask, render_template, jsonify
# import random
# import json

# app = Flask(__name__)

# # Charger les données depuis le fichier JSON en spécifiant l'encodage
# with open('output.json', 'r', encoding='utf-8') as json_file:
#     data = json.load(json_file)

# @app.route('/')
# def index():
#     # Utiliser les données chargées depuis le fichier JSON
#     count = len(data)
#     random_index = random.randint(0, count - 1)
#     random_quote = data[random_index]
#     return render_template('index.html', donnees=random_quote)

# @app.route('/refresh')
# def refresh_data():
#     # Utiliser les données chargées depuis le fichier JSON
#     count = len(data)
#     random_index = random.randint(0, count - 1)
#     random_quote = data[random_index]
#     return jsonify({
#         'auteur': random_quote['auteur'],
#         'citation': random_quote['citation']
#     })

# if __name__ == '__main__':
#     app.run(debug=True)
