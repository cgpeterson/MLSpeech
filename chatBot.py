import nltk
from nltk.stem import PorterStemmer
stemmer = PorterStemmer()

import numpy
import tensorflow
import tflearn

import random
import json
import pickle
import os

class chatBot:
    
    def __init__(self):
        with open("intents.json") as file:
            self.data = json.load(file)
        
        # Attempt to load pre-existing model training
        try:
            with open("data.pickle", "rb") as f:
                self.words, self.labels, self.training, self.output = pickle.load(f)
        except:
            self.words = []
            self.labels = []
            self.docs_x = []
            self.docs_y = []
            
            # Break words down to just the word portions
            for intent in self.data["intents"]:
                for pattern in intent["patterns"]:
                    wrds = nltk.word_tokenize(pattern)
                    self.words.extend(wrds)
                    self.docs_x.append(wrds)
                    self.docs_y.append(intent["tag"])
                    
                if intent["tag"] not in self.labels:
                    self.labels.append(intent["tag"])
                
            self.words = [stemmer.stem(word) for word in self.words if word != "?"]
            self.words = sorted(list(set(self.words)))
            
            self.labels = sorted(self.labels)
            
            self.training = []
            self.output = []
            
            out_empty = [0 for _ in range(len(self.labels))]
            
            # Identify words for net to use
            for x, doc in enumerate(self.docs_x):
                bag = []
                
                wrds = [stemmer.stem(w) for w in doc]
                
                for w in self.words:
                    if w in wrds:
                        bag.append(1)
                    else:
                        bag.append(0)
                
                output_row = out_empty[:]
                output_row[self.labels.index(self.docs_y[x])] = 1
                
                self.training.append(bag)
                self.output.append(output_row)
                
            self.training = numpy.array(self.training)
            self.output = numpy.array(self.output)
            
            with open("data.pickle", "wb") as f:
                pickle.dump((self.words, self.labels, self.training, self.output), f)
        
        # Neural Net
        
        
        net = tflearn.input_data(shape=[None, len(self.training[0])])
        net = tflearn.fully_connected(net, 8)
        net = tflearn.fully_connected(net, 8)
        net = tflearn.fully_connected(net, len(self.output[0]), activation="softmax")
        net = tflearn.regression(net)
        
        self.model = tflearn.DNN(net)
        
        # Attempt to load previous model
        try:
            self.model.load("model.tflearn")
        except:
            self.model = tflearn.DNN(net)
            self.model.fit(self.training, self.output, n_epoch=1000, batch_size=8, show_metric=False)
            self.model.save("model.tflearn")
    
    def bag_of_words(self, s, words):
        bag = [0 for _ in range(len(self.words))]
        
        s_words = nltk.word_tokenize(s)
        s_words = [stemmer.stem(word.lower()) for word in s_words]
        
        for se in s_words:
            for i, w in enumerate(words):
                if w == se:
                    bag[i] = 1
                    
        return numpy.array(bag)
        
    def chat(self, s):
        # Assign user input
        inp = s
        
        # Identify user input
        results = self.model.predict([self.bag_of_words(inp, self.words)])[0]
        results_index = numpy.argmax(results)
        tag = self.labels[results_index]
    
        # Choose response 
        rvalue = ""
        if results[results_index] > 0.8:
            for tg in self.data["intents"]:
                if tg["tag"] == tag:
                    responses = tg["responses"]
            rvalue = random.choice(responses)
        else:
            rvalue = "I don't understand. Try again"
                    
        return rvalue
        
    def reset(self):
        # Remove .pickle file to allow reload of info from new self.data
        if os.path.exists("data.pickle"):
            os.remove("data.pickle")
        
        # remove .tflearn file to allow reload of new model
        if os.path.exists("model.tflearn.meta"):
            os.remove("model.tflearn.meta")
            os.remove("model.tflearn.index")
            os.remove("model.tflearn.data-00000-of-00001")
        
        #remove recordings
        if os.path.exists("recorded.wav"):
            os.remove("recorded.wav")