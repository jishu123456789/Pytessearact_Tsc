# -*- coding: utf-8 -*-
from flask import Flask, request, jsonify
import cv2
import numpy as np
import pytesseract
import time
import requests
from pdf2image import convert_from_path
import concurrent.futures
import os

app = Flask(__name__)

# Limit OpenMP threads
os.environ["OMP_THREAD_LIMIT"] = "8"

def extract_text_from_image(image):
    """Extract text from an image using OCR."""
    try:
        preprocessed_image = np.array(image)
        gray = cv2.cvtColor(preprocessed_image, cv2.COLOR_BGR2GRAY)
        _, binarized = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        custom_config = r'--oem 3'
        text = pytesseract.image_to_string(binarized, config=custom_config)
        
        return text
    except Exception as e:
        print(f"Error processing image: {e}")
        return ""

def process_page(page):
    """Process a single page of a PDF."""
    return extract_text_from_image(page)

def download_pdf(pdf_url):
    """Download PDF from the given URL."""
    try:
        response = requests.get(pdf_url, stream=True)
        if response.status_code == 200:
            pdf_path = "temp.pdf"
            with open(pdf_path, "wb") as f:
                f.write(response.content)
            return pdf_path
        else:
            return None
    except Exception as e:
        print(f"Error downloading PDF: {e}")
        return None

@app.route("/extract_text", methods=["POST"])
def extract_text():
    """API endpoint to process a PDF from a URL."""
    data = request.json
    pdf_url = data.get("pdf_url")

    if not pdf_url:
        return jsonify({"error": "Missing PDF URL"}), 400

    pdf_file = download_pdf(pdf_url)
    if not pdf_file:
        return jsonify({"error": "Failed to download PDF"}), 500

    print(f"Processing PDF: {pdf_file}")
    start_time = time.time()
    
    try:
        pages = convert_from_path(pdf_file)
        extracted_text = []

        with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
            results = executor.map(process_page, pages)

        extracted_text.extend(results)

        end_time = time.time()
        print(f"Total Processing Time: {end_time - start_time:.2f} seconds")
        
        return jsonify({"text": extracted_text})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
