from urllib.parse import urlparse
from readauthors import get_authors
import wget
import urllib.request
import requests
import os
import json
import csvreader as cs



def URLParse(url):
    parsed_url = urlparse(url)
    id = parsed_url.path.split("/")[-1]
    return id

def get_institution(institution):
    if institution:
        current = institution[0].get('display_name', 'n/a')
        return current
    else:
        return 'n/a'

def get_works(name, id):    
    page = 1
    publications = []
    while True:
        url = "https://api.openalex.org/works"

        params = {
        "filter": f'author.id:{id},is_oa:true',
        "page": page,  # Start with the first page
        "per-page": 100
        }


      # Loop to handle pagination
        response = requests.get(url, params=params)

        if response.status_code == 200:
            # Parse the JSON response
            data = response.json()

            print(f'Open Access publications for {name} (Page {params["page"]}):\n')
            if 'results' in data and data['results']:
                for work in data['results']:
                    link = work['id']
                    title = work['title']
                    publications.append(link)
            else:
                print(f"{name} doesn't have open access publications")

            # Check if there is another page of results
            if 'meta' in data and data['meta'].get('next_url'):
                page += 1  # Increment to the next page
            else:
                break  # No more pages, break the loop
        else:
            print(f'Failed to retrieve data. HTTP status code: {response.status_code}')
            break  # Break the loop on failure

    return publications

def download_pdfs(name, url, title):    
    file_path = f'{name}'
    special_chars = ['\\', '/', ':', '*', '?', '"', '<', '>', '|', '#', '&', '=']
    safe_title = title

    for i in special_chars:
        if i in safe_title:
            safe_title = safe_title.replace(i, '-')
    
    safe_title = f'{safe_title}.pdf'
    full_file_path = os.path.join(file_path, safe_title)

    try:
        if not os.path.exists(file_path):
            os.makedirs(file_path)
            # Download the PDF and save it to the specified path
        if os.path.exists(full_file_path):
            print(f'{safe_title} already downloaded')
        #alternative = wget.download(url, out = full_file_path)
        urllib.request.urlretrieve(url, full_file_path)
        #print(f"PDF downloaded and saved as {full_file_path}\n")

    except Exception as e:
        #alternative = wget.download(url, out = full_file_path)
        print(f"{e}\n")
    return f'Downloaded {title}\n'

'''
This is a wAAAAAAY faster option to gather publication hrefs
'''
def api_works(name, url):
    # Loop to handle pagination
    response = requests.get(url)
    try:
        if response.status_code == 200:

            data = response.json()  
            location = data.get('locations', [])
            title = data.get('title')
            
            for results in location:
                if results['is_oa'] == True:                    
                    if results['pdf_url']: 
                        download_pdfs(name, results['pdf_url'], title)
                        break
                        #return f"{results['pdf_url']}, {title}"        
                        #print(results['pdf_url'])
                    elif results['landing_page_url']: 
                        download_pdfs(name, results['landing_page_url'], title)
                        break
    except Exception as e:
        print(f'error occured with {url}: {e}')
    
    return 'Next publication\n'
    
def GatherAuthors(authors):
    #setting API author endpoint
    url = "https://api.openalex.org/authors"

    unverified = {}
    verified = {}
    for i in range(0, len(authors)):
        # Set the search parameters
        params = {
            "filter": f'display_name.search:{authors[i]}',
            "per_page": 1,  # Limit results per page
            "page": 1       # Get the first page of results
        }

        # Send the GET request to the API
        response = requests.get(url, params=params)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            data = response.json()

            if 'results' in data and data['results']:
                for author in data['results']:
                    author_name = author['display_name']                
                    id = URLParse(author['id'])
                    institution = get_institution(author.get('last_known_institutions', []))
                    works_count = author['works_count']
                    if 'University of Michigan–Ann Arbor' in institution:
                        verified[author_name] = {
                            'id': id,
                            'institution': institution
                        }
                    elif 'Univeristy of Michigan-Ann Arbor' not in institution:
                        unverified[author_name] = {
                            'id':id,
                            'institution': institution
                        }
            else:
                continue
        else:
            print(f"Failed to retrieve data. HTTP Status code: {response.status_code}") 
    with open('verified', 'w') as file:
        json.dump(verified, file)
    
    with open('unverified', 'w') as unfile:
        json.dump(unverified, unfile)

    return f'Gathered Authors' 

if __name__ == '__main__':
    authors = get_authors()['NameFull']
    '''
    Uncomment when running the first time.
    Comment after running
    '''
    #GatherAuthors(authors)

    with open('verified', 'r') as verified:
        #Getting ID's to use for next loop
        verified = json.load(verified)
        #print(type(verified))
        works = {}
        i=0
        for names, values in verified.items():
            result = get_works(names, values['id'])                       
            works[names] = result
            break

        #Collecting the works per author
        for name, links in works.items():
            for i in links:
                id = URLParse(i)
                api_works(name, f'https://api.openalex.org/works/{id}')
        
    '''isr_titles = []
    for i in cs.data['Title']:
        isr_titles.append(i)

    with open('unverified', 'r') as unverified:
        unverified = json.load(unverified)

        works = {}
        for names, values in unverified.items():            
            result = get_works(names, values['id'])                       
            for i in result:
                id = URLParse(i)
                titles = api_works(names, f'https://api.openalex.org/works/{id}')
                if titles in isr_titles:
                    print(names, titles)'''