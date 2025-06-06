from flask import Flask, request, jsonify, render_template, redirect
from pymongo import MongoClient
import os

# إعداد Flask
app = Flask(__name__)

# الاتصال بقاعدة البيانات MongoDB Atlas
client = MongoClient("mongodb+srv://Store:ihge2660@mystoreproject.udmwjft.mongodb.net/store?retryWrites=true&w=majority")
db = client["store"]
products_collection = db["products"]

# الصفحة الرئيسية: عرض المنتجات
@app.route("/")
def index():
    products = list(products_collection.find())
    return render_template("index.html", products=products)

# صفحة الإدارة: إضافة منتجات وعرضها
@app.route("/admin", methods=["GET", "POST"])
def admin():
    if request.method == "POST":
        title = request.form.get("title")
        price = request.form.get("price")
        image = request.form.get("image")
        description = request.form.get("description")
        if title and price:
            products_collection.insert_one({
                "title": title,
                "price": price,
                "image": image,
                "description": description
            })
        return redirect("/admin")

    products = list(products_collection.find())
    return render_template("admin.html", products=products)

# حذف منتج
@app.route("/delete/<product_id>", methods=["POST"])
def delete_product(product_id):
    from bson.objectid import ObjectId
    products_collection.delete_one({"_id": ObjectId(product_id)})
    return redirect("/admin")

# التعديل يمكن إضافته هنا إذا أردت لاحقاً...

# ✅ لتعمل على Render: استخدم host 0.0.0.0 و port من المتغير البيئي
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
