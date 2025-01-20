## Senior Design Project
Expert field modeling capstone project

## How to run 

Currently for the demo it uses Bhirhanu Eshete but you can replace with another author wherever Bhirhanu's name is. Also replace my path with yours. 


for one author:
get_all_pdfs_from_experts_for_one_author("AUTHOR_FIRST_NAME AUTHOR_LAST_NAME")




# Tasks

Data Collection: Building a pipeline to gather full-text publications from various sources utilizing an API like Crossref and preprocess the data.
    Preprocess Data: Remove punctuation and non-alphabetic characters, make all words lowercase, remove stop words, lemmatization

Machine Modeling: Using NLP techniques to explore word embeddings and implement machine learning models to cluster and label researchers' expertise.
    ML Model: Both our own models and premade models like BERTopics will be explored to cluster expert topics

Database: Making a database to store information and a function to retrieve information from it
    Store: The generated topics, publications they came from, and the authors of said publications will be stored
    Retrieve: Function to retrieve the experts based on the entered topic

Optimization/Fine-Tuning: Optimization and fine-tuning involve adjusting model parameters and improving algorithmic efficiency to enhance the accuracy and performance of the NLP models in clustering and labeling researchers' expertise.

Grounding: making sure the generated expert fields are meaningful and reflective of actual academic content and researcher expertise. This means possibly meeting with researchers and exploring and implementing ML techniques like RAG.
