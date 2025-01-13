from flask import Flask, render_template, request, redirect, url_for, jsonify
from models import db, DataPoint

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

@app.route('/')
def home():
    with db.session.begin():
        data_points = db.session.query(DataPoint).all()
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

        with db.session.begin():
            new_point = DataPoint(feature1=feature1, feature2=feature2, category=category)
            db.session.add(new_point)

        return redirect(url_for('home'))
    else:
        return render_template('add.html')

@app.route('/delete/<int:record_id>', methods=['POST'])
def delete(record_id):
    with db.session.begin():
        data_point = db.session.query(DataPoint).get(record_id)
        if not data_point:
            return render_template('error.html',
                                   error_code=404,
                                   error_message="Record not found. Unable to delete."), 404
        db.session.delete(data_point)

    return redirect(url_for('home'))

@app.route('/api/data', methods=['GET'])
def api_get_data():
    with db.session.begin():
        data_points = db.session.query(DataPoint).all()
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
    except (ValueError, KeyError):
        return jsonify({'error': 'Invalid data in API request.'}), 400

    with db.session.begin():
        new_point = DataPoint(feature1=feature1, feature2=feature2, category=category)
        db.session.add(new_point)

    return jsonify({'id': new_point.id}), 201

@app.route('/api/data/<int:record_id>', methods=['DELETE'])
def api_delete_data(record_id):
    with db.session.begin():
        data_point = db.session.query(DataPoint).get(record_id)
        if not data_point:
            return jsonify({'error': 'Record not found'}), 404
        db.session.delete(data_point)

    return jsonify({'id': record_id})