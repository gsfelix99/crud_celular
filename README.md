# Uma simples aplicação *Flask* - **CRUD** Celular

Esta é uma aplicação baseada na framewrk Python Flask. O objetivo desta aplicação é a execução do CRUD um uma tabela no Banco de Dados de um modelo de celular.

A tabela de celulares possui os seguintes campos:
  - id (Chave Primária);
  - marca (Tipo String de tamanho 60);
  - modelo (Tipo String de tamanho 40);
  - nome (Tipo String de tamanho 20);
  - capacidade (Tipo String de tamanho 20);
  - velocidade_processamento (Tipo String de tamanho 20);
  - memoria_ram (Tipo String de tamanho 20).

Todos os campos não podem possuir valor nulo.

## Instalando dependências
Antes de iniciarmos a aplicação, é necessário a configuração do ambiente de desenvolvimento. Com a ajuda do arquivo *requirements.txt* podemos instalar todas as dependências necessárias:
```
$ pip install requirements.txt
```
As principais tecnologias utilizadas, são:
  - [Flask 2.0.2](https://flask.palletsprojects.com/en/1.1.x/);
  - [Flask-SQLAlchemy 2.5.1](https://flask-sqlalchemy.palletsprojects.com/en/2.x/#);
  - [mysql-connector-python 8.0.27](https://dev.mysql.com/doc/connector-python/en/);
  - [mysqlclient 2.1.0](https://pypi.org/project/mysqlclient/).
 
Os softwares utilidados, foram:
  - [Python 3.9.7](https://www.python.org/)
  - [PyCharm 2021.2.3 (Professional Edition)](https://www.jetbrains.com/pt-br/pycharm/download/#section=windows)
  - [DataGrip 2021.2.4](https://www.jetbrains.com/pt-br/datagrip/)
  - [MySQL Workbench 8.0.27 (community)](https://dev.mysql.com/downloads/workbench/)
  - [Postman 9.8.3](https://www.postman.com/)

 
### Conectando ao Bando de Dados

Com o ambiente de desenvolvimento já configurado, a primeira parte cosiste na conexão com o banco de dados, que para esta aplicação, foi optado pelo MySQL.  
```py
import json

import mysql.connector
from flask import Flask, Response, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:055109711@localhost/modelo_celular'

db = SQLAlchemy(app)
``` 
*Nota*: o endereço para conexão varia conforme a utilização. em um caso genérico, deve-se ser executado desta forma:
```py
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:[senha_acesso]@[endereço_servidor]/[nome_db]'
```

### Criando uma tabela

As tabelas são geradas automaticamente de acordo com o medelo criado com o *sqlaclchemy*, desta forma, podemos definir uma classe da seguinte forma:
```py
class Celular(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    marca = db.Column(db.String(60), nullable=False)
    modelo = db.Column(db.String(40), nullable=False)
    nome = db.Column(db.String(50), nullable=False)
    capacidade = db.Column(db.String(20), nullable=False)
    velocidade_processamento = db.Column(db.String(20), nullable=False)
    memoria_ram = db.Column(db.String(20), nullable=False)
```
*Nota:* O nome da classe será o nome final da tabela no BD.
Apesar da criação do modelo, a tabela ainda não foi criado no banco de dados propriamente dito. Para a criação da tabela no banco de dados, basta executar as seguintes linhas de código (Mais informações disponíveis na documentação do [*sqlalchemy*](https://flask-sqlalchemy.palletsprojects.com/en/2.x/quickstart/#a-minimal-application)):
```py
    >>> from crud_celular import db
    >>> db.create_all()
```
Desta forma, uma vez criada, a classe tem disponível algumas funções pré-definidas pelo *sqlalchemy*.
## CRUD

As operações de CRUD(**Create**, **Read**, **Update** e **Delete**), são efetuadas pelos métodos a seguir:
### Visualizando todos os registros
Pela rota definica com *Flask*, atravéz do método **GET** conseguimos consultar todos os registros da tabela *celular* no Banco de Dados. A classe *Celular*, como dito anteriormente, possui algumas funções do *sqlalchemy*, portanto, com o método *Celulaar.query.all()* é possível a consulta ao banco sem necessitar de querys em SQL.
```py
@app.route("/modelos", methods=["GET"])
def seleciona_todos_celulares():
    celular_objetos = Celular.query.all()
    celular_json = [modelo.to_json() for modelo in celular_objetos]

    return response_reporte(200, "modelos", celular_json)
```

*Nota:* A função *response_reporte()* é apenas uma forma de facilitar o gerenciamento de *Responses*, pois para cada método de CRUD criado, seria necessário uma nova *Response()*. A função *response_reporte()* foi definida da seguinte forma:
```python
def response_reporte(status, nome_do_conteudo, conteudo, mensagem="False"):
    body = {nome_do_conteudo: conteudo}
    if mensagem:
        body["mensagem"] = mensagem
    return Response(json.dumps(body), status=status, mimetype="application/json")
```
### Visualizando um registro por id
Para vizualizar um registro baseado em seu id, segue a mesma forma anterior, porém para um único registro, desta forma, o id passado pela rota é passado como parâmetro a função *sleciona_modelo_id*:
```py
@app.route("/modelo/<id>", methods=["GET"])
def sleciona_modelo_id(id):
    celular_objeto = busca_por_id(id)
    celular_json = celular_objeto.to_json()
    return response_reporte(200, "celular_por_id", celular_json)
```
Como a busca por id é repetido diverssas vezes no decorrer do código, a função *busca_pr_id* foi criada como forma a evitar esta repetição desnecessária.
```py
def busca_por_id(id):
    return Celular.query.filter_by(id=id).first_or_404(
        description='Não houve ocorrências do id: {}'.format(id))
```
A função *first_or_404()*, caso não haja nenhuma ocorrência requerida, ela retorna o seguinte erro:
```HTML
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">
<title>404 Not Found</title>
    <h1>Not Found</h1>
<p>Não houve ocorrências do id: 3</p>
```
*Nota:* Neste caso, foi feita a busca de um id 3 inexistente.  
### Inserindo um novo registro

Neste caso, como não estamos pegando mas sim inserindo algo no banco de dados, a nossa rota utiliza o método **POST**. Para a inserção devemos primeiro pegar as informações adquiridas pela função *get_json()*, e então associa-las a nossa classe *Celular*. Até este ponto, nunhuma informação foi enviada ao BD, primeiramente devemos dar o comando de **INSERT** com a função *db.session.all()*, e só então, depois de executar a função *db.session.commit()*, estes dados serão enviados ao BD. 
```py
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
```

### Atualizar um registro

Analogamente a inserção, para atualizar um registro iremos eviar informações ao BD, porém, desta vez com o método **PUT**. Como estamos enviando informações ao BD, devemos pegar as iformações fornecidas com a função *get_json()*, e então, associamos as mudanças, se ocorridas, para cada atributo de *Celular*, e então, da mesma forma que anteriormente, enviamos ao BD. 
```py
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

```

### Deletar um registro

Para o método **DELETE**, apenas realizamos uma busca por id, e com a função *db.session.delete()*, deletamos oregistro solicitado.
```py
@app.route("/modelo/<id>", methods=["DELETE"])
def deleta_celular(id):
    celular_objeto = busca_por_id(id)

    try:
        db.session.delete(celular_objeto)
        db.session.commit()
        return response_reporte(200, "celular", celular_objeto.to_json(), "Deletado com sucesso")
    except Exception as e:
        print('Error: ', e)
        return response_reporte(400, "celular", {}, "Erro ao deletar")

```

## Implementações futuras

 - Multiplas inserções 
 - Interação com uma página HTML
 - Adicionar novas tabelas

## Créditos

 - Referência ao video do canal [Programando Com Roger](https://www.youtube.com/watch?v=WDpPGFkI9UU).
 - Código original, disponível em [crud-flask](https://github.com/vieiraroger/crud-flask)
