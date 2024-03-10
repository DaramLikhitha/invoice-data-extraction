from openai import OpenAI
from dotenv import load_dotenv, find_dotenv
import os
import io
from PIL import Image
import pytesseract
from PyPDF2 import PdfReader
from pdf2image import convert_from_path

path = f'C:/Program Files/poppler-23.11.0/Library/bin'

_ = load_dotenv(find_dotenv())

client = OpenAI(
    # This is the default and can be omitted
    api_key=os.environ.get("OPENAI_API_KEY"),
)

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
    

# Function to extract text from scanned PDF files
def extract_text_from_pdf_img(pdf_file):

    images = convert_from_path(pdf_file,poppler_path=path)

    text = ""
    for i, image in enumerate(images):
        text += pytesseract.image_to_string(image)

    return text

def extracted_data(invoice_text):
    prompt = f"""Extract the company name from the following invoice text:\n\n{invoice_text}
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
        temperature=0.5,
    )

    # Extracting the company name from the generated response
    company_name = chat_completion.choices[0].message.content
    print(company_name)
    return company_name