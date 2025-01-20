import pandas
from data_pipline.webscraper import get_all_pdfs_from_experts_for_one_author


def read_inital_researcher_list(csv_path):
    file = pandas.read_csv(csv_path)
    authorList = file['NameFull'].to_list()
    #print(authorList)
    #         
    outfile = open("Author List", 'a')

    for i in authorList:
        outfile.write(i + "\n")
    
    return authorList

def get_publication(list_of_authors):
    for author in list_of_authors:
            get_all_pdfs_from_experts_for_one_author(author)

    
list_of_authors = read_inital_researcher_list('/Users/hudahussaini/senior_design/data/isr_faculty.csv')            
# list_of_authors = read_inital_researcher_list()
get_publication(list_of_authors=list_of_authors)

