import nltk
from nltk.stem.snowball import SpanishStemmer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
import pandas as pd
import sqlite3

class productReccomender():

    def __init__(self):
        self.stemmer = SpanishStemmer(ignore_stopwords=True)
        self.count_vectorizer = CountVectorizer()
        self.df = self.get_data_from_db("products.db")


    def give_reccomendations(self,sentence):
        standardized_sentence = self.standardize(sentence)
        results = self.calculate_cosine_similarity(standardized_sentence, self.df)
        best_index = results[0]
        best_score = results[1][0][1]
        return best_index, best_score



    def get_data_from_db(self,file):
        db = sqlite3.connect(file)
        df = pd.read_sql_query("SELECT id,name,full_description FROM products", db)

        df['full_description'] = df['full_description'].apply(self.standardize)

        return df

    def standardize(self, sentence):
        tokenized = nltk.word_tokenize(sentence)
        stemmed_sentence = [self.stemmer.stem(word.lower()) for word in tokenized]
        return " ".join(stemmed_sentence)

    def create_dataframe(self, matrix, tokens):

        indexes = ["sentence", "comparison"]
        df = pd.DataFrame(data=matrix, index=indexes, columns=tokens)
        return df


    def calculate_cosine_similarity(self, to_compare, comparison):
        cosine_results = []

        comparison_dict = dict(list(zip(comparison['id'], comparison['full_description'])))

        for key, value in comparison_dict.items():
            comparison_list = [to_compare, value]
            vector_matrix = self.count_vectorizer.fit_transform(comparison_list).toarray()
            tokens = self.count_vectorizer.get_feature_names()

            cosine_similarity_matrix = cosine_similarity(vector_matrix)
            df = self.create_dataframe(cosine_similarity_matrix, ['sentence', 'comparison'])

            similarity_score = df.iat[0, 1]

            cosine_results.append([key, similarity_score])

        all_results = sorted(cosine_results, key=lambda x: x[1], reverse=True)
        best_result = all_results[0][0]
        return best_result, all_results
