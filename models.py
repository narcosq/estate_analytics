from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Listing(db.Model):
    __tablename__ = 'listings'

    id = db.Column(db.Integer, primary_key=True)
    submission_date = db.Column(db.Date, default=datetime.utcnow)
    deactivation_date = db.Column(db.Date, nullable=True)
    deactivation_reason = db.Column(db.String(100))
    price = db.Column(db.Float)
    square_meters = db.Column(db.Float)
    district = db.Column(db.String(100))
    city = db.Column(db.String(100))
    region = db.Column(db.String(100))