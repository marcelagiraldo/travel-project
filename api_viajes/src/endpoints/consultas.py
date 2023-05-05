from flask import Blueprint, request
from http import HTTPStatus
import sqlalchemy.exc
import werkzeug
from src.database import db
from src.models.consulta import Consulta,consulta_schema,consultas_schema

consultas = Blueprint("consultas",__name__,url_prefix="/api/v1")

@consultas.get("/consultas")
def read_all():
    consultas = Consulta.query.order_by(Consulta.name).all()
    return {"data": consultas_schema.dump(consultas)}, HTTPStatus.OK

@consultas.get("/consultas/<int:id>")
def read_one(id):
    consulta = Consulta.query.filter_by(id=id).first()
    if(not consulta):
       return {"error": "Resource not found"}, HTTPStatus.NOT_FOUND
    return {"data": consulta_schema.dump(consulta)},HTTPStatus.OK

@consultas.post("/clientes/<int:documento>/viajes/<int:id_viaje>/consultas")
def create(documento,id_viaje):
    post_data = None

    try:
        post_data = request.get_json()
    except werkzeug.exceptions.BadRequest as e:
        return {"error": "Post body JSON data not found","message": str(e)}, HTTPStatus.BAD_REQUEST

    consulta = Consulta(id = request.get_json().get("id", None),
        documento=documento,
        id_viaje=id_viaje)
    try:
        db.session.add(consulta)
        db.session.commit()
    except sqlalchemy.exc.IntegrityError as e:
        return {"error": "Invalid resource values","message": str(e)}, HTTPStatus.BAD_REQUEST

    return {"data": consulta_schema.dump(consulta)}, HTTPStatus.CREATED

@consultas.put('/clientes/<int:documento>/viajes/<int:id_viaje>/consultas/<int:id>')
def update(id,documento,id_viaje):
    post_data = None

    try:
        post_data = request.get_json()
    except werkzeug.exceptions.BadRequest as e:
        return {"error": "Put body JSON data not found","message": str(e)}, HTTPStatus.BAD_REQUEST

    consulta = Consulta.query.filter_by(id=id).first()
    if(not consulta):
        return {"error": "Resource not found"}, HTTPStatus.NOT_FOUND

    if (documento != consulta.documento_cliente):
        consulta.documento_cliente = documento

    if (id_viaje != consulta.id_viaje):
        consulta.id_viaje = id_viaje

    try:
        db.session.commit()
    except sqlalchemy.exc.IntegrityError as e:
        return {"error": "Invalid resource values","message": str(e)}, HTTPStatus.BAD_REQUEST

    return {"data": consulta_schema.dump(consulta)}, HTTPStatus.OK

@consultas.delete("/clientes/<int:id>")
def delete(id):
    consulta = Consulta.query.filter_by(id=id).first()
    if(not consulta):
        return {"error": "Resource not found"}, HTTPStatus.NOT_FOUND
    try:
        db.session.delete(consulta)
        db.session.commit()
    except sqlalchemy.exc.IntegrityError as e:
        return {"error": "Resource could not be deleted","message": str(e)}, HTTPStatus.BAD_REQUEST

    return {"data": ""}, HTTPStatus.NO_CONTENT

