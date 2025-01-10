from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pyodbc://username:password@server/database?driver=SQL+Server'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Database Models
class Component(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    plan_key = db.Column(db.String(50))
    stat_pos = db.Column(db.String(20))
    order_number = db.Column(db.String(20))
    index = db.Column(db.String(5))
    position = db.Column(db.String(20))
    quantity = db.Column(db.Integer)
    volume = db.Column(db.Float)
    weight = db.Column(db.Float)
    component_type = db.Column(db.String(50))
    length = db.Column(db.Float)
    height = db.Column(db.Float)
    width = db.Column(db.Float)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_pdf():
    if 'pdf_file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    # File processing logic will go here
    return jsonify({'message': 'File uploaded successfully'})

if __name__ == '__main__':
    app.run(debug=True)
