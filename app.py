import os
import streamlit as st
import tempfile
from model import *

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