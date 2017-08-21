import nltk
import operator
import string
from nltk.corpus import wordnet as wn
from nltk.corpus import stopwords
from collections import Counter
import xml.etree.cElementTree as ET

#First iteration of my system, this script contains methods which are used to classify a context as being either a pun or not a pun

try:
        tree = ET.ElementTree(file='subtask1-homographic-test.xml') #retrieve xml file as Tree
        corpus = tree.getroot() #find corpus (body of text containing contexts)
        global dict1
        dict1 = {} #create empty dictionary
        global dict2
        dict2 = {} #create second empty dictionary for storing words with 2 or more synsets as these are the only words that can be homographic punned words.
        for index in range(len(corpus)):
                dict1[index] = corpus.getchildren()[index].getchildren()
                dict2[index] = [word.text.lower() for word in dict1[index] if len(wn.synsets(word.text))>=2 and word.text.lower() not in stopwords.words('english')]
                for index2 in range(len(dict1[index])):
                        dict1[index][index2] = dict1[index][index2].text.lower()
        #create a two dimensional dictionary with a list of synsets for each word stored as values.
        synsets = {}
        for index in range(len(dict2)):
                synsets[index] = {}
                for index2 in range(len(dict2[index])):
                        synsets[index][index2] = [synset for synset in wn.synsets(dict2[index][index2])]
except FileNotFoundError as e:
        print('File not found, please enter correct filename')
        
#a function to take a word as an input and return all of the possible candidate senses for that word
def synsets_word(word):
        try:
                word_senses = [synset for synset in wn.synsets(word)]
                return word_senses
        except (AttributeError, TypeError, KeyError) as e:
                print('Incorrect input entered, please enter a word')
                

#a function to take a word as an input and returns a list of definitions for all the senses of that word
def defns_word(word):
        try:
                defns_word = [synset.definition() for synset in wn.synsets(word)]
                return defns_word
        except (AttributeError, TypeError, KeyError) as e:
                print('Incorrect input entered, please enter a word')

#a function that requires a sense definition and a context as input and returns the overlap between the given senses definition and the target context
def overlap(context, definition):
        try:
          results = Counter()
          results = [context.count(w) for w in set(definition)]
          return sum(results)
        except (AttributeError, TypeError, KeyError) as e:
                print('Incorrect argument/s used, please enter a context and a sense definition')
                

#requires a sense and returns its definition concatenated with definitions of the senses hypomyms and hypernyms
#Hyponyms are immediate subordinates to the sense and hypernyms are the superordinates in the WordNet inventory.
def defns_hh(synset):
        try:
                defns_hh = synset.definition()
                for hyponym in synset.hyponyms():
                        defns_hh = defns_hh + ', ' + hyponym.definition()
                for hypernym in synset.hypernyms():
                        defns_hh = defns_hh + ', ' + hypernym.definition()
                for example in synset.examples():
                        defns_hh = defns_hh + ', ' + example
                defns_hh = [word.strip(string.punctuation).lower() for word in defns_hh.split() if word.lower() not in stopwords.words('english')]
                lower_lemma_names = [word.lower() for word in synset.lemma_names()]
                return [word for word in defns_hh if word.lower() not in lower_lemma_names]
        except (AttributeError, TypeError, KeyError) as e:
                print('Incorrect argument/s used, please enter a synset')
                

#requires a context and a word and returns the senses of the word whose definitions have the three highest overlaps with the phrase definition.
# we find three senses as the top two senses for a pun should return a similar score whilst the third sense should be less.
def max_three_overlap(context, word):
        try:
                senses_to_overlap = {}
                senses = synsets_word(word)
                for sense in senses:
                 senses_to_overlap[sense] = int(overlap(context, defns_hh(sense)))
                d = Counter(senses_to_overlap)
                return dict(d.most_common(3))
        except (AttributeError, TypeError, KeyError) as e:
                print('Incorrect argument/s used, please enter a context and a word')
                

#requires the index of the context in the dictionary and returns a string indicating whether the context at that index is a pun or not.
def pun(index):
        try:
                context = dict1[index]
                shortened_context = dict2[index]
                for word in shortened_context:
                        dict4 = max_three_overlap(context, word)
                        values = [value for value in dict4.values()]
                        if (len(values)> 2 and values[2] < values[1] and values[0] > 0 and values[1] > 0 and values[0]== values[1]):
                                return 'A pun!'
                        if (len(values) == 2 and values[0] == values[1] and values[0] > 0 and values[1] > 0):
                                return 'A pun!'
                return 'Not a pun!'
        except (AttributeError, TypeError, KeyError) as e:
                print('Incorrect argument/s used, please enter an index')


                
                          
                
                         

    
                
