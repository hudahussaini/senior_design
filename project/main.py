from pdf_scripts import fetch_pdf
import pandas
from APIs.crossref import use_crossref_api

directory = 'Data'

'''reader = PdfReader('smu009.pdf') '''
  
# printing number of pages in pdf file 
'''pdfLength = (len(reader.pages)) 

page = reader.pages[0]
text = page.extract_text()
print(pdfLength)
'''

def read_inital_researcher_list():
    file = pandas.read_csv('isr_faculty.csv')
    authorList = file['NameFull'].to_list()
    #print(authorList)
    #         
    outfile = open("Author List", 'a')

    for i in authorList:
        outfile.write(i + "\n")
    
    return authorList

def get_publication(list_of_authors):
    url_dict = use_crossref_api(list_of_authors, "mahreen248@gmail.com", 10)
    print(url_dict)
    #code to actually use pdf
    # for paper in url_dict:
        # content = fetch_pdf(url_dict[paper])
        #put content through model
        #store in 
    
            
list_of_authors = read_inital_researcher_list()
get_publication(list_of_authors=list_of_authors)