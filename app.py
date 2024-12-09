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

@app.route('/')
def index():
    data_points = DataPoint.query.all()
    return render_template('index.html', data_points=data_points)

@app.route('/add', methods=['GET', 'POST'])
def add_data_point():
    if request.method == 'POST':
        feature1 = request.form['feature1']
        feature2 = request.form['feature2']
        category = request.form['category']
        try:
            data_point = DataPoint(feature1=feature1, feature2=feature2, category=category)
            db.session.add(data_point)
            db.session.commit()
            return redirect(url_for('index'))
        except ValueError:
            return 'Invalid data', 400
    return render_template('add.html')

@app.route('/delete/<int:record_id>', methods=['POST'])
def delete_data_point(record_id):
    data_point = DataPoint.query.get(record_id)
    if data_point is None:
        return "Record not found", 404
    db.session.delete(data_point)
    db.session.commit()
    return redirect(url_for('index'))
