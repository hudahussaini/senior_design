import os
from pypdf import PdfReader 

directory = 'James Wagner Publications'

reader = PdfReader('smu009.pdf') 
  
# printing number of pages in pdf file 
pdfLength = (len(reader.pages)) 

page = reader.pages[0]
text = page.extract_text()
print(pdfLength)

'''
number_of_pages = len(reader.pages)
page = reader.pages[0]
text = page.extract_text()
'''


file = ""
for i in range(0, pdfLength):
    page = reader.pages[i]
    file += page

print(file)

# creating a page object 
#page = reader.pages[:]
        
# extracting text from page 
#print(page.extract_text())

'''for i in os.listdir(directory):
    name = os.path.splitext(i)[0]
    ext = os.path.splitext(i)[1]

    if name == 'smu009':'''
        
        

        
