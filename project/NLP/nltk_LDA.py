import os
import nltk
from nltk.corpus import stopwords
from gensim import corpora, models
import fitz  # PyMuPDF
import pyLDAvis
import pyLDAvis.gensim

nltk.download('stopwords')
stop_words = stopwords.words('english')

def create_docs(pdf_files):
    docs = []
    for pdf_file in pdf_files:
        with fitz.open(pdf_file) as pdf:
            text = ""
            for page_num in range(len(pdf)):
                page = pdf.load_page(page_num)
                text += page.get_text()
            docs.append(text)
    return docs

def preprocess_documents(docs):
    processed_docs = []
    for doc in docs:
        tokens = nltk.word_tokenize(doc.lower())
        tokens = [word for word in tokens if word.isalpha() and word not in stop_words]
        processed_docs.append(tokens)
    return processed_docs

def lda_topic_modeling(folder_path, num_topics=5):
    results = {}
    for author_folder in os.listdir(folder_path):
        author_folder_path = os.path.join(folder_path, author_folder)
        if os.path.isdir(author_folder_path):
            pdf_files = [os.path.join(author_folder_path, f) for f in os.listdir(author_folder_path)
                         if os.path.isfile(os.path.join(author_folder_path, f)) and f.endswith('.pdf')]
            docs = create_docs(pdf_files)
            processed_docs = preprocess_documents(docs)
            
            # Create a dictionary and corpus
            dictionary = corpora.Dictionary(processed_docs)
            corpus = [dictionary.doc2bow(doc) for doc in processed_docs]
            
            # Build LDA model
            lda_model = models.LdaModel(corpus, num_topics=num_topics, id2word=dictionary, passes=10)
            # Prepare data for pyLDAvis visualization
            vis_data = pyLDAvis.gensim.prepare(lda_model, corpus, dictionary)
            # pyLDAvis.enable_notebook()  # Enable for Jupyter notebook
            # OR
            pyLDAvis.save_html(vis_data, f'/Users/hudahussaini/senior_design/data/downloads/{author_folder}/lda_visualization.html')  # Save to standalone HTML

            # Get topics
            topics = lda_model.print_topics(num_words=10)
            results[author_folder] = topics
            print(f"Author: {author_folder}")
            for topic in topics:
                print(topic)
    return results

# Example usage
folder_path = "/Users/hudahussaini/senior_design/data/downloads"
results = lda_topic_modeling(folder_path)
