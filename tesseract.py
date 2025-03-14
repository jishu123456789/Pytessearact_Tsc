# -*- coding: utf-8 -*-
"""
Created on Thu Mar 13 11:33:05 2025
@author: jishu
"""

import cv2
import numpy as np
import pytesseract
import time
from pdf2image import convert_from_path
import concurrent.futures
import os


os.environ["OMP_THREAD_LIMIT"] = "16"


def extract_text_from_image(image):
    
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
    return extract_text_from_image(page)


def main(pdf_file):
   
    print(f"Processing PDF: {pdf_file}")

    start_time = time.time()
    pages = convert_from_path(pdf_file)
    extracted_text = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=16) as executor:
        results = executor.map(process_page, pages)
    extracted_text.extend(results)
    end_time = time.time()
    print(f"Total Processing Time: {end_time - start_time:.2f} seconds")
    output_file = pdf_file.replace(".pdf", "_extracted.txt")
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("\n".join(extracted_text))

    print(f"Extracted text saved to: {output_file}")
if __name__ == "__main__":
    pdf_path = "temp3.pdf" 
    main(pdf_path)
