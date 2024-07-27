import requests

# Step 1: Extract text from the image using OCR
def extract_text_from_image(image_path):
    url = "https://ocr-text-extraction-with-handwriting-detection.p.rapidapi.com/extract-text"
    querystring = {"ocr_type": "detect_text"}
    
    # Open the image file
    with open(image_path, "rb") as image_file:
        files = {
            "file": image_file
        }

        headers = {
            "x-rapidapi-key": "0a9a52237dmsh60a738ac5281f90p11e987jsneb3200d985f1",
            "x-rapidapi-host": "ocr-text-extraction-with-handwriting-detection.p.rapidapi.com"
        }

        response = requests.post(url, files=files, headers=headers, params=querystring)
        response_data = response.json()
        
        if 'detected_text' in response_data:
            return response_data['detected_text']
        else:
            print("Failed to extract text")
            print("Response:", response_data)
            return None

# Step 2: Detect the language of the extracted text
def detect_language(detected_text):
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
            return detected_language
        else:
            print("No detections found")
            return None
    else:
        print("Failed to detect language")
        print("Response:", response_data)
        return None

# Step 3: Translate the extracted text to English
def translate_text(text, detected_language):
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
        return translated_text
    else:
        print("Failed to translate text")
        print("Response:", response_data)
        return None

# Main function to perform the entire process
def main():
    image_path = r"C:\Users\Admin\Downloads\WhatsApp Image 2024-07-27 at 6.40.51 PM.jpeg"  # Replace with your image file path

    # Extract text from the image
    extracted_text = extract_text_from_image(image_path)
    if extracted_text is None:
        return
    
    print("Extracted text:")
    print(extracted_text)

    # Detect the language of the extracted text
    detected_language = detect_language(extracted_text)
    if detected_language is None:
        return
    
    print(f"Detected language: {detected_language}")

    # Translate the extracted text to English
    translated_text = translate_text(extracted_text, detected_language)
    if translated_text is None:
        return
    
    print("Translated text:")
    print(translated_text)

if __name__ == "__main__":
    main()
