from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource
from firebase_admin import firestore

# Inicializa o Firestore
db = firestore.client()

api = Blueprint('api', __name__)
rest_api = Api(api)

class UserCheck(Resource):
    def get(self, username):
        try:
            # Verifica se o diretório do usuário existe no Firestore
            encomendas_ref = db.collection('encomendas').document(username)
            if encomendas_ref.get().exists:
                return jsonify({'exists': True})
            return jsonify({'exists': False, 'message': 'Usuário não encontrado!'}), 404
        except Exception as e:
            print(f"Erro ao verificar o usuário: {e}")
            return jsonify({'error': 'Erro ao acessar o Firestore'}), 500

rest_api.add_resource(UserCheck, '/check_user/<string:username>')

class Encomenda(Resource):
    def get(self, username):
        try:
            encomendas_ref = db.collection('encomendas').document(username).collection('encomendas')
            encomendas = [doc.to_dict() for doc in encomendas_ref.stream()]
            return jsonify(encomendas)
        except Exception as e:
            print(f"Erro ao obter encomendas para o usuário {username}: {e}")
            return jsonify({'error': 'Erro ao acessar as encomendas'}), 500

    def post(self, username):
        try:
            data = request.json
            encomendas_ref = db.collection('encomendas').document(username).collection('encomendas')
            encomenda_ref = encomendas_ref.add(data)
            return jsonify({'id': encomenda_ref.id, 'message': 'Encomenda criada com sucesso!'}), 201
        except Exception as e:
            print(f"Erro ao criar encomenda para o usuário {username}: {e}")
            return jsonify({'error': 'Erro ao criar a encomenda'}), 500

class EncomendaDetail(Resource):
    def get(self, username, id):
        try:
            encomenda_ref = db.collection('encomendas').document(username).collection('encomendas').document(id)
            encomenda = encomenda_ref.get()
            if encomenda.exists:
                return jsonify(encomenda.to_dict())
            return jsonify({'message': 'Encomenda não encontrada!'}), 404
        except Exception as e:
            print(f"Erro ao obter a encomenda {id} para o usuário {username}: {e}")
            return jsonify({'error': 'Erro ao acessar a encomenda'}), 500

    def put(self, username, id):
        try:
            encomenda_ref = db.collection('encomendas').document(username).collection('encomendas').document(id)
            data = request.json
            if encomenda_ref.get().exists:
                encomenda_ref.set(data)
                return jsonify({'message': 'Encomenda atualizada com sucesso!'})
            return jsonify({'message': 'Encomenda não encontrada!'}), 404
        except Exception as e:
            print(f"Erro ao atualizar a encomenda {id} para o usuário {username}: {e}")
            return jsonify({'error': 'Erro ao atualizar a encomenda'}), 500

    def delete(self, username, id):
        try:
            encomenda_ref = db.collection('encomendas').document(username).collection('encomendas').document(id)
            if encomenda_ref.get().exists:
                encomenda_ref.delete()
                return jsonify({'message': 'Encomenda excluída com sucesso!'})
            return jsonify({'message': 'Encomenda não encontrada!'}), 404
        except Exception as e:
            print(f"Erro ao excluir a encomenda {id} para o usuário {username}: {e}")
            return jsonify({'error': 'Erro ao excluir a encomenda'}), 500

# Adiciona os recursos à API
rest_api.add_resource(Encomenda, '/encomendas/<string:username>')
rest_api.add_resource(EncomendaDetail, '/encomendas/<string:username>/<string:id>')