from flask import Blueprint, request
from http import HTTPStatus
import sqlalchemy.exc
import werkzeug
from src.database import db
from src.models.client import Client,client_schema,clients_schema

clients = Blueprint("clients",__name__,url_prefix="/api/v1/clients")

@clients.get("/")
def read_all():
    clients = Client.query.order_by(Client.name).all()
    return {"data": clients_schema.dump(clients)}, HTTPStatus.OK

@clients.get("/<int:id>")
def read_one(id):
    client = Client.query.filter_by(id=id).first()
    if(not client):
        return {"error": "Resource not found"}, HTTPStatus.NOT_FOUND
    return {"data": client_schema.dump(client)}, HTTPStatus.OK

@clients.post("/")
def create(user_id):
    post_data = None

    try:
        post_data = request.get_json()
    except werkzeug.exceptions.BadRequest as e:
        return {"error": "Post body JSON data not found","message": str(e)}, HTTPStatus.BAD_REQUEST

    client = Client(id = request.get_json().get("id", None),
        name = request.get_json().get("name", None),
        tipo_documento = request.get_json().get("tipo_documento", None),
        apellido = request.get_json().get("apellido", None),
        email = request.get_json().get("email", None),
        telefono = request.get_json().get("telefono", None),
        edad = request.get_json().get("edad", None),
        ciudad_residencia = request.get_json().get("ciudad_residencia", None))
    try:
        db.session.add(client)
        db.session.commit()
    except sqlalchemy.exc.IntegrityError as e:
        return {"error": "Invalid resource values","message": str(e)}, HTTPStatus.BAD_REQUEST

    return {"data": client_schema.dump(client)}, HTTPStatus.CREATED

@clients.put('/<int:id>')
def update(id):
    post_data = None

    try:
        post_data = request.get_json()
    except werkzeug.exceptions.BadRequest as e:
        return {"error": "Put body JSON data not found","message": str(e)}, HTTPStatus.BAD_REQUEST

    client = Client.query.filter_by(id=id).first()
    if(not client):
        return {"error": "Resource not found"}, HTTPStatus.NOT_FOUND

    client.name = request.get_json().get('name', client.name)
    client.email = request.get_json().get('email', client.email)
    client.password = request.get_json().get('password', client.password)
    try:
        db.session.commit()
    except sqlalchemy.exc.IntegrityError as e:
        return {"error": "Invalid resource values","message": str(e)}, HTTPStatus.BAD_REQUEST

    return {"data": client_schema.dump(client)}, HTTPStatus.OK

@clients.delete("/<int:id>")
def delete(id):
    client = Client.query.filter_by(id=id).first()
    if(not client):
        return {"error": "Resource not found"}, HTTPStatus.NOT_FOUND
    try:
        db.session.delete(client)
        db.session.commit()
    except sqlalchemy.exc.IntegrityError as e:
        return {"error": "Resource could not be deleted","message": str(e)}, HTTPStatus.BAD_REQUEST

    return {"data": ""}, HTTPStatus.NO_CONTENT

