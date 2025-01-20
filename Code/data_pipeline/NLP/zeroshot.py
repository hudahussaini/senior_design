from transformers import pipeline
import pandas as pd
import nltk
from nltk.tokenize import sent_tokenize
from nltk.corpus import stopwords
from collections import Counter
import numpy as np
import logging


# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

topics = [
        "Psychology",
        "Technology",
        "Business",
        "Politics",
        "Science",
        "Healthcare",
        "Machine Learning",
        "Climate Science",
        "Neuroscience",
        "Robotics"
    ]


class ZeroShotClassifier:
    def __init__(self, model_name="facebook/bart-large-mnli", topics=topics):
        self.classifier = pipeline("zero-shot-classification", model=model_name)
        self.topics = topics
        
    def expand_topics(self, topics):
        """
        Expand topics with related terms to improve matching
        """
        topic_expansions = {
            "technology": ["tech", "software", "digital", "computing", "innovation"],
            "business": ["corporate", "commerce", "industry", "market", "economy"],
            "politics": ["government", "policy", "legislation", "diplomatic", "electoral"],
            "Psychology":[
                "abuse", 
                "aggression", 
                "violence"
                "risk factors",
                "behavior pattern", 
                "socialization",
                "intergenerational truama",
                "genetic influence",
                "environmental factors",
                "genomics",
                "proteomics",
                "computational biology",
                "systems biology",
                "molecular modeling",
                "sequence analysis",
                "biological data mining",
                "nanomaterials",
                "polymer science"],
            "Machine Learning": [
                "artificial intelligence",
                "deep learning",
                "neural networks",
                "statistical learning",
                "reinforcement learning",
                "computer vision",
                "natural language processing"
            ],
            
            "Climate Science": [
                "atmospheric science",
                "climate modeling",
                "environmental data",
                "climate change",
                "meteorology",
                "oceanography",
                "earth systems"
            ],
            
            "Neuroscience": [
                "brain imaging",
                "neural circuits",
                "cognitive science",
                "neuroplasticity",
                "computational neuroscience",
                "brain-computer interface",
                "neurological disorders"
            ],
            
            
            "Robotics": [
                "autonomous systems",
                "robot control",
                "human-robot interaction",
                "robot learning",
                "manipulation",
                "robot perception",
                "swarm robotics"
            ],
            
            "Data Science": [
                "big data",
                "data mining",
                "predictive analytics",
                "statistical analysis",
                "data visualization",
                "exploratory analysis",
                "data engineering"
            ],
            
            "Biotechnology": [
                "genetic engineering",
                "synthetic biology",
                "tissue engineering",
                "biomaterials",
                "drug delivery",
                "therapeutic development",
                "bioprocessing"
            ],
            
            "Network Science": [
                "complex networks",
                "graph theory",
                "social network analysis",
                "network security",
                "distributed systems",
                "network protocols",
                "wireless networks"
            ],
            
            "High Performance Computing": [
                "parallel computing",
                "distributed computing",
                "GPU computing",
                "cloud computing",
                "supercomputing",
                "computational optimization",
                "scalable algorithms"
            ],
            
            "Applied Mathematics": [
                "optimization",
                "numerical analysis",
                "differential equations",
                "mathematical modeling",
                "computational mathematics",
                "dynamical systems",
                "mathematical physics"
            ],
            
            "Medical Imaging": [
                "image processing",
                "MRI",
                "CT scanning",
                "ultrasound",
                "radiological imaging",
                "medical image analysis",
                "imaging informatics"
            ],
            
            "Renewable Energy": [
                "solar energy",
                "wind power",
                "energy storage",
                "smart grid",
                "sustainable energy",
                "energy efficiency",
                "green technology"
            ],
            
            "Computational Chemistry": [
                "molecular dynamics",
                "quantum chemistry",
                "chemical modeling",
                "drug design",
                "molecular simulation",
                "computational spectroscopy",
                "chemical informatics"
            ]

        }
        expanded_topics = []
        for topic in topics:
            topic_lower = topic.lower()
            expanded_topics.append(topic)
            if topic_lower in topic_expansions:
                expanded_topics.extend(topic_expansions[topic_lower])
                
        return list(set(expanded_topics))
    
    def get_document_summary(self, text, max_sentences=3):
        """
        Extract key sentences from the document
        """
        # Tokenize into sentences
        sentences = sent_tokenize(text)
        
        if len(sentences) <= max_sentences:
            return text
            
        # Get word frequencies
        words = text.lower().split()
        word_freq = Counter(words)
        
        # Score sentences based on word importance
        sentence_scores = {}
        for sentence in sentences:
            score = sum(word_freq[word.lower()] for word in sentence.split() 
                       if word.lower() not in self.stop_words)
            sentence_scores[sentence] = score
            
        # Get top sentences
        top_sentences = sorted(sentence_scores.items(), 
                             key=lambda x: x[1], 
                             reverse=True)[:max_sentences]
        
        # Reconstruct text in original order
        summary_sentences = [sentence for sentence, score in sorted(top_sentences, 
                           key=lambda x: sentences.index(x[0]))]
        
        return ' '.join(summary_sentences)
    
    def classify_with_confidence_threshold(self, documents, confidence_threshold=0.3):
        """
        Classify documents with confidence thresholding and multiple passes
        """
        expanded_topics = self.expand_topics(self.topics)
    
        # Get document summary for long texts
        if len(documents.split()) > 200:
            summary = self.get_document_summary(documents)
        else:
            summary = documents
        
        # First pass with expanded topics
        result = self.classifier(summary, expanded_topics, multi_label=False)
        
        # If confidence is low, try with original topics
        if result['scores'][0] < confidence_threshold:
            result = self.classifier(summary, topics, multi_label=False)
        
        # Get top 3 predictions for analysis
        top_predictions = list(zip(result['labels'][:3], result['scores'][:3]))
        
        # Map back to original topics if using expanded topics
        predicted_topic = result['labels'][0]
        for orig_topic in topics:
            if predicted_topic.lower() in self.expand_topics([orig_topic]):
                predicted_topic = orig_topic
                break
        
        results = {
            'document': documents[:100] + '...' if len(documents) > 100 else documents,
            'predicted_topic': predicted_topic,
            'confidence': f"{result['scores'][0]:.2%}",
            'alternative_topics': [f"{label} ({score:.2%})" for label, score in top_predictions[1:]]
        }
    
        return pd.DataFrame(results)
    
    def analyze_classification_quality(self, results_df):
        """
        Analyze the quality of classifications
        """
        confidences = [float(conf.strip('%')) / 100 for conf in results_df['confidence']]
        
        analysis = {
            'mean_confidence': f"{np.mean(confidences):.2%}",
            'low_confidence_docs': len([c for c in confidences if c < 0.5]),
            'topic_distribution': results_df['predicted_topic'].value_counts().to_dict()
        }
        
        return analysis

    
    def log_topics(self, results_df, quality_analysis):
        logging.info("\nEnhanced Zero-Shot Classification Results:")
        logging.info(results_df.to_string(index=False))
        logging.info("\nClassification Quality Analysis:")
        logging.info(quality_analysis)

        