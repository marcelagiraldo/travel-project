from datetime import datetime
from src.database import db, ma
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    id = db.Column(db.String(10), primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(60), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=datetime.now())

    def __init__(self, **fields):
        super().__init__(**fields)

    def __repr__(self) -> str:
        return f"User >>> {self.name}"

    @staticmethod
    def hash_password(password):
        return generate_password_hash(password)@staticmethod
    def hash_password(password):
        return generate_password_hash(password)

    def check_password(self, password):
     return check_password_hash(self.password, password)

    def __setattr__(self, name, value):
        if(name == "password"):
            value = User.hash_password(value)
        super(User, self).__setattr__(name, value)

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        include_fk = True

user_schema = UserSchema()
users_schema = UserSchema(many=True)


