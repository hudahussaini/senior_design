import os
import nltk
import re
from nltk.corpus import stopwords, wordnet
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.tag import pos_tag
from gensim.models import Phrases
from gensim.models.phrases import Phraser
import fitz  # PyMuPDF
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


# Download required NLTK data
nltk.download('stopwords', quiet=True)
nltk.download('wordnet', quiet=True)
nltk.download('averaged_perceptron_tagger', quiet=True)
nltk.download('punkt', quiet=True)
nltk.download('omw-1.4', quiet=True)

class TopicModelDataPreprocessor:
    def __init__(self, min_word_length=3, remove_stopwords=True, lemmatize=True,
                 min_count=2, threshold=10):
        self.min_word_length = min_word_length
        self.remove_stopwords = remove_stopwords
        self.lemmatize = lemmatize
        self.min_count = min_count
        self.threshold = threshold

        # Set up stop words and lemmatizer
        self.stop_words = set(stopwords.words('english'))
        custom_stops = {'from', 'subject', 're', 'edu', 'use', 'nber'}
        self.stop_words.update(custom_stops)
        self.lemmatizer = WordNetLemmatizer()

    def clean_text(self, text):
        """Remove URLs, special characters, and extra whitespace."""
        text = re.sub(r'http\S+|www\S+|\S+@\S+', '', text)
        text = re.sub(r'[^a-zA-Z\s]', '', text)
        return ' '.join(text.split()).strip()

    def get_wordnet_pos(self, tag):
        """Convert Penn Treebank tags to WordNet POS tags."""
        tag_map = {
            'J': wordnet.ADJ,
            'V': wordnet.VERB,
            'N': wordnet.NOUN,
            'R': wordnet.ADV
        }
        return tag_map.get(tag[0], wordnet.NOUN)

    def preprocess_text(self, docs):
        """Tokenize, lemmatize, and clean documents, then apply bigram detection."""
        processed_docs = []
        for doc in docs:
            clean_doc = self.clean_text(doc.lower())
            tokens = word_tokenize(clean_doc)
            
            if self.lemmatize:
                pos_tags = pos_tag(tokens)
                processed_tokens = [
                    self.lemmatizer.lemmatize(token, self.get_wordnet_pos(pos))
                    for token, pos in pos_tags
                    if token.isalpha() and len(token) >= self.min_word_length
                    and (not self.remove_stopwords or token not in self.stop_words)
                ]
            else:
                processed_tokens = [
                    token for token in tokens
                    if token.isalpha() and len(token) >= self.min_word_length
                    and (not self.remove_stopwords or token not in self.stop_words)
                ]
                
            processed_docs.append(processed_tokens)
        
        # Detect and add bigrams
        bigram = Phrases(processed_docs, min_count=self.min_count, threshold=self.threshold)
        bigram_model = Phraser(bigram)
        return [bigram_model[doc] for doc in processed_docs]

    def create_docs(self, pdf_files):
        """Extract text from a list of PDF files."""
        docs = []
        for pdf_file in pdf_files:
            try:
                with fitz.open(pdf_file) as pdf:
                    text = ""
                    for page_num in range(len(pdf)):
                        page = pdf.load_page(page_num)
                        text += page.get_text()
                    docs.append(text)
            except Exception as e:
                #TODO: remove problem pdfs from folder and db
                logging.warning(f"couldn't open {pdf_file}")
        return docs

    def get_entire_author_text(self, author_folder):
        pdf_files = [file for file in author_folder.iterdir() if file.is_file() and file.suffix == '.pdf']
        raw_docs = self.create_docs(pdf_files)
        processed_docs = []
        for doc in raw_docs:
            clean_doc = self.clean_text(doc.lower())
            processed_docs.append(clean_doc)
        return " ".join(processed_docs) 

    def get_and_process_pdf_files(self, author_folder):
        """Convert PDFs to text, then preprocess and return lemmatized documents with bigrams."""
        # Loop through each author folder in the main directory
        pdf_files = [file for file in author_folder.iterdir() if file.is_file() and file.suffix == '.pdf']
        raw_docs = self.create_docs(pdf_files)
        return self.preprocess_text(raw_docs)