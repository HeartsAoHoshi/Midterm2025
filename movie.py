from flask_sqlalchemy import SQLAlchemy
from datetime import date

db = SQLAlchemy()

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=True)
    rating = db.Column(db.Float, nullable=False)
    release_date = db.Column(db.Date, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'rating': self.rating,
            'release_date': self.release_date.isoformat()
        }
