from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)

class DataPoint(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    feature1 = db.Column(db.Float, nullable=False)
    feature2 = db.Column(db.Float, nullable=False)
    category = db.Column(db.Integer, nullable=False)

db.create_all()