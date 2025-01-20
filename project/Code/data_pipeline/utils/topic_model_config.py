from pathlib import Path
import yaml

# Define default values for global variables
EMAIL = None
DATABASE_PATH = None
ALL_PDF_FOLDER_PATH = None
MODEL = None
AUTHOR_NAME = None

# Load the config file and set global variables
def load_config(file_path=None):
    global EMAIL, DATABASE_PATH, ALL_PDF_FOLDER_PATH, MODEL, AUTHOR_NAME
    
    # Set the default path for config.yaml if no file_path is provided
    if file_path is None:
        file_path = Path(__file__).parent.resolve() / 'config.yaml'
    
    with open(file_path, 'r') as file:
        config = yaml.safe_load(file)
    
    # Set the global variables
    EMAIL = config.get('email')
    DATABASE_PATH = config.get('database_path')
    ALL_PDF_FOLDER_PATH = config.get('all_pdf_folder_path')
    MODEL = config.get('model').lower().strip()
    AUTHOR_NAME = config.get('author')

# Automatically load config when the module is imported
load_config()
