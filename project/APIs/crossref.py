import requests
from project.data_pipline.pdf import *

def search_publications_by_author(author_name, email, n_rows:int):
    base_url = 'https://api.crossref.org/works'
    params = {
        'query.author': author_name,
        'rows': n_rows,  # Number of results to return
        'mailto': email
    }
    
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}")
        return None

def use_crossref_api(author_list, email, n_rows: int):
    # author_name = input("Enter the author's name: ")
    # email = input("Enter your email (required by CrossRef API): ")
    url_dict = {}
    for author in author_list:
        url_dict[author] = {}
        publications = search_publications_by_author(author, email, int(n_rows))
        if publications:
            items = publications.get('message', {}).get('items', [])
            for i, item in enumerate(items):
                title = item.get('title', ['No title'])[0]
                doi = item.get('DOI', 'No DOI')
                url = item.get('link', [{}])[0].get('URL', 'No URL')
                # print(f"{i+1}. {title} (DOI: {doi}) - URL: {url}")
                # if is_pdf_downloadable(url):
                url_dict[author][title] = url
                #     print(url)
    return url_dict
    


if __name__ == "__main__":
    use_crossref_api()
