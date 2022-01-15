import json

import mysql.connector
from flask import Flask, Response, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:055109711@localhost/modelo_celular'

db = SQLAlchemy(app)


class Celular(db.Model):
    """
    Para a criação da tabelo no banco de dados, basta executar as seguintes linhas de código:
    >>> from crud_celular import db
    >>> db.create_all()
    """

    id = db.Column(db.Integer, primary_key=True)
    marca = db.Column(db.String(60), nullable=False)
    modelo = db.Column(db.String(40), nullable=False)
    nome = db.Column(db.String(50), nullable=False)
    capacidade = db.Column(db.String(20), nullable=False)
    velocidade_processamento = db.Column(db.String(20), nullable=False)
    memoria_ram = db.Column(db.String(20), nullable=False)

    def to_json(self):
        return {
            "id": self.id,
            "marca": self.marca,
            "modelo": self.modelo,
            "nome": self.nome,
            "capacidade": self.capacidade,
            "velocidade_processamento": self.velocidade_processamento,
            "memoria_ram": self.memoria_ram
        }


# Visualizar todos os celulares
@app.route("/modelos", methods=["GET"])
def seleciona_todos_celulares():
    celular_objetos = Celular.query.all()
    celular_json = [modelo.to_json() for modelo in celular_objetos]

    return response_reporte(200, "modelos", celular_json)


# Visualizar celular por id
@app.route("/modelo/<id>", methods=["GET"])
def seleciona_modelo_id(id):
    celular_objeto = busca_por_id(id)
    celular_json = celular_objeto.to_json()

    return response_reporte(200, "celular_por_id", celular_json)


# Inserir um novo celular
@app.route("/modelo", methods=["POST"])
def inserir_celular():
    body = request.get_json()
    try:
        celular = Celular(marca=body["marca"],
                          modelo=body["modelo"],
                          nome=body["nome"],
                          capacidade=body["capacidade"],
                          velocidade_processamento=body["velocidade_processamento"],
                          memoria_ram=body["memoria_ram"])
        db.session.add(celular)
        db.session.commit()
        return response_reporte(201, "celular", celular.to_json())
    except Exception as e:
        print('Error: ', e)
        return response_reporte(400, "", {})


# Atualizar
@app.route("/modelo/<id>", methods=["PUT"])
def atualiza_celular(id):
    celular_objeto = busca_por_id(id)
    body = request.get_json()

    try:
        if 'marca' in body:
            celular_objeto.marca = body["marca"]
        if 'modelo' in body:
            celular_objeto.modelo = body["modelo"]
        if 'nome' in body:
            celular_objeto.nome = body["nome"]
        if 'capacidade' in body:
            celular_objeto.capacidade = body["capacidade"]
        if 'memoria_ram' in body:
            celular_objeto.memoria_ram = body["memoria_ram"]
        if 'velocidade_processamento' in body:
            celular_objeto.velocidade_processamento = body["velocidade_processamento"]

        db.session.add(celular_objeto)
        db.session.commit()
        return response_reporte(200, "celular", celular_objeto.to_json(), "Atualizado com sucesso")
    except Exception as e:
        print('Error: ', e)
        return response_reporte(400, "", {}, "Erro ao atualizar")

def busca_por_id(id):
    return Celular.query.filter_by(id=id).first_or_404(
        description='Não houve ocorrências do id: {}'.format(id))


def response_reporte(status, nome_do_conteudo, conteudo, mensagem="False"):
    body = {nome_do_conteudo: conteudo}
    if mensagem:
        body["mensagem"] = mensagem
    return Response(json.dumps(body), status=status, mimetype="application/json")
