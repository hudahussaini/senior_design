import sys
sys.path.append('/nfs/turbo/si-acastel/expert_field_project/data_pipeline/publication_API')



import requests
import logging
import xml.etree.ElementTree as ET
from base_api import BaseAPI
from typing import Optional, Dict, List

class ArxivAPI(BaseAPI):
    def __init__(self, rows: int, database_manager):
        super().__init__(database_manager)
        self.rows = rows
        # Define namespaces used in ArXiv API
        self.namespaces = {
            'atom': 'http://www.w3.org/2005/Atom',
            'arxiv': 'http://arxiv.org/schemas/atom'
        }

    def api_call(self, author_id: str) -> None:
        """
        Implementation of the API call for publications.
        
        Args:
            author_id (str): The ID of the author to search for
        """
        # Get author name from database
        author_name = self.db_manager.get_author_name_by_id(author_id)
        if not author_name:
            logging.error(f"Could not find author name for author_id: {author_id}")
            return

        # Construct the query URL
        author_query = 'au:' + '+'.join(author_name.split())
        url = f'http://export.arxiv.org/api/query?search_query={author_query}&start=0&max_results={self.rows}'

        try:
            logging.info('Searching for publications using Arxiv started...')
            # Make the request
            response = requests.get(url)
            response.raise_for_status()

            # Parse XML response
            root = ET.fromstring(response.content)
            # Process each entry
            entries = root.findall('atom:entry', self.namespaces)
            if not entries:
                logging.warning(f"No publications found for author: {author_name}")
                return

            for entry in entries:
                try:
                    publication = self._extract_publication_details(entry, author_id)
                    if publication:
                        if publication['url'] != 'No URL':
                            if self.download_pdf(publication['url'], publication['author_id']):
                                self.check_for_duplicates(author_name, publication)
                except Exception as e:
                    logging.error(f"Error processing entry: {str(e)}")
                    continue

        except requests.exceptions.RequestException as e:
            logging.error(f"API call failed: {e}")
        except ET.ParseError as e:
            logging.error(f"Error parsing XML response: {str(e)}")

    def _extract_publication_details(self, entry: ET.Element, author_id: str) -> Optional[Dict]:
        """
        Extract publication details from an entry element.
        
        Args:
            entry (Element): XML entry element
            author_id (str): Author identifier
            
        Returns:
            dict: Publication details or None if required fields are missing
        """
        try:
            # Extract title
            title_elem = entry.find('atom:title', self.namespaces)
            if title_elem is None or not title_elem.text:
                logging.warning("No title found for entry")
                return None
            
            # Extract ArXiv ID (DOI)
            id_elem = entry.find('atom:id', self.namespaces)
            if id_elem is None or not id_elem.text:
                logging.warning("No ID found for entry")
                return None
            
            # Extract PDF link
            pdf_link = None
            for link in entry.findall('atom:link', self.namespaces):
                if link.get('title') == 'pdf':
                    pdf_link = link.get('href')
                    break
            
            # Get DOI from ID (remove the arxiv.org prefix)
            arxiv_id = id_elem.text.split('/')[-1]
            
            return {
                'doi': arxiv_id,
                'title': title_elem.text.strip(),
                'author_id': author_id,
                'url': pdf_link if pdf_link else 'No URL'
            }
            
        except Exception as e:
            logging.error(f"Error extracting publication details: {str(e)}")
            return None

    def _get_text_safely(self, element: Optional[ET.Element]) -> str:
        """
        Safely extract text from an XML element.
        
        Args:
            element (Element): XML element
            
        Returns:
            str: Text content or empty string if element is None
        """
        return element.text.strip() if element is not None and element.text else ''