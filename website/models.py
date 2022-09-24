from . import db

from datetime import datetime


class Usina(db.Model):
    id = db.Column(db.Integer , primary_key=True , autoincrement=True)
    name = db.Column(db.String(20), nullable=False)

    #inversor = db.relationship("Inversor")


class Inversor(db.Model):
    id = db.Column(db.Integer , primary_key=True , autoincrement=True)
    name = db.Column(db.String(40), nullable=False)

    usina_id = db.Column(db.Integer, db.ForeignKey('usina.id'))
    usina = db.relationship("Usina")


    def __repr__(self) -> str:
        return f'<Inversor {self.id} | Usina {self.usina_id} | {self.name}>'


class Dados(db.Model):
    id = db.Column(db.Integer, db.ForeignKey(
        'inversor.id'),  primary_key=True)
    timestamp = db.Column(
        db.DateTime, default=datetime.utcnow(), primary_key=True, nullable=False)

    power_ca = db.Column(db.Float, nullable=False)
    power_cc = db.Column(db.Float)
    energy_ca = db.Column(db.Float, nullable=False)
    #temperature = db.Column(db.Float)

    inversor = db.relationship("Inversor")

