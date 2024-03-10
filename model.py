from openai import OpenAI
from dotenv import load_dotenv, find_dotenv
import os

_ = load_dotenv(find_dotenv())

client = OpenAI(
    # This is the default and can be omitted
    api_key=os.environ.get("OPENAI_API_KEY"),
)

def extracted_data(invoice_text):
    prompt = f"""Extract the company name from the following invoice text:\n\n{invoice_text}\n\n
                Company name:"""

    chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": prompt,
        }
    ],
    model="gpt-3.5-turbo",
    max_tokens=50,  # Adjust as needed
    temperature=0.5,
    )

    # Extracting the company name from the generated response
    company_name = chat_completion.choices[0].message.content
    print(company_name)
    return company_name