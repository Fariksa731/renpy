from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
from bson import ObjectId

app = Flask(__name__)

# إعداد الاتصال بقاعدة البيانات
MONGO_URI = "mongodb+srv://Store:ihge2660@mystoreproject.udmwjft.mongodb.net/store?retryWrites=true&w=majority"
client = MongoClient(MONGO_URI)
db = client["store"]
products_col = db["products"]

# الصفحة الرئيسية
@app.route('/')
def index():
    products = list(products_col.find())
    return render_template('index.html', products=products)

# صفحة الإدارة
@app.route('/admin')
def admin():
    products = list(products_col.find())
    return render_template('admin.html', products=products)

# API: إضافة منتج
@app.route('/api/products', methods=['POST'])
def add_product():
    data = request.json
    result = products_col.insert_one(data)
    return jsonify({'_id': str(result.inserted_id)}), 201

# API: حذف منتج
@app.route('/api/products/<id>', methods=['DELETE'])
def delete_product(id):
    products_col.delete_one({'_id': ObjectId(id)})
    return jsonify({'status': 'deleted'})

# API: تعديل منتج
@app.route('/api/products/<id>', methods=['PUT'])
def update_product(id):
    data = request.json
    products_col.update_one({'_id': ObjectId(id)}, {'$set': data})
    return jsonify({'status': 'updated'})

if __name__ == '__main__':
    app.run(debug=True)
