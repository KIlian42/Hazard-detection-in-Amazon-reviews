import pandas as pd
import numpy as np
import string
import re
from nltk.corpus import stopwords
import spacy
stop = set(stopwords.words("english"))
nlp = spacy.load('en_core_web_lg-3.0.0/en_core_web_lg/en_core_web_lg-3.0.0')
# from sklearn.model_selection import train_test_split
from collections import Counter
from tensorflow import keras
from keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from keras.models import Sequential
from keras.layers import Embedding, LSTM, Dense
from keras.optimizers import Adam
import random


def remove_URL(text):
    url = re.compile(r"https?://\S+|www\.\S+")
    return url.sub(r"", text)

def remove_html(text):
    html = re.compile(r"<.*?>")
    return html.sub(r"", text)

def remove_punct(text):
    table = str.maketrans("", "", string.punctuation)
    return text.translate(table)

def lemmatizer(text):
    doc = nlp(str(text))
    text = ' '.join([token.lemma_ if token.lemma_ != '-PRON-' else token.text for token in doc])
    return text

def remove_stopwords(text):
    text = [word.lower() for word in text.split() if word.lower() not in stop]
    return " ".join(text)

def transform_labels(text):
    if (text == 'positive'):
        return 1
    else:
        return 0

def counter_word(text):
    count = Counter()
    for i in text.values:
        for word in i.split():
            count[word] += 1
    return count

def decode(text):
    return " ".join([reverse_word_index.get(i, "?") for i in text])

if __name__ == '__main__':
    kernel_size = 5
    Preprocessed_Filtered_Reviews = 'Preprocessed_Filtered_Reviews'+str(kernel_size)+'.csv'
    df = pd.read_csv(Preprocessed_Filtered_Reviews, delimiter=';')

    # === Get average review length for padding size:
    lengths = []
    lengths2 = []
    df['review'] = df['review'].astype(str)
    # print(df['review'].apply(len).mean())
    for index, row in df.iterrows():
        if row['label'] == 'positive':
            lengths.append(len(row['review'].split(' ')))
        if row['label'] == 'negative':
            lengths2.append(len(row['review'].split(' ')))
    # Answer: 1
    print('positive:', len(lengths))
    average = np.mean(np.array(lengths), axis=0)
    print('Average positive:', average)
    sd = np.std(np.array(lengths), axis=0)
    print('Standard deviation positive:', sd)
    print('Min positive:', min(lengths))
    print('Max positive:', max(lengths))
    # Answer: 2
    print('negative:', len(lengths2))
    average = np.mean(np.array(lengths2), axis=0)
    print('Average negative:', average)
    sd = np.std(np.array(lengths2), axis=0)
    print('Standard deviation negative:', sd)
    print('Min negative:', min(lengths2))
    print('Max negative:', max(lengths2))

    positive = df.loc[df['label'] == 'positive'].head(3347)
    negative = df.loc[df['label'] == 'negative']

    frames = [positive, negative]
    df = pd.concat(frames)
    df = df.sample(frac=1)

    # Some preprocessing
    df["label"] = df.label.map(lambda x: transform_labels(x))

    # Split train/test dataset
    #X = df['review'].values
    #y = df['label'].values
    #X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Split train/test dataset using Pandas
    train_size = int(df.shape[0] * 0.8)
    train_sentences = df.review[:train_size]
    train_labels = df.label[:train_size]
    test_sentences = df.review[train_size:]
    test_labels = df.label[train_size:]

    # ======

    text = df.review
    counter = counter_word(text)
    num_words = len(counter)
    max_length = 12

    tokenizer = Tokenizer(num_words=num_words)
    tokenizer.fit_on_texts(train_sentences)

    word_index = tokenizer.word_index

    train_sequences = tokenizer.texts_to_sequences(train_sentences)

    train_padded = pad_sequences(train_sequences, maxlen=max_length, padding="post", truncating="post")
    test_sequences = tokenizer.texts_to_sequences(test_sentences)
    test_padded = pad_sequences(test_sequences, maxlen=max_length, padding="post", truncating="post")

    reverse_word_index = dict([(value, key) for (key, value) in word_index.items()])

    decode(train_sequences[0])

    model = Sequential()
    model.add(Embedding(num_words, 32, input_length=max_length))
    model.add(LSTM(64, dropout=0.1))
    model.add(Dense(1, activation="sigmoid"))
    optimizer = Adam(learning_rate=3e-4)
    model.compile(loss="binary_crossentropy", optimizer=optimizer, metrics=["accuracy"])
    # model.summary()

    #history = model.fit(train_padded, train_labels, epochs=20, validation_data=(test_padded, test_labels))
    #model.save('trained_bilstm_5')
    model = keras.models.load_model('trained_bilstm_5')


    df = pd.read_csv('test.csv', delimiter=';')
    # Some preprocessing
    df["review"] = df.review.map(lambda x: remove_URL(x))
    df["review"] = df.review.map(lambda x: remove_html(x))
    df["review"] = df.review.map(lambda x: remove_punct(x))
    df["review"] = df["review"].map(lemmatizer)
    df["review"] = df["review"].map(remove_stopwords)

    pred = []
    for index, row in df.iterrows():
        splitted = len(row['review'].split(' '))
        print(splitted, row["review"])
        seq = tokenizer.texts_to_sequences([row["review"]])
        padded = pad_sequences(seq, maxlen=max_length)
        print(padded)
        pred.append(model.predict(padded))

    # Print predictions
    for p in pred:
        print(p)
    '''
    for i, prediction in enumerate(pred):
        if prediction[0] >= 0.5:
            print("Positive:", txt[i])
        else:
            print("Negative:", txt[i])
    '''

