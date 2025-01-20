#API Open Alex

import sys

# Add the directory containing 'base_api.py' to sys.path
sys.path.append('/nfs/turbo/si-acastel/expert_field_project/data_pipeline/publication_API')


from urllib.parse import urlparse
import urllib.request
import requests
import os
import json
from base_api import BaseAPI
import logging

class OpenAlex(BaseAPI):
    def __init__(self, database_manager):
        super().__init__(database_manager)

    def api_call(self, author_id):
        """Implementation of the API call for publications."""
        try:
            page = 1
            author_name = self.db_manager.get_author_name_by_id(author_id)
            if not author_name:
                logging.error(f"Could not find author name for author_id: {author_id}")
                return
            url = "https://api.openalex.org/authors"
            params = {
                "filter": f'display_name.search:{author_name}',
                "per_page": 1,  
                "page": 1     
            }
            logging.info('Searching for publications using Open Alex started...')
            response = requests.get(url, params=params)
            oa_id = self.get_alex_id(author_name)
            while True:
                url = "https://api.openalex.org/works"
                params = {
                    "filter": f'author.id:{oa_id},is_oa:true',
                    "page": page,  
                    "per-page": 100
                }
                response = requests.get(url, params=params)
                logging.info(f'Open Access publications for {author_name} (Page {params["page"]}):')
                if response.status_code == 200:
                    data = response.json()
                    if 'results' in data and data['results']:
                        for work in data['results']:
                                pdf_url = None
                                if 'best_oa_location' in work:
                                    best_location = work['best_oa_location']
                                    if isinstance(best_location, dict):
                                        pdf_url = best_location.get('pdf_url')
                                
                                if not pdf_url and 'locations' in work:
                                    for location in work['locations']:
                                        if isinstance(location, dict) and location.get('pdf_url'):
                                            pdf_url = location['pdf_url']
                                            continue
                                
                                if work['doi']:
                                    doi_url = work['doi']
                                    doi_number = doi_url.replace('https://doi.org/', '')
                                else:
                                    continue

                                publication = {
                                    'doi': doi_number,
                                    'title': work['title'],
                                    'author_id': author_id,
                                    'url': pdf_url
                                }
                                if publication['url']:
                                    if self.download_pdf(publication['url'], publication['author_id']):
                                        self.check_for_duplicates(author_name, publication)
                    else:
                        logging.info(f"{author_name} doesn't have open access publications")
                    if 'meta' in data and data['meta'].get('next_url'):
                        page += 1  
                    else:
                        break  
                else:
                    logging.warning(f'Failed to retrieve data. HTTP status code: {response.status_code}')
                    break  
        except Exception as e:
            logging.warning(e)

    def get_alex_id(self, author_name):
        url = "https://api.openalex.org/authors"
        params = {
            "filter": f'display_name.search:{author_name}',
            "per_page": 1,  # Limit results per page
            "page": 1       # Get the first page of results
        }
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            return self.URLParse(data['results'][0]['id'])

    def URLParse(self, url):
        parsed_url = urlparse(url)
        id = parsed_url.path.split("/")[-1]
        return id
