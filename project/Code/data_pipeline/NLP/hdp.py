import tomotopy as tp
import logging
# from nlp_abs_class import TopicModel

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# from abc import ABC, abstractmethod

# class TopicModel(ABC):
#     def __init__(self, num_topics=None):
#         self.num_topics = num_topics
#         self.model = None
    
#     @abstractmethod
#     def train(self, docs):
#         """Train the topic model with preprocessed documents"""
#         pass
        
#     @abstractmethod
#     def get_topics(self):
#         """Extract topics from trained model"""
#         pass

class HDPTopicModel():
    def __init__(self, tw=tp.TermWeight.IDF, min_cf=5, rm_top=7, gamma=1, alpha=0.1, initial_k=10, seed=99999):
        # super().__init__(num_topics)
        self.model = tp.HDPModel(
            tw=tw, min_cf=min_cf, rm_top=rm_top,
            gamma=gamma, alpha=alpha, initial_k=initial_k, seed=seed
        )

    def train(self, docs, mcmc_iter=1000, burn_in=100):
        # Add documents to the HDP model
        for vec in docs:
            self.model.add_doc(vec)

        # Perform burn-in
        self.model.burn_in = burn_in
        self.model.train(0)
        
        # Perform training iterations
        for i in range(0, mcmc_iter, 100):
            self.model.train(100, workers=3)
            logging.info(f"Iteration: {i}\tLog-likelihood: {self.model.ll_per_word}\tNum. of topics: {self.model.live_k}")
    
    def get_topics(self, top_n=10):
        """Extract and return the topics from the trained HDP model."""
        sorted_topics = [k for k, v in sorted(enumerate(self.model.get_count_by_topics()), key=lambda x: x[1], reverse=True)]
        topics = {}

        for k in sorted_topics:
            if not self.model.is_live_topic(k):
                continue  # Skip non-live topics
            topic_wp = [(word, prob) for word, prob in self.model.get_topic_words(k, top_n=top_n)]
            topics[k] = topic_wp  # Store topic word/frequency array

        return topics

    def log_topics(self, topics):
        for key in topics:
            logging.info(topics[key])