from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Product(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    price = db.Column(db.Float)
    description = db.Column(db.String(200))
    image = db.Column(db.String(200))
    type = db.Column(db.String(20))
    reviews = db.Column(db.Integer)