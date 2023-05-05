from datetime import datetime
from src.database import db, ma

class Consulta(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=datetime.now())
    documento_cliente = db.Column(db.String(10),db.ForeignKey('client.documento',onupdate="CASCADE",ondelete="RESTRICT"),nullable=False)
    id_viaje = db.Column(db.String(10),db.ForeignKey('viaje.id',onupdate="CASCADE",ondelete="RESTRICT"),nullable=False)

    def __init__(self, **fields):
        super().__init__(**fields)

    def __repr__(self) -> str:
        return f"Consulta >>> {self.name}"

class ConsultaSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
     model = Consulta
    include_fk = True

consulta_schema = ConsultaSchema()
consultas_schema = ConsultaSchema(many=True)
