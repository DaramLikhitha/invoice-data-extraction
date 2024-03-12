import streamlit as st
from PIL import Image
import pytesseract
from PyPDF2 import PdfReader
import io
from model import *


# Function to extract text from images using OCR
def extract_text_from_image(image):
    Img = Image.open(io.BytesIO(image))
    text = pytesseract.image_to_string(Img)
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

# Streamlit UI
def main():
    st.set_page_config(page_title="Invoice Bot")
    st.title("Invoice Data Extraction")

    uploaded_file = st.file_uploader("Choose a PDF or image file", type=["pdf", "png", "jpg", "jpeg"])

    if uploaded_file is not None:
        file_type = uploaded_file.name.split('.')[-1]

        # Display uploaded image or PDF
        if file_type.lower() in ['png', 'jpg', 'jpeg']:
            # st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)
            text = extract_text_from_image(uploaded_file.read())
        elif file_type.lower() == 'pdf':
            text = extract_text_from_pdf(uploaded_file.read())

        if text=="":
            st.error("Sorry...Unable to extract data from uploaded documents")

        elif st.button('Extract Data'):

            # Call your Model here
            result = extracted_data(text)

            st.subheader("Carrier name : ")
            st.success(result)


if __name__ == "__main__":
    main()