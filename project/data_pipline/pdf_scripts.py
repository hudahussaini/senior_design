import io
import requests
import PyPDF2

def is_pdf_downloadable(url):
    try:
        response = requests.head(url, allow_redirects=True)
        content_type = response.headers.get('Content-Type', '').lower()
        if 'application/pdf' in content_type:
            return True
        else:
            # If HEAD request does not confirm, try a GET request
            response = requests.get(url, stream=True)
            content_type = response.headers.get('Content-Type', '').lower()
            if 'application/pdf' in content_type:
                return True
    except requests.RequestException as e:
        print(f"An error occurred: {e}")
    return False

def fetch_pdf(url):
    response = requests.get(url)
    if response.status_code == 200:
        return io.BytesIO(response.content)
    else:
        print(f"Error fetching PDF: {response.status_code}")
        return None

def read_pdf(pdf_file):
    reader = PyPDF2.PdfReader(pdf_file)
    number_of_pages = len(reader.pages)
    for page_number in range(number_of_pages):
        page = reader.pages[page_number]
        print(page.extract_text())