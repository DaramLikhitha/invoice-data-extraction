# Invoice Data Extraction - MODEL-1

## Overview

This project utilizes the OpenAI GPT-3.5-turbo model for extracting carrier names from single invoice images or PDFs.

## Constraints

1. Only one PDF or image should be processed at a time.
2. If the input is a PDF consisting of images, data extraction will not be performed.

## Usage

### Input

- Accepts either a single invoice image or a PDF file.

### Output

- Extracts the carrier name from the provided invoice.

## Instructions

1. Ensure that only one PDF or image is provided as input.
2. If the input is a PDF, make sure it does not contain image-based pages.

To run the invoice data extraction, follow these steps:

1. **Clone the Repository**:

    ```bash
    git clone https://github.com/DaramLikhitha/invoice-data-extraction.git
    cd invoice-data-extraction
    ```

2. **Install Dependencies**:

    ```bash
    pip install -r requirements.txt
    ```

3. **Run with Streamlit**:

    ```bash
    streamlit run app.py
    ```

4. **Access the App**:

   Open your web browser and navigate to [http://localhost:8501](http://localhost:8501).

## Notes

- Ensure that you have a valid OpenAI GPT-3.5-turbo API key configured.

- For optimal performance, provide clear and well-scanned single invoice images or PDFs.

## Contributing

Contributions are welcome! Feel free to open issues or submit pull requests.

