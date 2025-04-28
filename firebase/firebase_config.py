import firebase_admin
from firebase_admin import credentials, db
import os

# Ruta al archivo JSON de la clave
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
cred_path = os.path.join(BASE_DIR, 'firebase', 'serviceAccountKey.json')

# Inicializar Firebase si aún no está inicializado
if not firebase_admin._apps:
    cred = credentials.Certificate(cred_path)
    firebase_admin.initialize_app(cred, {
        'https://appproductos-9ead1-default-rtdb.firebaseio.com/'
    })