from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

# Route to serve the HTML page
@app.route('/')
def index():
    return render_template('index.html')

# Route for extracting text from the image
@app.route('/extract_text', methods=['POST'])
def extract_text_from_image():
    image = request.files.get('file')
    if not image:
        return jsonify({"error": "No image file provided"}), 400

    url = "https://ocr-text-extraction-with-handwriting-detection.p.rapidapi.com/extract-text"
    querystring = {"ocr_type": "detect_text"}

    headers = {
        "x-rapidapi-key": "0a9a52237dmsh60a738ac5281f90p11e987jsneb3200d985f1",
        "x-rapidapi-host": "ocr-text-extraction-with-handwriting-detection.p.rapidapi.com"
    }

    response = requests.post(url, files={"file": image}, headers=headers, params=querystring)
    response_data = response.json()

    if 'detected_text' in response_data:
        return jsonify({"detected_text": response_data['detected_text']})
    else:
        return jsonify({"error": "Failed to extract text"}), 500

# Route for detecting the language of the extracted text
@app.route('/detect_language', methods=['POST'])
def detect_language():
    data = request.json
    detected_text = data.get('text')

    if not detected_text:
        return jsonify({"error": "No text provided"}), 400

    url = "https://google-translator9.p.rapidapi.com/v2/detect"
    payload = {"q": detected_text}
    headers = {
        "x-rapidapi-key": "0a9a52237dmsh60a738ac5281f90p11e987jsneb3200d985f1",
        "x-rapidapi-host": "google-translator9.p.rapidapi.com",
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)
    response_data = response.json()

    if 'data' in response_data and 'detections' in response_data['data']:
        detections = response_data['data']['detections']
        if detections:
            detected_language = detections[0][0]['language']
            return jsonify({"detected_language": detected_language})
    
    return jsonify({"error": "Failed to detect language"}), 500

# Route for translating the text to English
@app.route('/translate_text', methods=['POST'])
def translate_text():
    data = request.json
    text = data.get('text')
    detected_language = data.get('language')

    if not text or not detected_language:
        return jsonify({"error": "No text or language provided"}), 400

    url = "https://google-translator9.p.rapidapi.com/v2"
    payload = {
        "q": text,
        "source": detected_language,
        "target": "en",
        "format": "text"
    }
    headers = {
        "x-rapidapi-key": "0a9a52237dmsh60a738ac5281f90p11e987jsneb3200d985f1",
        "x-rapidapi-host": "google-translator9.p.rapidapi.com",
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)
    response_data = response.json()

    if 'data' in response_data and 'translations' in response_data['data']:
        translated_text = response_data['data']['translations'][0]['translatedText']
        return jsonify({"translated_text": translated_text})
    
    return jsonify({"error": "Failed to translate text"}), 500

if __name__ == '__main__':
    app.run(debug=True)
