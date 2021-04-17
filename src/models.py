from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.email

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }

class Mascota(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    idUser = db.Column(db.Integer, db.ForeignKey('user.id'))
    nombre = db.Column(db.String(120), unique=False, nullable=False)
    edad = db.Column(db.Integer, nullable=False)
    peso = db.Column(db.Integer, nullable=False)
    user = db.relationship("User", backref=db.backref("Mascota", cascade="all,delete"))

    def __repr__(self):
        return '<Mascota %r>' % self.nombre

    def serialize(self):
        return {
            "id": self.id,
            "idUser": self.idUser,
            "nombre": self.nombre,
            "edad": self.edad,
            "peso": self.peso,
            "user": self.user.serialize()
            # do not serialize the password, its a security breach
        }
    