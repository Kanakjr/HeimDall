##########################
#  Code Author: 1359531  #
##########################

# uncomment for the first time
# import nltk
# nltk.download('punkt')

from core.nlpfunctions import bow
from core.nlpfunctions import clean_up_sentence
import nltk
from nltk.stem.lancaster import LancasterStemmer
stemmer = LancasterStemmer()

import json
import random
import pickle
import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Dropout

# import our heimdall intents file
with open('files/intents.json') as json_data:
    intents = json.load(json_data)

words = []
classes = []
documents = []
ignore_words = ['?']
for intent in intents['intents']:
    for pattern in intent['patterns']:
        w = nltk.word_tokenize(pattern)
        words.extend(w)
        documents.append((w, intent['tag']))
        if intent['tag'] not in classes:
            classes.append(intent['tag'])

words = [stemmer.stem(w.lower()) for w in words if w not in ignore_words]
words = sorted(list(set(words)))
classes = sorted(list(set(classes)))

print (len(documents), "documents")
print (len(classes), "classes", classes)
print (len(words), "unique stemmed words", words)

training = []
output = []
output_empty = [0] * len(classes)

for doc in documents:
    bag = []
    pattern_words = doc[0]
    pattern_words = [stemmer.stem(word.lower()) for word in pattern_words]
    for w in words:
        bag.append(1) if w in pattern_words else bag.append(0)

    output_row = list(output_empty)
    output_row[classes.index(doc[1])] = 1
    training.append([bag, output_row])

random.shuffle(training)
training = np.array(training)

train_x = list(training[:,0])
train_y = list(training[:,1])
train_x = np.asarray(train_x, dtype=np.float32)
train_y = np.asarray(train_y, dtype=np.float32)

##################### Model ################################

model = Sequential()
model.add(Dense(48, input_dim=train_x.shape[1], activation='relu'))
# model.add(Dropout(0.1))
model.add(Dense(32, activation='relu'))
# model.add(Dropout(0.5))
model.add(Dense(16, activation='relu'))
# model.add(Dropout(0.5))
model.add(Dense(train_y.shape[1], activation='softmax'))
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

#############################################################

model.fit(train_x, train_y, epochs=200)

# evaluate the keras model
_, accuracy = model.evaluate(train_x, train_y)
print('Accuracy: %.2f' % (accuracy*100))

model.summary()

# save all of our data structures
pickle.dump( {'words':words, 'classes':classes}, open( "files/meta.pkl", "wb" ) )
model.save("files/model.h5")

