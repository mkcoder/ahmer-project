from flask import Flask, request, jsonify
from flask_cors import CORS
from transformers import CLIPProcessor, CLIPModel
import torch
import numpy as np
from PIL import Image
from databaseClass import Database
import mysql.connector
import os

# Suppress TensorFlow logs (optional)
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"

app = Flask(__name__)

# Enable CORS for cross-origin requests
CORS(app, resources={r"/search": {"origins": "http://127.0.0.1:5500"}})

# Initialize the database
db = Database()

# Load the CLIP model and processor for image feature extraction
model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

def get_product_details_from_image(image_file, num_results=5):
    # Function to get product details from the database by comparing an input image with product descriptions.
    try:
        # Fetch all product descriptions and their details from the database
        query = """
        SELECT product_detail.Product_id, 
               product_detail.product_name, 
               product_description.product_description, 
               product_detail.product_price, 
               product_detail.product_size, 
               product_detail.product_image, 
               product_detail.product_link
        FROM product_detail
        JOIN product_description ON product_detail.Product_link = product_description.Product_link
        """
        db.cursor.execute(query)
        products = db.cursor.fetchall()

        # Handle case where no products exist in the database
        if not products:
            return {"error": "No products found in the database"}

        # Extract product descriptions and details
        product_descriptions = [product[2] for product in products]
        product_details = [product for product in products]

        # Convert the uploaded file to a PIL Image
        try:
            image = Image.open(image_file).convert("RGB")
        except Exception as e:
            return {"error": f"Invalid image format: {e}"}

        # Preprocess the image
        image_input = processor(images=image, return_tensors="pt")

        # Extract features from the image using the CLIP model
        with torch.no_grad():
            image_features = model.get_image_features(**image_input).numpy()

        # Preprocess the text with truncation enabled
        inputs = processor(
            text=product_descriptions,
            return_tensors="pt",
            padding=True,
            truncation=True  # Truncate descriptions longer than 77 tokens
        )
        with torch.no_grad():
            text_features = model.get_text_features(**inputs).numpy()

        # Compute cosine similarity between the image and text embeddings
        similarities = np.dot(image_features, text_features.T) / (
            np.linalg.norm(image_features) * np.linalg.norm(text_features, axis=1)
        )

        # Get indices of the most similar products
        sorted_idx = similarities.argsort()[0][-num_results:][::-1]

        # Prepare the response with product details
        result = []
        for idx in sorted_idx:
            product = product_details[idx]
            result.append({
                "product_id": product[0],
                "product_name": product[1],
                "product_description": product[2],
                "product_price": product[3],
                "product_size": product[4],
                "product_image": product[5],
                "product_link": product[6],
                "similarity_score": float(similarities[0][idx])  # Add similarity score for transparency
            })
        return result
    except mysql.connector.Error as e:
        return {"error": f"Database error: {e}"}
    except Exception as e:
        return {"error": f"Unexpected error: {e}"}


@app.route('/search', methods=['POST'])
def search_product():

    # API endpoint to receive an input image and return matched product details.
    try:
        print("Request received!")  # Debug log

        # Validate and fetch the uploaded image
        if 'image' not in request.files or request.files['image'].filename == '':
            return jsonify({"error": "No valid image file provided"}), 400

        image_file = request.files['image']
        print(f"Received image file: {image_file.filename}")  # Debug log

        # Get product details based on the uploaded image
        product_details = get_product_details_from_image(image_file)

        # Check for errors in the result
        if 'error' in product_details:
            print(f"Error in product details: {product_details['error']}")  # Debug log
            return jsonify(product_details), 500

        print(f"Returning product details: {product_details}")  # Debug log
        return jsonify(product_details), 200
    except Exception as e:
        # Log any unexpected errors
        print(f"Error: {e}")
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, port=5002)
