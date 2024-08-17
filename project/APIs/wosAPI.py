import os
import time
import clarivate.wos_starter.client
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
# from webdriver_manager.chrome import ChromeDriverManager
from clarivate.wos_starter.client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://api.clarivate.com/apis/wos-starter/v1
# See configuration.py for a list of all supported configuration parameters.
configuration = clarivate.wos_starter.client.Configuration(
    host = "https://api.clarivate.com/apis/wos-starter/v1"
)

# Configure API key authorization: ClarivateApiKeyAuth
configuration.api_key['ClarivateApiKeyAuth'] = "13914ebd7e410adec9aa6b4b44d63247f2dc7e97"

# Enter a context with an instance of the API client
with clarivate.wos_starter.client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = clarivate.wos_starter.client.DocumentsApi(api_client)
    q = 'AU=Wagner+James+R' # str | Web of Science advanced [advanced search query builder](https://webofscience.help.clarivate.com/en-us/Content/advanced-search.html). The supported field tags are listed in description.
    db = 'WOS' # str | Web of Science Database abbreviation * WOS - Web of Science Core collection * BIOABS - Biological Abstracts * BCI - BIOSIS Citation Index * BIOSIS - BIOSIS Previews * CCC - Current Contents Connect * DIIDW - Derwent Innovations Index * DRCI - Data Citation Index * MEDLINE - MEDLINE The U.S. National Library of Medicine® (NLM®) premier life sciences database. * ZOOREC - Zoological Records * PPRN - Preprint Citation Index * WOK - All databases  (optional) (default to 'WOS')
    limit = 10 # int | set the limit of records on the page (1-50) (optional) (default to 10)
    page = 1 # int | set the result page (optional) (default to 1)
    sort_field = 'LD+D' # str | Order by field(s). Field name and order by clause separated by '+', use A for ASC and D for DESC, ex: PY+D. Multiple values are separated by comma. Supported fields:  * **LD** - Load Date * **PY** - Publication Year * **RS** - Relevance * **TC** - Times Cited  (optional)
    modified_time_span = None # str | Defines a date range in which the results were most recently modified. Beginning and end dates must be specified in the yyyy-mm-dd format separated by '+' or ' ', e.g. 2023-01-01+2023-12-31. This parameter is not compatible with the all databases search, i.e. db=WOK is not compatible with this parameter. (optional)
    tc_modified_time_span = None # str | Defines a date range in which times cited counts were modified. Beginning and end dates must be specified in the yyyy-mm-dd format separated by '+' or ' ', e.g. 2023-01-01+2023-12-31. This parameter is not compatible with the all databases search, i.e. db=WOK is not compatible with this parameter. (optional)
    detail = None # str | it will returns the full data by default, if detail=short it returns the limited data (optional)

    try:
        # Query Web of Science documents 
        
        api_response = api_instance.documents_get('AU=Wagner+James+R', db=db, limit=10, page=page, sort_field=sort_field,
                                                  modified_time_span=modified_time_span,
                                                  tc_modified_time_span=tc_modified_time_span, detail=detail)
        documents_list_dict = api_response.to_dict()
        
        results = documents_list_dict["hits"]
        # link = results[1]['links']['record']
        print(results)
                
        '''
        This section is intended to accept the cookies of the pdf website link.
        **************************STILL IN PROGRESS***************************
        
        
        link = 'https://www.webofscience.com/api/gateway?GWVersion=2&SrcApp=michiganexperts2024&SrcAuth=WosAPI&KeyUT=WOS:001047718300004&DestLinkType=FullRecord&DestApp=WOS_CPL'

        options = webdriver.ChromeOptions()
        service = Service(executable_path=r"C:/Program Files/driver/chromedriver.exe")

        driver = webdriver.Chrome(service=service, options=options)

        #Due to the use of the webdriver, cookies need to be accepted
        driver.get(link)
        driver.maximize_window()
        
        cookies = driver.find_element(By.XPATH, '//button[text()="Manage cookie preferences"]')

        cookies.click()
        
        input("Press enter to close the browser.......")
        '''

    except ApiException as e:
        print("Exception when calling DocumentsApi->documents_get: %s\n" % e)





