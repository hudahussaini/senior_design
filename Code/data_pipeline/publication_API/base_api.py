import os
import requests
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class BaseAPI:
    def __init__(self, database_manager):
        self.db_manager = database_manager

    #TODO: change name to show it adds too
    def check_for_duplicates(self, author_id, publication):
        """Check for duplicates in the database and add if not found."""
        try:
            self.db_manager.add_publication(publication)
            logging.info(f"Unique publication : {publication['title']}")
            #not a duplicate
            return False
        except Exception as e:
            logging.info(f"Likley a Duplicate : {publication['title']}")
            return True


    def download_pdf(self, url, author_id):
        """
        Download a PDF from the given URL, save it to a directory named after the author ID.
        Confirms the content type and header to ensure the file is a PDF.
        """
        # Setup directory path
        base_path = '/nfs/turbo/si-acastel/expert_field_project/full_pdfs_by_author'
        save_directory = os.path.join(base_path, str(author_id))
        
        # Create directory if it doesn't exist
        os.makedirs(save_directory, exist_ok=True)
        try:
            # Perform HEAD request to verify the URL points to a PDF
            response = requests.head(url, allow_redirects=True, timeout=10)
            if 'application/pdf' not in response.headers.get('Content-Type', '').lower():
                logging.info(f'HEAD request could not confirm PDF content at {url}, attempting GET.')
            
            # Attempt to get a portion of the file to confirm PDF header
            response = requests.get(url, stream=True, timeout=10)
            if response.status_code != 200:
                logging.warning(f'Failed to download PDF, status code: {response.status_code}')
                return False

            # Get filename from URL or use default if empty
            filename = url.split('/')[-1]
            if not filename.endswith('.pdf'):
                filename += '.pdf'
            file_path = os.path.join(save_directory, filename)
            
            # Skip download if file already exists
            if os.path.exists(file_path):
                logging.info(f'PDF already exists at {file_path}, skipping download.')
                return False

            logging.info(f'Downloading PDF from {url} to {file_path}')
            
            # Download and write to file in chunks
            with open(file_path, 'wb') as file:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:  # Write each chunk to file
                        file.write(chunk)
            
            # Confirm file size after writing; if 0 bytes, consider it a failed download
            if os.path.getsize(file_path) == 0:
                logging.warning(f'Downloaded file at {file_path} is empty. Removing file.')
                os.remove(file_path)
                return False
            
            logging.info(f'Successfully downloaded PDF to {file_path}')
            return True

        except requests.Timeout:
            logging.warning(f"Timeout while attempting to download PDF from {url}")
            return False
        except requests.RequestException as e:
            logging.warning(f"Request error occurred: {e}")
            return False
        except IOError as e:
            logging.warning(f"File error while saving PDF: {e}")
            return False
        except Exception as e:
            logging.warning(f"Unexpected error: {e}")
            return False

        def api_call(self, author_id, publication):
            """Simulate an API call, to be implemented by subclasses."""
            raise NotImplementedError("Subclasses should implement this method.")

