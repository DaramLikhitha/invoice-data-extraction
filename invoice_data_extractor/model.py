from openai import OpenAI
from dotenv import load_dotenv, find_dotenv
import os
import io
from PIL import Image
import pytesseract
from PyPDF2 import PdfReader
from pdf2image import convert_from_path
import cv2
import numpy as np


path = f'C:/Program Files/poppler-23.11.0/Library/bin'

_ = load_dotenv(find_dotenv())

client = OpenAI(
    # This is the default and can be omitted
    api_key=os.environ.get("OPENAI_API_KEY"),
)

# Function for additional OpenCV image processing
def additional_image_processing(image):
    # Example: Apply GaussianBlur for additional smoothing
    blurred_img = cv2.GaussianBlur(image, (5, 5), 0)
    return blurred_img

# Function to extract text from images using OCR
def extract_text_from_image(image):
    Img = Image.open(io.BytesIO(image))
    img_array = np.array(Img)

    # Convert the image to grayscale
    gray_img = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)

    # Apply adaptive thresholding to enhance text visibility
    threshold_img = cv2.adaptiveThreshold(gray_img, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)

    # Apply additional OpenCV processing
    processed_img = additional_image_processing(threshold_img)

    text = pytesseract.image_to_string(processed_img)
    return text

# Function to extract text from PDF files
def extract_text_from_pdf(pdf_file):
    text = ""
    try:
        pdf_reader = PdfReader(io.BytesIO(pdf_file))
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            text += page.extract_text()
        return text
    except Exception as e:
        return f"Error reading PDF: {str(e)}"

# Function to extract text from scanned PDF files
def extract_text_from_pdf_img(pdf_file):
    images = convert_from_path(pdf_file, poppler_path=path)

    text = ""
    for i, image in enumerate(images):
        # Convert each image to grayscale
        gray_img = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2GRAY)

        # Apply adaptive thresholding to enhance text visibility
        threshold_img = cv2.adaptiveThreshold(gray_img, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)

        # Apply additional OpenCV processing
        processed_img = additional_image_processing(threshold_img)

        text += pytesseract.image_to_string(processed_img)

    return text

from tenacity import (
    retry,
    stop_after_attempt,
    wait_random_exponential,
)  # for exponential backoff

@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(3))
# Function for GPT-3 interaction
def extracted_data(invoice_text):
    prompt = f"""Extract the carrier/company name from the following invoice text:\n\n{invoice_text}
    \n\nCompany name:"""

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model="gpt-3.5-turbo-0301",
        max_tokens=100,  # Adjust as needed
        temperature=0.1,
    )

    # Extracting the company name from the generated response
    company_name = chat_completion.choices[0].message.content
    print(company_name)
    return company_name
