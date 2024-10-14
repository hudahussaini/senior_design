#Rate Limits for this api are below:
#  -> no more than one request every three seconds
#  -> limit requests to a single connection at a time


import urllib.request
import re

author = 'Amanda Kowlski'
author_query = 'au:Amanda+Kowalski'
url = f'http://export.arxiv.org/api/query?search_query={author_query}&start=0&max_results=8'

with urllib.request.urlopen(url) as f:
    results = f.read().decode('utf-8').splitlines()    

    for i, v in enumerate(results):
        
        #print(v)
        entries = v.split('</entry>')[0]
        #entries = [f"<entry>{entry.split('</entry>')[0]}</entry>" for entry in entries]
        #print(entries)

        #this portion of code will use regular expressions to search for the authors name. Can verify from there
        expression = v
        #print(seperate_results)
        auth_pattern = r"<name>(.*?)</name>"
        href_pattern = r'''title="pdf" href="([^"]*)"'''


        href = re.search(href_pattern, expression)
        auth = re.search(auth_pattern, expression)
        
        if href:
            link = href.group(1)
            print(link)
        else:
            continue


        ''' if auth:
            name = auth.group(1)
            if name == author:
                print(name)
        else:
            continue'''



        
 