from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
from bson import ObjectId
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

# ✅ رابط MongoDB Atlas (مأخوذ من كلامك)
client = MongoClient("mongodb+srv://Store:ihge2660@mystoreproject.udmwjft.mongodb.net/store?retryWrites=true&w=majority")
db = client['store']
products = db['products']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/api/products')
def get_products():
    all_products = list(products.find())
    for p in all_products:
        p['_id'] = str(p['_id'])
    return jsonify(all_products)

@app.route('/add', methods=['POST'])
def add_product():
    data = request.get_json()
    products.insert_one({
        'name': data['name'],
        'description': data['description'],
        'price': data['price'],
        'image': data['image']
    })
    return '', 204

@app.route('/delete/<id>', methods=['DELETE'])
def delete_product(id):
    products.delete_one({'_id': ObjectId(id)})
    return '', 204

@app.route('/update/<id>', methods=['PUT'])
def update_product(id):
    data = request.get_json()
    products.update_one({'_id': ObjectId(id)}, {'$set': {
        'name': data['name'],
        'description': data['description'],
        'price': data['price'],
        'image': data['image']
    }})
    return '', 204

# ✅ اجعل التطبيق يستخدم المنفذ الذي توفره Render
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
