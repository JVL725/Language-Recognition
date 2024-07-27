document.addEventListener('DOMContentLoaded', () => {
    const detectButton = document.getElementById('detectButton');
    const imageInput = document.getElementById('imageInput');
    const detectedLanguageElem = document.getElementById('detectedLanguage');
    const translatedTextElem = document.getElementById('translatedText');

    detectButton.addEventListener('click', () => {
        const file = imageInput.files[0];
        if (!file) {
            alert('Please upload an image file.');
            return;
        }

        const formData = new FormData();
        formData.append('file', file);

        fetch('/extract_text', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert(data.error);
                return;
            }

            const extractedText = data.detected_text;
            detectLanguage(extractedText);
        })
        .catch(error => console.error('Error:', error));
    });

    function detectLanguage(text) {
        fetch('/detect_language', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ text })
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert(data.error);
                return;
            }

            const detectedLanguage = data.detected_language;
            detectedLanguageElem.textContent = `Detected Language: ${detectedLanguage}`;
            translateText(text, detectedLanguage);
        })
        .catch(error => console.error('Error:', error));
    }

    function translateText(text, language) {
        fetch('/translate_text', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ text, language })
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert(data.error);
                return;
            }

            const translatedText = data.translated_text;
            translatedTextElem.textContent = `Translated Text: ${translatedText}`;
        })
        .catch(error => console.error('Error:', error));
    }
});
