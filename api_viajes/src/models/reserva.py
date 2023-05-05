from datetime import datetime
from src.database import db, ma
from src.models.consulta import Consulta

class Reserva(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    origen = db.Column(db.String(50),unllble=False)
    destino = db.Column(db.String(50),unllble=False)
    fecha = db.Column(db.Date,unllble=False)
    estado = db.Column(db.String(30),unllble=False)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=datetime.now())

    consultas = db.relationship('Consultas', backref="owner")

    def __init__(self, **fields):
        super().__init__(**fields)

    def __repr__(self) -> str:
        return f"Reserva >>> {self.name}"

class ReservaSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
     model = Reserva
    include_fk = True

reserva_schema = ReservaSchema()
reservas_schema = ReservaSchema(many=True)
