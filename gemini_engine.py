import os
from google import genai
from google.genai import types
from PIL import Image
from dotenv import load_dotenv

load_dotenv()

# Initialize the new Google GenAI client
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# Use Gemini 2.5 Flash (Stable)
MODEL_NAME = "gemini-2.5-flash" 

def analyze_label(image_path: str):
    """
    Sends an image to Gemini 3.1 for OCR and health analysis using the new google-genai SDK.
    Returns a structured response.
    """
    print(f"Opening image: {image_path}")
    img = Image.open(image_path)
    
    prompt = """
    Analyze this food label image and provide a structured report.
    Include the following sections:
    1. Product Name
    2. Ingredients List
    3. Nutrition Facts Summary
    4. Safety Score (1-10, where 10 is safest/healthiest)
    5. Health Warnings (highlight harmful additives, high sugar, etc.)
    6. Eco-Tip (packaging sustainability)
    7. Suggested Alternatives
    
    Format the output with emojis and clear headings suitable for a Telegram message.
    """
    
    print("Sending request to Gemini API...")
    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=[prompt, img]
    )
    print("Response received.")
    
    return response.text
