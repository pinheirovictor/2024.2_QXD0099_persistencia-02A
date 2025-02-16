import firebase_admin
from firebase_admin import credentials, firestore

# Carregar credenciais JSON do Firebase (baixe no Firebase Console)
cred = credentials.Certificate("persistence-aula-firebase-adminsdk-fbsvc-d5a2a80c7e.json")
firebase_admin.initialize_app(cred)

# Inicializa o Firestore
db = firestore.client()
