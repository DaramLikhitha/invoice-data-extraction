# Invoice Data Extraction Tool

## Overview

This project utilizes the OpenAI GPT-3.5-turbo model for extracting data from multiple invoice images or PDFs.

## Application

The application runs with Streamlit, providing a user-friendly interface for interacting with the model.

## Usage

### Input

- Accepts multiple invoice images or PDF files.

### Output

- Extracts the invoice data from the provided invoices.

## Prerequisites

Before running the tool, ensure you have the following installed:

- Python 3.7 or later
- Dependencies listed in `requirements.txt`
- Tesseract OCR installed
- Poppler installed and added to system path

## Deployment
You can access the deployed version of this tool here.
For invoice carrier/company name extraction: https://invoice-carrier-name-extractor.streamlit.app/
For invoice multi fields data extraction: https://invoice-multiple-data-extractor.streamlit.app/
For invoice dynamic fields data extraction: https://invoice-dynamic-data-extractor.streamlit.app/

## Notes

- Ensure that you have a valid OpenAI GPT-3.5-turbo API key configured in .env file.


## Contributing

Contributions are welcome! Feel free to open issues or submit pull requests.


