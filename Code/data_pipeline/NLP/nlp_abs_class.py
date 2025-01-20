from abc import ABC, abstractmethod

class TopicModel(ABC):
    def __init__(self, num_topics=None):
        self.num_topics = num_topics
        self.model = None
    
    @abstractmethod
    def train(self, docs):
        """Train the topic model with preprocessed documents"""
        pass
        
    @abstractmethod
    def get_topics(self):
        """Extract topics from trained model"""
        pass
