# model.py
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from transformers import CLIPProcessor, CLIPModel
import torch
import numpy as np
from PIL import Image
import mysql.connector

class ProductSearchModel:
    def __init__(self, db):
        self.db = db
        self.clip_model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
        self.clip_processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

    def get_product_details_from_description(self, description_input, num_results=5):
        try:
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
            self.db.cursor.execute(query)
            products = self.db.cursor.fetchall()

            if not products:
                return {"error": "No products found in the database"}

            product_descriptions = [product[2] for product in products]
            product_ids = [product[0] for product in products]
            product_names = [product[1] for product in products]
            product_prices = [product[3] for product in products]
            product_sizes = [product[4] for product in products]
            product_images = [product[5] for product in products]
            product_links = [product[6] for product in products]

            vectorizer = TfidfVectorizer(stop_words='english')
            tfidf_matrix = vectorizer.fit_transform(product_descriptions + [description_input])

            cosine_similarities = cosine_similarity(tfidf_matrix[-1], tfidf_matrix[:-1])
            similarity_scores = cosine_similarities.flatten()
            sorted_idx = similarity_scores.argsort()[-num_results:][::-1]

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

            return result
        except mysql.connector.Error as e:
            return {"error": f"Error retrieving products from the database: {e}"}

    def get_product_details_from_image(self, image_file, num_results=5):
        try:
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
            self.db.cursor.execute(query)
            products = self.db.cursor.fetchall()

            if not products:
                return {"error": "No products found in the database"}

            product_descriptions = [product[2] for product in products]
            product_details = [product for product in products]

            try:
                image = Image.open(image_file).convert("RGB")
            except Exception as e:
                return {"error": f"Invalid image format: {e}"}

            image_input = self.clip_processor(images=image, return_tensors="pt")
            with torch.no_grad():
                image_features = self.clip_model.get_image_features(**image_input).numpy()

            inputs = self.clip_processor(
                text=product_descriptions,
                return_tensors="pt",
                padding=True,
                truncation=True
            )
            with torch.no_grad():
                text_features = self.clip_model.get_text_features(**inputs).numpy()

            similarities = np.dot(image_features, text_features.T) / (
                np.linalg.norm(image_features) * np.linalg.norm(text_features, axis=1)
            )

            sorted_idx = similarities.argsort()[0][-num_results:][::-1]

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
                    "similarity_score": float(similarities[0][idx])
                })
            return result
        except mysql.connector.Error as e:
            return {"error": f"Database error: {e}"}
        except Exception as e:
            return {"error": f"Unexpected error: {e}"}