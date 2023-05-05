from datetime import datetime
from src.database import db, ma
from src.models.consulta import Consulta

class Viaje(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tipo_viaje = db.Column(db.String(50),unllble=False)
    valor = db.Column(db.Float,unllble=False)
    caracteristicas = db.Column(db.String(100),unllble=False)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=datetime.now())

    consultas = db.relationship('Consultas', backref="owner")

    def __init__(self, **fields):
        super().__init__(**fields)

    def __repr__(self) -> str:
        return f"Viaje >>> {self.name}"

class ViajeSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
     model = Viaje
    include_fk = True

viaje_schema = ViajeSchema()
viajes_schema = ViajeSchema(many=True)
