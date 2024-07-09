import os
from serpapi import GoogleSearch

#get an account here https://serpapi.com/playground?engine=google_scholar&q=author%3A+%22J+Wagner%22&hl=en
params = {
  "api_key": "",
  "engine": "google_scholar",
  "q": "author: 'J Wagner'",
  "hl": "en"
}

def use_google_scholar():
    search = GoogleSearch(params)
    results = search.get_dict()
    organic_results = results["organic_results"]
    return organic_results

def format_results(results):
    formatted = []
    for result in results:
        pdf_link = ""
        if 'resources' in result:
            for resource in result['resources']:
                if resource.get('file_format') == 'PDF':
                    pdf_link = resource['link']
                    break
        try:
          formatted.append(f"Title: {result.get('title')}\n"
                          f"Link: {result.get('link')}\n"
                          f"PDF Link: {pdf_link}\n"
                          f"Snippet: {result.get('snippet')}\n"
                          f"Authors: {', '.join([author['name'] for author in result['publication_info']['authors']])}\n"
                          f"Publication: {result['publication_info']['summary']}\n"
                          f"Cited by: {result['inline_links']['cited_by']['total']}\n"
                          f"-------------------\n")
        except:
            continue
    return "\n".join(formatted)

def get_log_filename(query):
    base_filename = query.replace(" ", "_")
    filename = f"{base_filename}.log"
    counter = 1
    while os.path.exists(filename):
        filename = f"{base_filename}{counter}.log"
        counter += 1
    return filename

def write_log_file(filename, content):
    with open(filename, 'w') as file:
        file.write(content)

def use_google_scholar_main():
    results = use_google_scholar()
    formatted_results = format_results(results)
    log_filename = get_log_filename(params["q"])
    write_log_file(log_filename, formatted_results)
    print(f"Results logged in {log_filename}")

