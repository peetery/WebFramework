from flask import Flask, render_template, request, redirect, url_for, jsonify
from models import db, DataPoint

DATABASE_URI = 'sqlite:///data_points.db'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
db.init_app(app)


@app.route('/')
def home():
    data_points = db.session.scalars(db.select(DataPoint))
    return render_template('home.html', data_points=data_points)


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        try:
            feature1 = float(request.form['feature1'])
            feature2 = float(request.form['feature2'])
            category = int(request.form['category'])

        except ValueError:
            return render_template('error.html',
                                   error_code=400,
                                   error_message="Invalid data. Please check your input and try again."
                                   ), 400

        new_point = DataPoint(feature1=feature1, feature2=feature2, category=category)
        db.session.add(new_point)
        db.session.commit()
        return redirect(url_for('home'))
    else:
        return render_template('add.html')


@app.route('/delete/<int:record_id>', methods=['POST'])
def delete(record_id):
    data_point = db.session.scalar(db.select(DataPoint).where(DataPoint.id == record_id))
    if not data_point:
        return render_template('error.html',
                                error_code=404,
                                error_message="Record not found. Unable to delete."
                               ), 404
    db.session.delete(data_point)
    db.session.commit()
    return redirect(url_for('home'))


@app.route('/api/data', methods=['GET'])
def api_get_data():
    data_points = db.session.scalars(db.select(DataPoint))
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

    new_point = DataPoint(feature1=feature1, feature2=feature2, category=category)
    db.session.add(new_point)
    db.session.commit()
    return jsonify({'id': new_point.id}), 201


@app.route('/api/data/<int:record_id>', methods=['DELETE'])
def api_delete_data(record_id):
    data_point = db.session.scalar(db.select(DataPoint).where(DataPoint.id == record_id))
    if not data_point:
        return jsonify({'error': 'Record not found'}), 404
    db.session.delete(data_point)
    db.session.commit()
    return jsonify({'id': record_id})