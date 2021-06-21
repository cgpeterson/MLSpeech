import nltk
from nltk.stem import PorterStemmer
stemmer = PorterStemmer()

import numpy
import tflearn
import tensorflow.compat.v1 as tf
tf.disable_v2_behavior()

import random
import json
import pickle
import os

class chatBot:
    
    def __init__(self):
        with open("intents.json") as file:
            data = json.load(file)
        
        # Attempt to load pre-existing model training
        try:
            with open("data.pickle", "rb") as f:
                words, labels, training, output = pickle.load(f)
        except:
            words = []
            labels = []
            docs_x = []
            docs_y = []
            
            # Break words down to just the word portions
            for intent in data["intents"]:
                for pattern in intent["patterns"]:
                    wrds = nltk.word_tokenize(pattern)
                    words.extend(wrds)
                    docs_x.append(wrds)
                    docs_y.append(intent["tag"])
                    
                if intent["tag"] not in labels:
                    labels.append(intent["tag"])
                
            words = [stemmer.stem(word) for word in words if word != "?"]
            words = sorted(list(set(words)))
            
            labels = sorted(labels)
            
            training = []
            output = []
            
            out_empty = [0 for _ in range(len(labels))]
            
            # Identify words for net to use
            for x, doc in enumerate(docs_x):
                bag = []
                
                wrds = [stemmer.stem(w) for w in doc]
                
                for w in words:
                    if w in wrds:
                        bag.append(1)
                    else:
                        bag.append(0)
                
                output_row = out_empty[:]
                output_row[labels.index(docs_y[x])] = 1
                
                training.append(bag)
                output.append(output_row)
                
            training = numpy.array(training)
            output = numpy.array(output)
            
            with open("data.pickle", "wb") as f:
                pickle.dump((words, labels, training, output), f)
        
        # Neural Net
        tf.reset_default_graph()
        
        with tf.Session() as sess:
            net = tflearn.input_data(shape=[None, len(training[0])])
            net = tflearn.fully_connected(net, 8)
            net = tflearn.fully_connected(net, 8)
            net = tflearn.fully_connected(net, len(output[0]), activation="softmax")
            net = tflearn.regression(net)
            
            model = tflearn.DNN(net)
            
            # Attempt to load previous model
            try:
                model.load("model.tflearn")
            except:
                model.fit(training, output, n_epoch=1000, batch_size=8, show_metric=True)
                model.save("model.tflearn")
    
    def bag_of_words(s, words):
        bag = [0 for _ in range(len(words))]
        
        s_words = nltk.word_tokenize(s)
        s_words = [stemmer.stem(word.lower()) for word in s_words]
        
        for se in s_words:
            for i, w in enumerate(words):
                if w == se:
                    bag[i] = 1
                    
        return numpy.array(bag)
        
    def chat(s):
        # Assign user input
        inp = s
        
        # Exit Program
        if inp.lower() == "quit":
            return "-1"
            
        # Identify user input
        results = model.predict([bag_of_words(inp, words)])
        results_index = numpy.argmax(results)
        tag = labels[results_index]
    
        # Choose response    
        for tg in data["intents"]:
            if tg["tag"] == tag:
                responses = tg["responses"]
                
        return random.choice(responses)
        
    def reset():
        # Remove .pickle file to allow reload of info from new data
        if os.path.exists("data.pickle"):
            os.remove("data.pickle")
        
        # remove .tflearn file to allow reload of new model
        if os.path.exists("model.tflearn"):
            os.remove("model.tflearn")
        
        return chatBot()