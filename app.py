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

with app.app_context():
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

@app.route('/api/data', methods=['GET'])
def get_data():
    data_points = DataPoint.query.all()
    return jsonify([{'id': dp.id,
                     'feature1': dp.feature1,
                     'feature2': dp.feature2,
                     'category': dp.category} for dp in data_points])

@app.route('/api/data', methods=['POST'])
def api_add_data_point():
    data = request.get_json()
    try:
        dp = DataPoint(feature1=data['feature1'], feature2=data['feature2'], category=data['category'])
        db.session.add(dp)
        db.session.commit()
        return jsonify({'id': dp.id,}), 201
    except (ValueError, KeyError):
        return jsonify({'error': 'Invalid data'}), 400

@app.route('/api/data/<int:record_id>', methods=['DELETE'])
def api_delete_data_point(record_id):
    data_point = DataPoint.query.get(record_id)
    if data_point is None:
        return jsonify({'error': 'Record not found'}), 404
    db.session.delete(data_point)
    db.session.commit()
    return '', 204

if __name__ == '__main__':
    app.run(debug=True)