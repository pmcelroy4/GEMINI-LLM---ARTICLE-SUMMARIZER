import os
from pypdf import PdfReader
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('GOOGLE_API_KEY')

genai.configure(api_key=API_KEY)

filename = input("Please provide the pdf file path and name you would like summarized: ")
print('\n')

#Opening the pdf file
pdfFileObject = open(filename, 'rb')

#Creating a pdf reader object
pdfreader = PdfReader(pdfFileObject)
text = []
summary = ''

#Store pages as a list
for i in range(len(pdfreader.pages)):
    page = pdfreader.pages[i].extract_text()
    page = page.replace('\t\r', '')
    page = page.replace('\xa0', '')
    text.append(page)

#Join multiple pages together for character limit on Gemini
def join_pages(lst, pages_to_join):
    new_list = []
    for i in range(0, len(lst), pages_to_join):
        new_list.append(' '.join(lst[i:i+pages_to_join]))
    return new_list

new_text = join_pages(text, 3)

#print(f'Original pages: {len(text)}')
#print(f'New pages: {len(new_text)}')

model = genai.GenerativeModel('gemini-1.5-pro')

def get_completion(prompt):
    response = model.generate_content(prompt)
    return response.text

for i in range(len(new_text)):
    prompt = f"""Your task is to act as a Text Summarizer.
    I will provide you text from pages of a book from beginning to end.
    Your job is to summarize the text from these pages in 100 words or less.
    Don't be conversational. I just need a concise 100 word answer.
    The text will be provided below delimited with triple back ticks.
    ```{new_text[i]}```
    """
    try:
        response = get_completion(prompt)
    except:
        response = get_completion(prompt)
    print(response)
    summary = summary + ' ' + response + '\n\n'
    