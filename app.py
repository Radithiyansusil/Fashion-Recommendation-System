from flask import Flask, render_template, request
import requests
import json
import google.generativeai as genai
import absl.logging
import creds
# from dotenv import load_dotenv
# import os

# load_dotenv()  # Load environment variables from .env file
# api_key = os.getenv("API_KEY") # Get the API key from the environment variables

# Initialize logging system
absl.logging.set_verbosity(absl.logging.ERROR)

genai.configure(api_key=creds.api_key) # Set the API key for the GenAI client
model = genai.GenerativeModel("gemini-1.5-flash")

app = Flask(__name__)

# Function to generate recommendations
def generate_recommendation(gender,clothing_item, color, style, occasion, material, age, size):
    prompt = f"""
    You are a fashion expert. Your task is to suggest a complete outfit recommendation based on the following clothing item and its characteristics:

    - Gender:{gender} 
    - Clothing Item: {clothing_item}
    - Color: {color}
    - Style: {style}
    - Occasion: {occasion}
    - Material: {material}
    - Age: {age}
    - Size: {size}

    Based on the above details, suggest the following:
    1. A matching pair for the clothing item (e.g., if the input is a shirt, suggest pants or jeans).
    2. A suitable hairstyle that complements the outfit.
    3. A pair of shoes that matches the occasion and style.

    Provide your answer in the following format:
    - Matching Pair: [Your suggestion]
    - Hairstyle: [Your suggestion]
    - Shoes: [Your suggestion]
    - Reason: [Brief explanation of why these choices work well together]
    """
    response = model.generate_content(prompt)
    if len(response.text) > 0:
        formatted_output = response.text.replace("- Matching Pair:", "<br>- Matching Pair:")
        formatted_output = formatted_output.replace("- Hairstyle:", "<br>- Hairstyle:")
        formatted_output = formatted_output.replace("- Shoes:", "<br>- Shoes:")
        formatted_output = formatted_output.replace("- Reason:", "<br>- Reason:")
        return formatted_output
    else:
        return "Error: Unable to generate a recommendation. Please try again."

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # Get user input from the form
        gender = request.form['gender']
        clothing_item = request.form['clothing_item']
        color = request.form['color']
        style = request.form['style']
        occasion = request.form['occasion']
        material = request.form['material']
        age = request.form['age']
        size = request.form['size']

        # Generate recommendations
        recommendations = generate_recommendation(gender,clothing_item, color, style, occasion, material, age, size)
        return render_template('index.html', recommendations=recommendations)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)