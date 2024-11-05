from app import create_app
import firebase_admin
from firebase_admin import credentials

# Inicializa o Firebase Admin SDK
cred = credentials.Certificate('./cedentials.json')
firebase_admin.initialize_app(cred)

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)