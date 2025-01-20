import os
import logging
import fitz  # PyMuPDF
import nltk
import string
from collections import defaultdict
from bertopic import BERTopic
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sentence_transformers import SentenceTransformer
from umap import UMAP

# Download necessary NLTK data
nltk.download('wordnet')
nltk.download('punkt')
nltk.download('stopwords')

class DocumentProcessor:
    """Processes PDF documents: reading and preprocessing text."""
    def __init__(self):
        self.lemmatizer = WordNetLemmatizer()
        self.stop_words = set(stopwords.words('english'))

    def read_pdf(self, file_path):
        """Reads and extracts text from a PDF file."""
        text = ""
        with fitz.open(file_path) as doc:
            for page_num in range(doc.page_count):
                text += doc[page_num].get_text("text").lower()
        return text

    def preprocess_text(self, text):
        """Tokenizes, lemmatizes, and removes stop words from the text."""
        tokens = word_tokenize(text)
        processed = [
            self.lemmatizer.lemmatize(token.lower())
            for token in tokens
            if len(token) > 4 and token.isalpha() and token not in string.punctuation and token not in self.stop_words
        ]
        return " ".join(processed)

    def create_docs(self, file_names, dir_path):
        """Processes all documents in a directory."""
        docs = []
        for file in file_names:
            try:
                text = self.read_pdf(os.path.join(dir_path, file))
                preprocessed_text = self.preprocess_text(text)
                docs.append(preprocessed_text)
            except Exception as e:
                logging.error(f"Error processing {file}: {e}")
        return docs

class BERTTopicModel:
    """Performs topic modeling using BERTopic."""
    def __init__(self):
        self.model = None
        self.sentence_model = SentenceTransformer('all-MiniLM-L6-v2')

    def fit(self, docs):
        """Fits a BERTopic model to the provided documents."""
        num_docs = len(docs)
        logging.info(f"Number of documents: {num_docs}")

        if num_docs < 2:
            logging.warning("Not enough documents for topic modeling.")
            return None, None

        # Generate embeddings
        embeddings = self.sentence_model.encode(docs)
        logging.info(f"Embedding shape: {embeddings.shape}")

        # Small dataset logic: Skip UMAP
        if num_docs <= 5:
            logging.info("Fewer than or equal to 5 documents - skipping UMAP.")
            self.model = BERTopic()
        else:
            n_neighbors = min(15, max(2, num_docs - 1))
            n_components = min(5, num_docs - 1)
            logging.info(f"UMAP configured with n_neighbors={n_neighbors}, n_components={n_components}")
            umap_model = UMAP(n_neighbors=n_neighbors, n_components=n_components, random_state=42)
            self.model = BERTopic(umap_model=umap_model, top_n_words=10)

        # Fit the model
        topics, probs = self.model.fit_transform(docs)
        return topics, probs

    def get_topic_info(self):
        """Retrieves information about the topics from the trained model."""
        if self.model:
            return self.model.get_topic_info()
        return {}

class AuthorProcessor:
    """Processes documents by author and applies topic modeling."""
    def __init__(self, base_path):
        self.base_path = base_path
        self.document_processor = DocumentProcessor()
        self.model = BERTTopicModel()
        self.docs_dict = defaultdict(list)

    def collect_documents(self):
        """Collects all PDF file names for each author."""
        for author in os.listdir(self.base_path):
            author_path = os.path.join(self.base_path, author)
            if os.path.isdir(author_path):
                self.docs_dict[author] = [file for file in os.listdir(author_path)]
        return self.docs_dict

    def process_authors(self, author_name=None):
        """Processes a specific author or all authors and performs topic modeling."""
        self.collect_documents()

        if author_name:
            # If a specific author is specified, process only that author
            if author_name in self.docs_dict:
                files = self.docs_dict[author_name]
                author_path = os.path.join(self.base_path, author_name)
                docs = self.document_processor.create_docs(files, author_path)

                if len(docs) < 10:
                    logging.warning(f"Skipping {author_name} due to insufficient documents.")
                    return

                logging.info(f"Running BERT on {author_name}")
                topics, probs = self.model.fit(docs)
                topic_info = self.model.get_topic_info()
                logging.info(f"Topics for {author_name}: {topic_info}")
            else:
                logging.warning(f"Author {author_name} not found in the directory.")

def main():
    #print("you're in BERT!")
    logging.basicConfig(level=logging.INFO)
    base_path = r'/nfs/turbo/si-acastel/expert_field_project/full_pdfs_by_author/'
    author_processor = AuthorProcessor(base_path)
    
    # To process a specific author, specify their name
    author_name = "huesmann"  # Replace with the actual author name
    author_processor.process_authors(author_name=author_name)
