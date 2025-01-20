import os
import json
from bertopic import BERTopic
from sentence_transformers import SentenceTransformer
from project.data_pipline.nlp import create_docs

def get_topic(folder_path):
    results = {}  # Dictionary to store results

    for author_folder in os.listdir(folder_path):
        author_folder_path = os.path.join(folder_path, author_folder)
        
        if os.path.isdir(author_folder_path):
            # Get list of PDF files for the current author
            pdf_files = [os.path.join(author_folder_path, f) for f in os.listdir(author_folder_path) 
                            if os.path.isfile(os.path.join(author_folder_path, f)) and f.endswith('.pdf')]
            
            # Create docs for the current author
            docs = create_docs(pdf_files)
            
            if not docs:
                print(f"No documents created for author: {author_folder}")
                continue
            
            # Initialize sentence transformer model
            sentence_model = SentenceTransformer("all-MiniLM-L6-v2")
            embeddings = sentence_model.encode(docs, show_progress_bar=True)
            
            if len(docs) != len(embeddings):
                raise ValueError("Mismatch between number of documents and embeddings.")
            
            # Initialize and fit BERTopic model
            model = BERTopic(n_gram_range=(1, 2), min_topic_size=5, nr_topics="auto")
            try:
                model.fit(docs, embeddings)
            except Exception as e:
                print(f"Error fitting BERTopic model for author {author_folder}: {e}")
                continue
            
            # Get detailed topic information and frequency
            topic_freq = model.get_topic_freq().to_dict()  # Convert DataFrame to dict
            topic_info = model.get_topic_info().to_dict()  # Convert DataFrame to dict
            representative_docs = model.get_representative_docs()
            
            # Store results in dictionary
            results[author_folder] = {
                "topic_freq": topic_freq,
                "topic_info": topic_info,
                "representative_docs": representative_docs
            }

    # Write results to a JSON file
    with open('topic_modeling_results.json', 'w') as f:
        json.dump(results, f, indent=4)

    return results

# Example usage
folder_path = "/Users/hudahussaini/senior_design/data/downloads"
results = get_topic(folder_path)
