from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Mapped, mapped_column

db = SQLAlchemy()

class DataPoint(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    feature1: Mapped[float] = mapped_column(nullable=False)
    feature2: Mapped[float] = mapped_column(nullable=False)
    category: Mapped[int] = mapped_column(nullable=False)