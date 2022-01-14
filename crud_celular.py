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


def response_reporte(status, nome_do_conteudo, conteudo, mensagem="False"):
    body = {nome_do_conteudo: conteudo}
    if mensagem:
        body["mensagem"] = mensagem
    return Response(json.dumps(body), status=status, mimetype="application/json")
