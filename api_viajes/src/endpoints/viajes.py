from flask import Blueprint, request
from http import HTTPStatus
import sqlalchemy.exc
import werkzeug
from src.database import db
from src.models.viaje import Viaje,viaje_schema,viajes_schema

viajes = Blueprint("viajes",__name__,url_prefix="/api/v1")

@viajes.get("/viajes")
def read_all():
    viajes = Viaje.query.order_by(Viaje.id).all()
    return {"data": viajes_schema.dump(viajes)}, HTTPStatus.OK

@viajes.get("/viajes/<int:id>")
def read_one(id):
    viaje = Viaje.query.filter_by(id=id).first()
    if(not Viaje):
       return {"error": "Resource not found"}, HTTPStatus.NOT_FOUND
    return {"data": viaje_schema.dump(viaje)},HTTPStatus.OK

@viajes.post("/viajes")
def create():
    post_data = None

    try:
        post_data = request.get_json()
    except werkzeug.exceptions.BadRequest as e:
        return {"error": "Post body JSON data not found","message": str(e)}, HTTPStatus.BAD_REQUEST

    Viaje = Viaje(id = request.get_json().get("id", None),
        documento=documento,
        id_viaje=id_viaje)
    try:
        db.session.add(Viaje)
        db.session.commit()
    except sqlalchemy.exc.IntegrityError as e:
        return {"error": "Invalid resource values","message": str(e)}, HTTPStatus.BAD_REQUEST

    return {"data": Viaje_schema.dump(Viaje)}, HTTPStatus.CREATED

@viajes.put('/clientes/<int:documento>/viajes/<int:id_viaje>/viajes/<int:id>')
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

@viajes.delete("/clientes/<int:id>")
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

