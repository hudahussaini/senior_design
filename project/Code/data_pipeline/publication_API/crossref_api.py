import sys
sys.path.append('/nfs/turbo/si-acastel/expert_field_project/data_pipeline/publication_API')

import requests
import logging
from base_api import BaseAPI

class CrossrefAPI(BaseAPI):
    def __init__(self, email: str, rows: int, database_manager):
        super().__init__(database_manager)
        self.email = email
        self.rows = rows

    def api_call(self, author_id):
        """Implementation of the API call for publications."""
        author_name = self.db_manager.get_author_name_by_id(author_id)
        if not author_name:
            logging.error(f"Could not find author name for author_id: {author_id}")
            return
        base_url = 'https://api.crossref.org/works'
        params = {
            'query.author': author_name,
            'rows': self.rows,
            'mailto': self.email
        }
        logging.info('Searching for publications using crossref started...')
        response = requests.get(base_url, params=params)
        if response.status_code == 200:
            crossref_response = response.json()
            items = crossref_response.get('message', {}).get('items', [])
            for item in items:
                publication = {
                    'doi': item.get('DOI', 'No DOI'),
                    'title': item.get('title', ['No title'])[0],
                    'author_id': author_id,
                    'url': item.get('link', [{}])[0].get('URL', 'No URL')
                }
                # Attempt to download the PDF if a URL is available
                if publication['url'] != 'No URL':
                    if self.download_pdf(publication['url'], publication['author_id']):
                        self.check_for_duplicates(author_name, publication)
                else:
                    logging.info(f"No URL - skipping publication {publication['title']}")
        else:
            logging.error(f"Error: {response.status_code} with parameters: {params}")

