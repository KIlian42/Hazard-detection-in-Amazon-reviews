import spacy
import numpy as np
import pandas as pd
import re
nlp = spacy.load('en_core_web_lg-3.0.0/en_core_web_lg/en_core_web_lg-3.0.0')

from pprint import pprint
import gensim

def lemmatizer(text):
    doc = nlp(str(text))
    text = ' '.join([token.lemma_ if token.lemma_ != '-PRON-' else token.text for token in doc])
    return text

def stop_word_remover(text):
    doc = nlp(str(text))
    text = ' '.join([token.text for token in doc if token.is_stop == False])
    return text

def origin_preprocessing(text):
    # (1) Removing leading and ending whitespaces
    preprocessed_text = text.strip()

    # (2) Replacing multiple spaces with a single space
    preprocessed_text = re.sub(' +', ' ', text)

    # (3) First regard special characters as different words
    preprocessed_text = re.sub('(?<=\w)([!?,.])', r' \1', preprocessed_text)
    preprocessed_text = preprocessed_text.replace('-', ' - ')
    preprocessed_text = preprocessed_text.replace(':', ' : ')
    origin_text = preprocessed_text.split(" ")
    origin_text_preprocessed = []
    for i in origin_text:
        if i != '':
            origin_text_preprocessed.append(i)

    return origin_text_preprocessed

def sentence_preprocess(text):
    # (1) Removing leading and ending whitespaces
    preprocessed_text = text.strip()

    # (2) Replacing multiple spaces with a single space
    preprocessed_text = re.sub(' +', ' ', preprocessed_text)

    # (3) First regard special characters as different words
    preprocessed_text = re.sub('(?<=\w)([!?,.])', r' \1', preprocessed_text)
    preprocessed_text = preprocessed_text.replace('-', ' - ')
    preprocessed_text = preprocessed_text.replace(':', ' : ')

    # (4) Lowercase
    preprocessed_text = preprocessed_text.lower()

    # (5) Lemmatize
    preprocessed_text = lemmatizer(preprocessed_text)

    # (6) Tokenize into words.
    words = preprocessed_text.split(' ')
    words_preprocessed = []
    for i in words:
        if i != '':# and i != ',' and i != '.' and i != ':':
            words_preprocessed.append(i)

    return words_preprocessed

def text_to_vector(text, model):
    vector = np.zeros(100)
    non_zero_words = 0

    if type(text) == str:
        words = text.split()
        for word in words:
            try:
                vector += model.wv[word]
                non_zero_words += 1
            except:
                pass
    if non_zero_words != 0:
        return vector / non_zero_words
    else:
        return vector

if __name__ == '__main__':
    data = pd.read_csv('Electronics_reviews_1_star.csv', delimiter=';')
    for index, row in data.iterrows():
        #if row['rating'] == '1':
        print(sentence_preprocess(row['review']))

