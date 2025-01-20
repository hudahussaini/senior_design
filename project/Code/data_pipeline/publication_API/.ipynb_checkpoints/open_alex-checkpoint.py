#API Open Alex
from urllib.parse import urlparse
import urllib.request
import requests
import os
import json
from publication_API.base_api import BaseAPI
import logging

class OpenAlex(BaseAPI):
    def __init__(self, database_manager):
        super().__init__(database_manager)

    def api_call(self, author_id):
        """Implementation of the API call for publications."""
        author_name = self.db_manager.get_author_name_by_id(author_id)
        if not author_name:
            logging.error(f"Could not find author name for author_id: {author_id}")
            return
        url = "https://api.openalex.org/authors"
        params = {
            "filter": f'display_name.search:{author_name},is_oa:true',
            "per_page": 1,  # Limit results per page
            "page": 1       # Get the first page of results
        }
        logging.info('Searching for publications using Open Alex started...')
        # Send the GET request to the API
        response = requests.get(url, params=params)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            meta_data = response.json()
            work_response = requests.get(meta_data['results'][0]['works_api_url'], params=params)
            data = work_response.json()
            if 'results' in data and data['results']:
                for result in data['results']:
                    if 'key' in result:
                        print("pass")
                    if 'best_oa_location' in result and result['best_oa_location']:
                        pdf_url = result['best_oa_location'].get('pdf_url')
                    # If no PDF URL in best_oa_location, try locations
                    if pdf_url is None and 'locations' in result:
                        for location in result['locations']:
                            if location.get('pdf_url'):
                                pdf_url = location['pdf_url']
                                break
                    doi_url = result.get('doi')
                    doi_number = doi_url.replace('https://doi.org/', '')

                    publication = {
                        'doi': doi_number,
                        'title': result.get('title') or result.get('display_name'),
                        'author_id': author_id,
                        'url': pdf_url
                    }
                    if publication['url']:
                        if self.check_for_duplicates(author_name, publication) or not self.download_pdf(publication['url'], publication['author_id']):
                            logging.warning(f"Skipping publication - either duplicate or download failed: {publication['title']}")
                        else:
                            logging.info(f"Successfully processed unique publication: {publication['title']} by {publication['author_id']}")
                    else:
                        logging.info(f"Error: Mostly Likely No URL - skipping publication {publication['title']}")
        else:
            logging.error(f"Error: {response.status_code} with parameters: {params}")