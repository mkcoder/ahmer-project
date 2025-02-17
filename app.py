from flask import Flask, request, jsonify
from flask_cors import CORS
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from databaseClass import Database
import mysql.connector

app = Flask(__name__)

# Initialize the database
db = Database()

def get_product_details_from_description(description_input, num_results=5):
    """
    Function to get product details from the database by comparing the input text with product descriptions
    and return multiple similar products.
    """
    try:
        # Retrieve all descriptions and their corresponding product details from the database
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

        # If no products were returned
        if not products:
            print("No products found in the database.")  # Log when no products are found
            return {"error": "No products found in the database"}

        # Extract product descriptions and product IDs for comparison
        product_descriptions = [product[2] for product in products]
        product_ids = [product[0] for product in products]
        product_names = [product[1] for product in products]
        product_prices = [product[3] for product in products]
        product_sizes = [product[4] for product in products]
        product_images = [product[5] for product in products]
        product_links = [product[6] for product in products]

        # Use TfidfVectorizer to convert text into vectors
        vectorizer = TfidfVectorizer(stop_words='english')
        tfidf_matrix = vectorizer.fit_transform(product_descriptions + [description_input])

        # Calculate cosine similarity between the input description and all product descriptions
        cosine_similarities = cosine_similarity(tfidf_matrix[-1], tfidf_matrix[:-1])

        # Get the indices of the most similar products
        similarity_scores = cosine_similarities.flatten()  # Flatten the array to get all similarity scores
        sorted_idx = similarity_scores.argsort()[-num_results:][::-1]  # Get top N most similar products, sorted by score

        # Prepare the response with multiple product details
        result = []
        for idx in sorted_idx:
            product = {
                "product_id": product_ids[idx],
                "product_name": product_names[idx],
                "product_description": product_descriptions[idx],
                "product_price": product_prices[idx],
                "product_size": product_sizes[idx],
                "product_image": product_images[idx],
                "product_link": product_links[idx]
            }
            result.append(product)

        print(f"Returning top {num_results} product details: {result}")  # Log the returned result
        return result
    except mysql.connector.Error as e:
        print(f"Error retrieving products from the database: {e}")  # Log the error
        return {"error": f"Error retrieving products from the database: {e}"}

CORS(app, resources={r"/search": {"origins": "http://127.0.0.1:5500"}})

@app.route('/search', methods=['POST'])
def search_product():
    """
    API endpoint to receive input text and return matched product details
    """
    try:
        # Get the input text (description) from the POST request
        data = request.get_json()
        print(f"Received data: {data}")
        
        # Extract description input from the received data
        description_input = data.get('description', '')

        if not description_input:
            return jsonify({"error": "Description input is missing"}), 400

        print(f"Searching for product details matching: {description_input}")

        # Get the most similar product based on description
        product_details = get_product_details_from_description(description_input)

        if 'error' in product_details:
            print(f"Error in product search: {product_details['error']}")
            return jsonify(product_details), 500

        # Return the product details as JSON
        print(f"Returning product details: {product_details}")
        return jsonify(product_details), 200

    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5001)