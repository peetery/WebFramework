from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import mapped_column

db = SQLAlchemy()

class DataPoint(db.Model):
    id = mapped_column(db.Integer, primary_key=True, autoincrement=True)
    feature1 = mapped_column(db.Float, nullable=False)
    feature2 = mapped_column(db.Float, nullable=False)
    category = mapped_column(db.Integer, nullable=False)

    def __repr__(self):
        return f"DataPoint({self.id}, {self.feature1}, {self.feature2}, {self.category})"