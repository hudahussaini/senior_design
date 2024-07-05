import os
from pypdf import PdfReader 
import pandas

directory = 'Data'

'''reader = PdfReader('smu009.pdf') '''
  
# printing number of pages in pdf file 
'''pdfLength = (len(reader.pages)) 

page = reader.pages[0]
text = page.extract_text()
print(pdfLength)
'''


file = pandas.read_csv('isr_faculty.csv')
authorList = file['NameFull'].to_list()
#print(authorList)
#         
outfile = open("Author List", 'a')

for i in authorList:
    outfile.write(i + "\n")
