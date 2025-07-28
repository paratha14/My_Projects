from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from bson import ObjectId
from dotenv import load_dotenv
import os

# RAG-specific imports
from mongo import get_vendor_data, get_supplier_data
from user_utils import generate_dynamic_query, vendor_to_text
from vectorstore import build_vectorstore
from rag import build_rag_chain


load_dotenv()
app = Flask(__name__)
CORS(app)

# MongoDB setup
client = MongoClient(os.getenv("MONGO_URI"))
db = client["vendo"]
users_collection = db["users"]
orders_collection = db["orders"]
recipes_collection = db["recipes"]

# Helpers
def serialize_doc(doc):
    doc['_id'] = str(doc['_id'])
    return doc

# --- RAG Initialization ---
suppliers = get_supplier_data()
vectorstore = build_vectorstore(suppliers)
retriever = vectorstore.as_retriever(search_type="mmr", search_kwargs={"k": 2})
rag_chain = build_rag_chain()
print("RAG chain built successfully!")

# ---------------- HOME ----------------
@app.route("/", methods=["GET"])
def home():
    return jsonify({ "message": "Flask unified app is running!" })


# ---------------- USERS ----------------
@app.route('/users', methods=['GET'])
def get_all_users():
    try:
        users = list(users_collection.find())
        return jsonify([serialize_doc(user) for user in users])
    except Exception as e:
        return jsonify({"error": "Internal Server Error"}), 500

@app.route('/user/<id>', methods=['GET'])
def get_user_by_id(id):
    try:
        user = users_collection.find_one({"_id": ObjectId(id)})
        if not user:
            return jsonify({"error": "User not found"}), 404
        return jsonify(serialize_doc(user))
    except Exception as e:
        return jsonify({"error": "Internal Server Error"}), 500

@app.route('/newUser', methods=['POST'])
def create_user():
    try:
        user = request.json
        hashed_pw = bcrypt.hashpw(user['password'].encode('utf-8'), bcrypt.gensalt())
        user['password'] = hashed_pw
        user['createdAt'] = str(user.get('createdAt', ''))
        result = users_collection.insert_one(user)
        return jsonify({ "insertId": str(result.inserted_id) }), 201
    except Exception as e:
        return jsonify({"error": "Internal Server Error"}), 500

@app.route('/deleteUser/<id>', methods=['DELETE'])
def delete_user(id):
    try:
        result = users_collection.delete_one({ "_id": ObjectId(id) })
        if result.deleted_count == 0:
            return jsonify({"error": "User not found"}), 404
        return jsonify({ "message": "User deleted successfully" })
    except Exception as e:
        return jsonify({"error": "Internal Server Error"}), 500


# ---------------- ORDERS ----------------
@app.route('/orders', methods=['GET'])
def get_orders():
    try:
        orders = list(orders_collection.find({}))
        if not orders:
            return jsonify({ "error": "No orders found" }), 404
        return jsonify([serialize_doc(order) for order in orders])
    except Exception as e:
        return jsonify({ "error": "Internal Server Error" }), 500

@app.route('/newOrder', methods=['POST'])
def create_order():
    try:
        order = request.json
        result = orders_collection.insert_one(order)
        return jsonify({ "insertId": str(result.inserted_id) }), 201
    except Exception as e:
        return jsonify({ "error": "Internal Server Error" }), 500


# ---------------- RECIPES ----------------
@app.route('/recipes', methods=['GET'])
def get_recipes():
    try:
        recipes = list(recipes_collection.find({}))
        if not recipes:
            return jsonify({ "error": "No recipes found" }), 404
        return jsonify([serialize_doc(recipe) for recipe in recipes])
    except Exception as e:
        return jsonify({ "error": "Internal Server Error" }), 500

@app.route('/recipe/<id>', methods=['GET'])
def get_recipe_by_id(id):
    try:
        recipe = recipes_collection.find_one({ "_id": ObjectId(id) })
        if not recipe:
            return jsonify({ "error": "Recipe not found" }), 404
        return jsonify(serialize_doc(recipe))
    except Exception as e:
        return jsonify({ "error": "Internal Server Error" }), 500

@app.route('/newRecipe', methods=['POST'])
def create_recipe():
    try:
        recipe = request.json
        result = recipes_collection.insert_one(recipe)
        return jsonify({ "recipeId": str(result.inserted_id) })
    except Exception as e:
        return jsonify({ "error": "Internal Server Error" }), 500


# ---------------- RAG SUGGESTIONS ----------------
@app.route("/vendor-recommendation/<username>", methods=["POST"])
def recommend(username):
    try:
        vendor = get_vendor_data(username)
        if not vendor:
            return jsonify({"error": "Vendor not found"})

        query = generate_dynamic_query(vendor)
        docs = retriever.invoke(query)
        supp_info = "\n".join([doc.page_content for doc in docs])
        vendor_info = vendor_to_text(vendor)

        result = rag_chain.invoke({ "vendor_info": vendor_info, "supp_info": supp_info })
        return jsonify(result)
    except Exception as e:
        print("RAG error:", e)
        return jsonify({ "error": "Failed to generate recommendation" }), 500


# ---------------- START SERVER ----------------
if __name__ == '__main__':
    port = int(os.getenv("PORT", 3000))
    app.run(debug=True, port=port)
