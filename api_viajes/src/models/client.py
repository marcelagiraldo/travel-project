from datetime import datetime
from src.database import db, ma
from src.models.consulta import Consulta


class Client(db.Model):
    documento = db.Column(db.String(10), primary_key=True)
    tipo_documento = db.Column(db.String(20))
    name = db.Column(db.String(80), nullable=False)
    apellido = db.Column(db.String(60), unique=True, nullable=False)
    telefeno = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), nullable=False)
    edad = db.Column(db.Integer, nullable=False)
    ciudad_residencia = db.Column(db.String(30), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=datetime.now())

    consultas = db.relationship('Consultas', backref="owner")

    def __init__(self, **fields):
        super().__init__(**fields)

    def __repr__(self) -> str:
        return f"Client >>> {self.name}"

class ClientSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
     model = Client
    include_fk = True

client_schema = ClientSchema()
clients_schema = ClientSchema(many=True)
