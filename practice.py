import cv2
import torch
from transformers import CLIPProcessor, CLIPModel
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Initialize the CLIP model and processor from Hugging Face
model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

def extract_image_features(image_path):
    # Load the image
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError(f"Image at path {image_path} could not be loaded.")
    
    # Convert BGR to RGB (OpenCV uses BGR by default)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    # Resize to the required input size for CLIP (224x224)
    image = cv2.resize(image, (224, 224))
    
    # Use the processor to handle image input
    inputs = processor(images=image, return_tensors="pt", padding=True)
    with torch.no_grad():
        image_features = model.get_image_features(**inputs)
    
    return image_features

def extract_text_features(texts):
    # Process and get text features from CLIP
    inputs = processor(text=texts, return_tensors="pt", padding=True)
    with torch.no_grad():
        text_features = model.get_text_features(**inputs)
    
    return text_features

def load_descriptions():
    # Example database of descriptions about female dresses
    descriptions = [
        "A red evening gown with lace details and a long train",
        "A casual summer dress with floral patterns and short sleeves",
        "A blue cocktail dress with a fitted waist and a flowing skirt",
        "A black dress with a high collar and puffed sleeves",
        "A white wedding dress with a fitted bodice and a voluminous skirt"
    ]
    
    return descriptions

def compare_image_with_database(image_path, descriptions):
    # Extract features from the input image
    image_features = extract_image_features(image_path)
    
    # Extract text features for all descriptions in the database
    text_features = extract_text_features(descriptions)
    
    # Compute cosine similarity between image features and all descriptions
    similarity_scores = cosine_similarity(image_features.numpy(), text_features.numpy())
    
    # Find the best match
    best_match_index = np.argmax(similarity_scores)
    return descriptions[best_match_index], similarity_scores[0][best_match_index]

# Load the descriptions in the database
descriptions = load_descriptions()

# Example input image
image_path = 'C:\Users\HAROON TRADERS\OneDrive\Desktop\Fyp_2025'  # Update this path with your image location

# Compare the input image with descriptions in the database
match_description, score = compare_image_with_database(image_path, descriptions)

print(f"Best match: {match_description} with similarity score: {score}")
