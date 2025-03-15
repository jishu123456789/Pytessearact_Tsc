# Pytessearact_Tsc

# Flask PDF Text Extraction API

This is a Flask-based API that extracts text from PDFs using Tesseract OCR and OpenCV.

## Features

- Accepts a PDF URL via a POST request.
- Downloads and converts the PDF to images.
- Uses Tesseract OCR to extract text.
- Returns the extracted text as a response.

## Installation

### Prerequisites

Ensure you have the following installed:

- Python 3.8+
- Pip
- Tesseract OCR

### Install Dependencies

```sh
pip install flask requests numpy opencv-python pytesseract pdf2image
```

## Running the API Locally

### 1. Start the Flask App

```sh
python app.py
```

You should see output like this:

```
 * Running on http://127.0.0.1:5000
 * Running on http://192.168.X.X:5000 (Your Local Network IP)
```

### 2. Check Your Local IP Address

If running locally, use:

```
http://127.0.0.1:5000/extract_text
```

If accessing from another device on the same WiFi:

```
http://192.168.X.X:5000/extract_text
```

(Replace `X.X` with your actual local IP.)

## Testing the API

### Using Postman

1. Open **Postman**.
2. Select **POST** request.
3. Enter URL: `http://127.0.0.1:5000/extract_text`
4. Set **Headers**:
   ```json
   {
     "Content-Type": "application/json"
   }
   ```
5. Set **Body (raw JSON)**:
   ```json
   {
     "pdf_url": "https://investors.3m.com/financials/sec-filings/content/0001558370-19-000470/0001558370-19-000470.pdf"
   }
   ```
6. Click **Send**.

### Using `curl` (Command Line)

```sh
curl -X POST http://127.0.0.1:5000/extract_text \
     -H "Content-Type: application/json" \
     -d '{"pdf_url": "https://investors.3m.com/financials/sec-filings/content/0001558370-19-000470/0001558370-19-000470.pdf"}'
```

## Flask API Code Example

Create a file `app.py`:

```python
from flask import Flask, request, jsonify
import requests
import cv2
import numpy as np
import pytesseract
from pdf2image import convert_from_path
import os

app = Flask(__name__)

@app.route('/extract_text', methods=['POST'])
def extract_text():
    data = request.get_json()
    pdf_url = data.get("pdf_url")
    if not pdf_url:
        return jsonify({"error": "No PDF URL provided"}), 400
    
    response = requests.get(pdf_url)
    if response.status_code != 200:
        return jsonify({"error": "Failed to download PDF"}), 500
    
    with open("temp.pdf", "wb") as f:
        f.write(response.content)
    
    pages = convert_from_path("temp.pdf")
    extracted_text = []
    for page in pages:
        img = np.array(page)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        text = pytesseract.image_to_string(gray)
        extracted_text.append(text)
    
    return jsonify({"extracted_text": "\n".join(extracted_text)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
```

### 🚀 Enjoy using the Flask PDF Text Extraction API! 🚀

