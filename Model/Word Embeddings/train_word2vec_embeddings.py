import spacy
import re
from gensim.models import Word2Vec
import pandas as pd
nlp = spacy.load('en_core_web_lg-3.0.0/en_core_web_lg/en_core_web_lg-3.0.0')
import tqdm

path = '/Users/kiliankramer/Desktop/MRP2 Scraping/'

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

if __name__ == '__main__':
    '''
    data = pd.read_csv('Electronics_reviews_1_star.csv', delimiter=';')
    data = data[:10000]
    sentences = []
    print(data.shape)
    for index, row in data.iterrows():
        print(index)
        sentence = sentence_preprocess(row['review'])
        print(sentence)
        sentences.append(sentence)
    # train model
    model = Word2Vec(sentences, min_count=1, vector_size=300)
    model.save('model.bin')
    '''

    new_model = Word2Vec.load('model.bin')
    print(new_model.wv.most_similar('explode', topn=100))
    # print(new_model.wv['I'])