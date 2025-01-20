import os
import nltk
from nltk.corpus import stopwords
from gensim import corpora, models
import fitz  # PyMuPDF
import pyLDAvis
import pyLDAvis.gensim
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Download and configure NLTK stopwords
nltk.download('stopwords')
stop_words = stopwords.words('english')

class LDATopicModel:
    def __init__(self, num_topics=5, passes=10):
        self.num_topics = num_topics
        self.passes = passes

    def train(self, processed_docs):
        """Trains an LDA model using Gensim."""
        dictionary = corpora.Dictionary(processed_docs)
        corpus = [dictionary.doc2bow(doc) for doc in processed_docs]
        lda_model = models.LdaModel(
            corpus, num_topics=self.num_topics, id2word=dictionary, passes=self.passes
        )
        return lda_model, corpus, dictionary

    def visualize_topics(self, lda_model, corpus, dictionary, output_path):
        """Saves the LDA visualization as an HTML file."""
        vis_data = pyLDAvis.gensim.prepare(lda_model, corpus, dictionary)
        pyLDAvis.save_html(vis_data, output_path)

    def lda_topic_modeling(self, folder_path):
        """Main function to perform topic modeling for each author's PDFs."""
        lda_model, corpus, dictionary = self.train_lda_model(processed_docs)
        return lda_model, corpus, dictionary

    def get_topics(self, lda_model, num_words=10):
        """Extracts topics from the trained LDA model."""
        return lda_model.print_topics(num_words=num_words)

    def log_topics(self, topics):
        pass
            