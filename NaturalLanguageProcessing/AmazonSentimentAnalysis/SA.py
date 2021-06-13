import re
import time
import random
import numpy as np 
import pandas as pd
import pickle
import sklearn
from collections import defaultdict
import contractions
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.stem.snowball import SnowballStemmer
from nltk.stem import WordNetLemmatizer 
from sklearn import metrics
from sklearn.linear_model import LogisticRegression, SGDClassifier
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.naive_bayes import MultinomialNB
from sklearn.ensemble import RandomForestClassifier

lemmatizer = WordNetLemmatizer()
ps = PorterStemmer() 
stemmer = SnowballStemmer("english")
stop_words = set(stopwords.words('english'))


class Sentiment_Analyzer():
    def __init__(self):
        self.load_LDA_Weights()
        self.load_SA_Model()
        self.load_vectorizer()
    
    @staticmethod
    def apply_negation(review):
        review = re.sub(' +', ' ', review)
        negation, delims, result, deleted_delim, words = False, "?.,!:;", [], False, review.split(" ")
        only_letter_pattern = re.compile('[^a-zA-Z]')
        for word in words:
            if (word not in stop_words) or (word == 'not' or word == 'no'):
                if any(delim in word for delim in delims):
                    deleted_delim = True
                cleaned_word = only_letter_pattern.sub('', word).lower()
                negated = "not_" + cleaned_word if negation else cleaned_word
                if ((len(negated) >= 3 and 'not_' not in negated) or ('not_' in negated and len(negated) >= 7)) and len(negated) <= 25:
                    result.append(negated)
                if any(neg in word for neg in ["not", "no"]):
                    negation = not negation
                if deleted_delim:
                    negation = False
                    deleted_delim = False
        return result
    
    @staticmethod
    def edit(review):
        only_letter_pattern, words, results = re.compile('[^a-zA-Z]'), review.split(" "), []
        for word in words:
            if word not in stop_words:
                if len(word) >= 3 and len(word) <= 25:
                    cleaned_word = only_letter_pattern.sub('', word).lower()
                    results.append(cleaned_word)
        return results
        
    
    def normalize_text(self, list_of_reviews, Negate = False):
        results = []
        for i, review in enumerate(list_of_reviews):
            token_roots = []
            lower_cased_review = review.lower()
            tokenized_review = lower_cased_review.split(" ")          
            for token in tokenized_review:
                token_roots.append(lemmatizer.lemmatize(stemmer.stem(token)))
            decontracted_review = contractions.fix(" ".join(token_roots))
            if Negate:
                decontracted_review = self.apply_negation(decontracted_review)
            else:
                decontracted_review = self.edit(decontracted_review)
            results.append(decontracted_review)
        return results
    
    def load_LDA_Weights(self):
        with open("NormalizedLDAW.pickle",'rb') as f:
            self.ldaw = pickle.load(f)
        return None
    
    def load_SA_Model(self):
        with open("LRNegModel.pickle",'rb') as f:
            self.SentimentAnalyzer = pickle.load(f)
        return None
    
    def load_vectorizer(self):
        with open("vectorizer.pickle",'rb') as f:
            self.vectorizer = pickle.load(f)
        return None
        
    
    def find_topic(self, review):
        normalized_review = self.normalize_text(review)[0]
        topic_scores, topic_names = [0,0,0,0,0],['iphone','battery&charge','screen','phone case','product&usability']
        for token in normalized_review:
            results = self.ldaw.loc[self.ldaw['word'] == token]
            for i, score in enumerate(list(results['relevance'])):
                topic_scores[i] += score
        maxValueIndex = np.argmax(topic_scores)
        print(topic_scores)
        return topic_names[maxValueIndex]
    
    def find_sentiment_Score(self, review):
        normalized_review = self.normalize_text(review, Negate = True)[0]
        transformed_vectorized_review = self.vectorizer.transform([" ".join(normalized_review)])
        sentiment_result = list(self.SentimentAnalyzer.predict(transformed_vectorized_review))[0]
        sentiment_probabilities = self.SentimentAnalyzer.predict_proba(transformed_vectorized_review)
        case_prob, sentiment_score = None, None
        if sentiment_result == 'negative':
            case_prob = sentiment_probabilities[0][0]
            sentiment_score = 5 - (4*case_prob)
        else:
            case_prob = sentiment_probabilities[0][1]
            sentiment_score = 1 + (4*case_prob)
        return sentiment_result, sentiment_score
            
        