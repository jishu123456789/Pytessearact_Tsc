# Pytessearact_Tsc

# Flask PDF Text Extraction API

This is a Flask-based API that extracts text from PDFs using Tesseract OCR and OpenCV.

## Features

- Accepts a PDF URL via a POSTMAN request.
- Downloads and converts the PDF to images.
- Uses Tesseract OCR to extract text.
- Returns the extracted text as a response.

## Installation

### Prerequisites

Ensure you have the following installed in your virtual environment in ubuntu:

- Python 3.9+
- Pip
- Tesseract OCR
- pdf2image

### Install Dependencies : Install them in your virtual enviroment in ubuntu

```sh
pip install flask requests numpy opencv-python pytesseract pdf2image tesseract-ocr
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

### Using `curl` (Command Line) : [You can directly put this command on Postman. A Sample PDF url is also given] [Give proper url as per your device] 

```sh
curl -X POST http://127.0.0.1:5000/extract_text \
     -H "Content-Type: application/json" \
     -d '{"pdf_url": "https://arxiv.org/pdf/2410.07659"}'
```
        
### 🚀 Enjoy using the Flask PDF Text Extraction API! 🚀

