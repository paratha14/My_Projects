from langchain_core.documents import Document

def format_items(items):
    return ', '.join([f"{item['itemname']} (₹{item['itemPrice']}, {item['itemType']})" for item in items])

def supplier_to_text(supplier):
    loc = supplier['location']
    return f"""
    Supplier Name: {supplier['businessname']}
    Owner: {supplier['username']}
    Email: {supplier['email']}
    Contact: {int(supplier['contact'])}
    Location: {loc['Landmark']}, {loc['city']}, {loc['state']} - {loc['pincode']}
    Items Offered: {format_items(supplier['itemsSold'])}
    Joined on: {supplier['createdAt'].strftime('%B %d, %Y')}
    """.strip()

def vendor_to_text(vendor):
    loc = vendor['location']
    cleaned_items = [
        {
            'itemname': item['itemname'],
            'itemPrice': item['itemPrice'],
            'itemType': item['itemType']
        } for item in vendor['itemsSold']
    ]

    items_offered = ", ".join(
        f"{item['itemname']} (₹{item['itemPrice']}, {item['itemType']})"
        for item in cleaned_items
    )

    return f"""
Vendor Name: {vendor['businessname']}
Owner: {vendor['username']}
Email: {vendor['email']}
Contact: {int(vendor['contact'])}
Location: {loc['Landmark']}, {loc['city']}, {loc['state']} - {loc['pincode']}

Items Offered: {items_offered}

Joined on: {vendor['createdAt'].strftime('%B %d, %Y')}
""".strip()

def generate_dynamic_query(vendor)->str:
    if "itemsSold" not in vendor or not vendor["itemsSold"]:
        return "I need suppliers for raw materials."

    item_list = [
        f"{item['itemname']} (₹{item['itemPrice']}, {item['itemType']})"
        for item in vendor["itemsSold"]
    ]
    return f"I need suppliers who sell raw materials for items like {', '.join(item_list)}."
