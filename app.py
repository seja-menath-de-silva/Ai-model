from flask import Flask, render_template, request, jsonify
from google.generativeai import genai
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

# Configure API
def configure_api():
    api_key = "AIzaSyAgYD9komBIepaqDvKT3FJSVbynsc9WVkg"
    genai.configure(api_key=api_key)

# Set up the model
def setup_model():
    generation_config = {
        "temperature": 0.4,
        "top_p": 1,
        "top_k": 32,
        "max_output_tokens": 4096,
    }

    safety_settings = [
        {
            "category": "HARM_CATEGORY_HARASSMENT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        {
            "category": "HARM_CATEGORY_HATE_SPEECH",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        {
            "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        {
            "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        }
    ]

    return genai.GenerativeModel(model_name="gemini-pro-vision",
                                 generation_config=generation_config,
                                 safety_settings=safety_settings)

# Handle file upload
def upload_file():
    file = request.files['image']
    if file:
        filename = secure_filename(file.filename)
        file.save(os.path.join("uploads", filename))
        return filename
    return None

@app.route('/')
def index():
    return render_template('https://dub9yt9jaous2llnwnuokw.on.drv.tw/index%20.html')

@app.route('/generate_content', methods=['POST'])
def generate_content():
    configure_api()
    model = setup_model()

    prompt = request.form['prompt']
    image_filename = upload_file()

    if image_filename:
        image_path = os.path.join("uploads", image_filename)
        with open(image_path, 'rb') as image_file:
            image_data = image_file.read()
            prompt_parts = [prompt]
            generated_text = model.generate_content(prompt_parts, image_data).text
            return jsonify({"generated_text": generated_text})

    return jsonify({"error": "Image not uploaded"})

if __name__ == '__main__':
    os.makedirs("uploads", exist_ok=True)
    app.run(debug=True)
