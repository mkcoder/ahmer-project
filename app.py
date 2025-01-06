# from flask import Flask, request, jsonify
# from PIL import Image
# from transformers import pipeline
# import io

# app = Flask(__name__)

# # Example Hugging Face pipeline for image processing
# image_processor = pipeline("image-classification", model="google/vit-base-patch16-224")

# @app.route('/upload', methods=['POST'])
# def upload_image():
#     try:
#         # Check if an image file is part of the request
#         if 'image' not in request.files:
#             return jsonify({"error": "No image file provided"}), 400

#         image_file = request.files['image']

#         # Open the image file
#         image = Image.open(image_file)

#         # Convert the image to a format suitable for the Hugging Face model
#         image = image.convert("RGB")

#         # Process the image using the Hugging Face pipeline
#         results = image_processor(image)

#         # Return the results as JSON
#         return jsonify({"results": results}), 200

#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

# if __name__ == '__main__':
#     app.run(debug=True)

from flask import Flask, request, jsonify
import mysql.connector

app = Flask(__name__)

# Database connection
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Newton 123",
        database="cloth_design_database"
    )

@app.route('/compare-text', methods=['POST'])
def compare_text():
    data = request.json
    input_text = data.get('inputText')

    if not input_text:
        return jsonify({"message": "No input text provided"}), 400

    # Connect to the database
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)  # Fetch rows as dictionaries

    # Query to join product description and product details based on product_url
    query = """
    SELECT 
        p.Product_link AS url, 
        p.Product_image AS image, 
        p.Product_price, 
        p.Product_size, 
        d.product_description AS description
    FROM 
        products_detail p
    JOIN 
        product_description d
    ON 
        p.product_url = d.product_url
    WHERE 
        d.product_description LIKE %s
    """
    cursor.execute(query, (f"%{input_text}%",))
    products = cursor.fetchall()

    connection.close()

    if products:
        # Return matched products
        return jsonify({"products": products}), 200
    else:
        # No match found
        return jsonify({"message": "No matching product found"}), 404

if __name__ == '__main__':
    app.run(debug=True)

