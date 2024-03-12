# Invoice Data Extraction - MODEL-3

## Overview

This project utilizes the OpenAI GPT-3.5-turbo model for extracting carrier names from multiple invoice images or PDFs.

## Benefits

- Accepts multiple PDFs or images simultaneously.
- Scanned PDFs are formatted/enhanced to provide accurate responses.

## Application

The application runs with Streamlit, providing a user-friendly interface for interacting with the model.

## Usage

### Input

- Accepts multiple invoice images or PDF files.

### Output

- Extracts the carrier/company name from the provided invoices.

## Constraints

- Only extracts the carrier/company name.

## How to Run
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

- For optimal performance, provide clear and well-scanned multiple invoice images or PDFs.

## Contributing

Contributions are welcome! Feel free to open issues or submit pull requests.


