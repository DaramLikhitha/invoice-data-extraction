import streamlit as st
import os
import tempfile
from model import *


# Streamlit UI
def main():
    st.set_page_config(page_title="Invoice Bot")
    st.title("Invoice Data Extraction")

    uploaded_file = st.file_uploader("Choose a PDF or image file", type=["pdf", "png", "jpg", "jpeg"])

    if uploaded_file is not None:
        file_type = uploaded_file.name.split('.')[-1]
        content = uploaded_file.read()

        # Display uploaded image or PDF
        if file_type.lower() in ['png', 'jpg', 'jpeg']:
            # st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)
            text = extract_text_from_image(content)

        elif file_type.lower() == 'pdf':
            text = extract_text_from_pdf(content)

        if text=="":
            temp_dir = tempfile.TemporaryDirectory()
            file_path = os.path.join(temp_dir.name, uploaded_file.name)

            with open(file_path, 'wb') as f:
                f.write(content)

            text = extract_text_from_pdf_img(file_path)

            temp_dir.cleanup()

        if st.button('Extract Data'):

            # Call your Model here
            result = extracted_data(text)

            st.subheader("Carrier name : ")
            st.success(result)

    else:
        st.warning("Please upload a PDF file.")

if __name__ == "__main__":
    main()