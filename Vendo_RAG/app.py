from flask import Flask, request, jsonify
from mongo import get_vendor_data, get_supplier_data
from user_utils import generate_dynamic_query, vendor_to_text
from vectorstore import build_vectorstore
from rag import build_rag_chain
from flask_cors import CORS

app= Flask(__name__)
CORS(app)

suppliers = get_supplier_data()
vectorstore = build_vectorstore(suppliers)
retriever = vectorstore.as_retriever(search_type="mmr", search_kwargs={"k": 2})
rag_chain = build_rag_chain()
print("RAG chain built successfully!")

@app.route("/", methods=["GET"])
def home():
    return "Flask app is running!"

@app.route("/recommend", methods=["POST"])
def recommend():
    data = request.get_json()
    vendor_username = data.get("vendor_username")

    vendor = get_vendor_data(vendor_username)
    print("Data received!")
    if not vendor:
        return jsonify({"error": "Vendor not found"})

    query = generate_dynamic_query(vendor)
    print("Generated query:", query)
    docs = retriever.invoke(query)
    supp_info = "\n".join([doc.page_content for doc in docs])
    print("Supplier info retrieved:", supp_info)
    vendor_info = vendor_to_text(vendor)
    print("Vendor info:", vendor_info)

    result = rag_chain.invoke({"vendor_info": vendor_info, "supp_info": supp_info})
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)