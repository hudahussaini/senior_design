#!/usr/bin/env python
# coding: utf-8

# In[1]:


'''
2) Check Open Alex, Crossref, Arxiv and Google Scholars for pdfs
3) if unique add to pdf storage and add name to title column 
'''
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


# In[2]:


from database.database_manager import DatabaseManager
from publication_API.crossref_api import CrossrefAPI
from publication_API.arxiv_api import ArxivAPI
from publication_API.open_alex import OpenAlex
from NLP.LDA import lda_topic_modeling

DATABASE_PATH = '/nfs/turbo/si-acastel/expert_field_project/data_pipeline/database/experts.db'

database_manager = DatabaseManager(DATABASE_PATH)
#TODO: change email before sign off
# instantiate APIs 
crossref_api = CrossrefAPI(email='hudah@umich.edu', rows=10, database_manager=database_manager)
# arxiv_api = ArxivAPI(rows=10, database_manager=database_manager)
open_alex_api = OpenAlex(database_manager=database_manager)

author_list = database_manager.get_all_authors()


# In[3]:


for author_id in author_list:
    crossref_api.api_call(author_id)
    # arxiv_api.api_call(author_id)
    open_alex_api.api_call(author_id)


# In[3]:


lda_topic_modeling(database_manager=database_manager, folder_path=ALL_PDF_FOLDER_PATH)

