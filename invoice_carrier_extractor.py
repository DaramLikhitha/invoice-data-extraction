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
import streamlit as st
import tempfile

path = f'C:/Program Files/poppler-23.11.0/Library/bin'
os.environ['PATH'] = path

_ = load_dotenv(find_dotenv())

client = OpenAI(
    # This is the default and can be omitted
    api_key=os.environ.get("OPENAI_API_KEY"),
)

# Function for additional OpenCV image processing
def additional_image_processing(image):

    image_np = np.array(image)
    resized_image = cv2.resize(image_np, (3100, 3600))
    gray = cv2.cvtColor(resized_image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    _, thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    # st.image(thresh)
    return thresh

# Function to extract text from images using OCR
def extract_text_from_image(image):
    Img = Image.open(io.BytesIO(image))
    img_array = np.array(Img)

    # Apply additional OpenCV processing
    processed_img = additional_image_processing(img_array)

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
    images = convert_from_path(pdf_file)

    text = ""
    for i, image in enumerate(images):
        # Apply additional OpenCV processing
        processed_img = additional_image_processing(image)

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

# Streamlit UI
def main():
    st.set_page_config(page_title="Invoice Bot")
    st.title("Invoice Data Extraction")

    uploaded_files = st.file_uploader("Choose a PDF or image file", type=["pdf", "png", "jpg", "jpeg"], accept_multiple_files=True)
    if uploaded_files is not None:
        invoices = []
        for uploaded_file in uploaded_files:
            file_type = uploaded_file.name.split('.')[-1]
            content = uploaded_file.read()

            # Display uploaded image or PDF
            if file_type.lower() in ['png', 'jpg', 'jpeg']:
                text = extract_text_from_image(content)

            elif file_type.lower() == 'pdf':
                text = extract_text_from_pdf(content)

            if text == "":
                temp_dir = tempfile.TemporaryDirectory()
                file_path = os.path.join(temp_dir.name, uploaded_file.name)

                with open(file_path, 'wb') as f:
                    f.write(content)

                text = extract_text_from_pdf_img(file_path)

                temp_dir.cleanup()
            
            invoices.append([uploaded_file.name,text])

    else:
        st.warning("Please upload a PDF or image file.")
    
    if st.button('Extract Data'):
        st.subheader("Carrier name : ")

        for name,text in invoices:
            result = extracted_data(text)
            st.write(name)
            st.success(result)


if __name__ == "__main__":
    main()