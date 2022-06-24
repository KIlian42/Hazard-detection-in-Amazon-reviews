import pandas as pd
# Load the regular expression library
import re

#data = pd.read_csv('Electronics_reviews_1_star.csv', delimiter=';')
#print(data.shape)
#data['review'] = data['review'].astype(str)

data = pd.read_csv('/Users/kiliankramer/PycharmProjects/MRP2/combined_Electronics.csv', delimiter=';')
data = data.loc[data['brand'] == 'Sony']
print(data['main_category'].value_counts(ascending=1))

data = data.loc[data['main_category'] == 'Home Audio & Theater']
print(data.shape)
data['review'] = data['review'].astype(str)

print(data.head())
# Remove punctuation
data['review'] = data['review'].map(lambda x: re.sub('[,\.!?]', '', x))
# Convert the titles to lowercase
data['review'] = data['review'].map(lambda x: x.lower())
# Print out the first rows of papers
print(data.head())

import gensim
from gensim.utils import simple_preprocess
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
stop_words = stopwords.words('english')
stop_words.extend(['from', 'subject', 're', 'edu', 'use'])

def sent_to_words(sentences):
    for sentence in sentences:
        # deacc=True removes punctuations
        yield(gensim.utils.simple_preprocess(str(sentence), deacc=True))

def remove_stopwords(texts):
    return [[word for word in simple_preprocess(str(doc))
             if word not in stop_words] for doc in texts]

data_prep = data.review.values.tolist()
data_words = list(sent_to_words(data_prep))
# remove stop words
data_words = remove_stopwords(data_words)
print(data_words[:1][0][:30])

# ======

import gensim.corpora as corpora
# Create Dictionary
id2word = corpora.Dictionary(data_words)
# Create Corpus
texts = data_words
# Term Document Frequency
corpus = [id2word.doc2bow(text) for text in texts]
# View
print(corpus[:1][0][:30])

# ======

from pprint import pprint
# number of topics
num_topics = 3
# Build LDA model
lda_model = gensim.models.LdaModel(corpus=corpus,id2word=id2word,num_topics=num_topics)
# Print the Keyword in the 10 topics
pprint(lda_model.print_topics())
doc_lda = lda_model[corpus]


