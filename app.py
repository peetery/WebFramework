from flask import Flask, render_template, request, redirect, url_for, jsonify, abort
from models import db, DataPoint

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

@app.route('/')
def home():
    data_points = DataPoint.query.all()
    return render_template('home.html', data_points=data_points)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        if not all(key in request.form for key in ['feature1', 'feature2', 'category']):
            return render_template('error.html',
                                   error_code=400,
                                   error_message="Missing required fields. Please fill in all fields and try again."), 400
        try:
            feature1 = float(request.form['feature1'])
            feature2 = float(request.form['feature2'])
            category = int(request.form['category'])
        except ValueError:
            return render_template('error.html',
                                   error_code=400,
                                   error_message="Invalid data. Please check your input and try again."), 400
        new_point = DataPoint(feature1=feature1, feature2=feature2, category=category)
        db.session.add(new_point)
        db.session.commit()
        return redirect(url_for('home'))
    else:
        return render_template('add.html')

@app.route('/delete/<int:record_id>', methods=['POST'])
def delete(record_id):
    data_point = DataPoint.query.get(record_id)
    if not data_point:
        return render_template('error.html',
                               error_code=404,
                               error_message="Record not found. Unable to delete."), 404
    db.session.delete(data_point)
    db.session.commit()
    return redirect(url_for('home'))

# API Endpoints
@app.route('/api/data', methods=['GET'])
def api_get_data():
    data_points = DataPoint.query.all()
    return jsonify([{
        'id': dp.id,
        'feature1': dp.feature1,
        'feature2': dp.feature2,
        'category': dp.category
    } for dp in data_points])

@app.route('/api/data', methods=['POST'])
def api_add_data():
    data = request.get_json()
    try:
        feature1 = float(data['feature1'])
        feature2 = float(data['feature2'])
        category = int(data['category'])
        new_point = DataPoint(feature1=feature1, feature2=feature2, category=category)
        db.session.add(new_point)
        db.session.commit()
        return jsonify({'id': new_point.id}), 201
    except (ValueError, KeyError):
        return jsonify({'error': 'Invalid data in API request.'}), 400

@app.route('/api/data/<int:record_id>', methods=['DELETE'])
def api_delete_data(record_id):
    data_point = DataPoint.query.get(record_id)
    if not data_point:
        return jsonify({'error': 'Record not found'}), 404
    db.session.delete(data_point)
    db.session.commit()
    return jsonify({'id': record_id})