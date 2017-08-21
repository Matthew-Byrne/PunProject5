import nltk
from nltk.corpus import wordnet as wn
from nltk.corpus import stopwords
from collections import Counter
from collections import defaultdict
import xml.etree.cElementTree as ET
import sys
import string
import re

#These methods are for computing relations between synsets and are used in my implemention of the Graph Connectivity algorithm

hypo = lambda s:s.hyponyms() #a lambda function for computing all the hyponyms of a synset
hyper = lambda s:s.hypernyms()#a lambda function for computing all the hypernyms of a synset


#this method requires a synset as an argument and returns a list of synsets which relate to unambiguous words contained within the example sentences provided by WordNet.
def example_unamb_synsets (synset):
        try:                
                unambiguous_synsets = []
                for example in synset.examples():
                        for word in example.split():
                                word = re.sub(r'[^\w\s]','',word)
                                if(word not in stopwords.words('english')):
                                        unambiguous_synsets.extend(wn.synsets(word))
                return unambiguous_synsets
        except (AttributeError, TypeError, KeyError) as e:
                print('You have entered an incorrect argument, please enter a synset')

#Requires a synset as an input and returns all of the synsets which are related via a nominilazation relation,
#that is, the lemmas within the synsets are derivational forms of the inputted synsets lemmas.
def dev_synsets(synset):
        try:
                dev_synsets = []
                for lemma in synset.lemmas():
                        for dev in lemma.derivationally_related_forms():
                                if dev.synset() not in dev_synsets:
                                        dev_synsets.append(dev.synset())
                return dev_synsets                      
        except (AttributeError, TypeError, KeyError) as e:
                print('You have entered an incorrect argument, please enter a synset')
                

noun_tree = ET.ElementTree(file = 'noun.xml') #parse in XML file using ElementTree containing disambiguated noun definitions
wordnet = noun_tree.getroot()  #set root for the tree
#this functions takes a noun synset as an input and returns a list of synsets which are the senses of the words used in the definition of the inputted synset
def defn_synsets_nouns(input_synset):
        try:  
              defn_synsets_nouns = []  
              offset1 = input_synset.offset() #offset number uniquely identifies each word in the XML file
              for synset_id in wordnet.findall('synset'):
                      offset2 = synset_id.get('ofs').lstrip("0") #strip away zeroes from offset number read from xml file
                      if offset2 != str(offset1): 
                              continue
                      else:
                              glosses = synset_id.findall('gloss') 
                              wsd = glosses[2] #gloss wsd
                              def_id = wsd.find('def')
                              for wf in def_id.findall('wf'):
                                      if wf.attrib['tag'] == 'man' or wf.attrib['tag'] == 'auto':
                                              sense_keys = []
                                              for id in wf.findall('id'):
                                                      sense_keys.append(id.attrib['sk'])
                                                      for sense_key in sense_keys:
                                                              if sense_key != 'purposefully_ignored%0:00:00::':
                                                                      synset2 = wn.lemma_from_key(sense_key).synset()
                                                                      if  synset2 != input_synset and synset2 not in defn_synsets_nouns :#compare with inputted synset to ensure no duplicates
                                                                              defn_synsets_nouns.append(synset2)
              return defn_synsets_nouns
        except (AttributeError, TypeError, KeyError) as e:
                print('You have entered an incorrect argument, please enter a noun synset')

 
verb_tree = ET.ElementTree(file = 'verb.xml') #parse in XML file using ElementTree containing disambiguated verb definitions
wordnet2 = verb_tree.getroot() #set root
#this functions takes a verb synset as an input and returns a list of synsets which are the senses of the words used in the definition of the inputted synset
def defn_synsets_verbs(input_synset):
        try:
              defn_synsets_verbs = []  
              offset1 = input_synset.offset()
              for synset_id in wordnet2.findall('synset'):
                      offset2 = synset_id.get('ofs').lstrip("0") #strip away zeroes from offset number read from xml file
                      if offset2 != str(offset1):
                              continue
                      else:
                              glosses = synset_id.findall('gloss')
                              wsd = glosses[2] #gloss wsd
                              def_id = wsd.find('def')
                              for wf in def_id.findall('wf'):
                                      if wf.attrib['tag'] == 'man' or wf.attrib['tag'] == 'auto':
                                              sense_keys = []
                                              for id in wf.findall('id'):
                                                      sense_keys.append(id.attrib['sk'])
                                                      for sense_key in sense_keys:
                                                              if sense_key != 'purposefully_ignored%0:00:00::':
                                                                      synset2 = wn.lemma_from_key(sense_key).synset()
                                                                      if  synset2 != input_synset and synset2 not in defn_synsets_verbs :#compare with inputted synset to ensure no duplicates
                                                                              defn_synsets_verbs.append(synset2)
              return defn_synsets_verbs
        except (AttributeError, TypeError, KeyError) as e:
                print('You have entered an incorrect argument, please enter a verb synset')
                                         
adjective_tree = ET.ElementTree(file = 'adj.xml') #parse in XML file using ElementTree containing disambiguated adjective definitions
wordnet3 = adjective_tree.getroot() #set root
#this functions takes an adjective synset as an input and returns a list of synsets which are the senses of the words used in the definition of the inputted synset
def defn_synsets_adjectives(input_synset):
        try:
                defn_synsets_adjectives = []
                offset1 = input_synset.offset()
                for synset_id in wordnet3.findall('synset'):
                        offset2 = synset_id.get('ofs').lstrip("0") #strip away zeroes from offset number read from xml file
                        if offset2 != str(offset1):
                                continue
                        else:
                              glosses = synset_id.findall('gloss')
                              wsd = glosses[2] #gloss wsd
                              def_id = wsd.find('def')
                              for wf in def_id.findall('wf'):
                                      if wf.attrib['tag'] == 'man' or wf.attrib['tag'] == 'auto':
                                              sense_keys = []
                                              for id in wf.findall('id'):
                                                      sense_keys.append(id.attrib['sk'])
                                                      for sense_key in sense_keys:
                                                              if sense_key != 'purposefully_ignored%0:00:00::':
                                                                      synset2 = wn.lemma_from_key(sense_key).synset()
                                                                      if  synset2 != input_synset and synset2 not in defn_synsets_adjectives :#compare with inputted synset to ensure no duplicates
                                                                              defn_synsets_adjectives.append(synset2)
                return defn_synsets_adjectives
        except (AttributeError, TypeError, KeyError) as e:
                print('You have entered an incorrect argument, please enter an adjective synset')
                                                                  
adverb_tree = ET.ElementTree(file = 'adv.xml') #parse in XML file using ElementTree containing disambiguated adverb definitions
wordnet4 = adverb_tree.getroot()
#this functions takes an adverb synset as an input and returns a list of synsets which are the senses of the words used in the definition of the inputted synset
def defn_synsets_adverbs(input_synset):
        try:
                defn_synsets_adverbs = []
                offset1 = input_synset.offset()
                for synset_id in wordnet4.findall('synset'):
                        offset2 = synset_id.get('ofs').lstrip("0") #strip away zeroes from offset number read from xml file
                        if offset2 != str(offset1):
                                continue
                        else:
                                glosses = synset_id.findall('gloss')
                                wsd = glosses[2] #gloss wsd
                                def_id = wsd.find('def')
                                for wf in def_id.findall('wf'):
                                        if wf.attrib['tag'] == 'man' or wf.attrib['tag'] == 'auto':
                                                sense_keys = []
                                                for id in wf.findall('id'):
                                                        sense_keys.append(id.attrib['sk'])
                                                        for sense_key in sense_keys:
                                                                if sense_key != 'purposefully_ignored%0:00:00::':
                                                                        synset2 = wn.lemma_from_key(sense_key).synset()
                                                                        if  synset2 != input_synset and synset2 not in defn_synsets_adverbs :#compare with inputted synset to ensure no duplicates
                                                                                defn_synsets_adverbs.append(synset2)
                return defn_synsets_adverbs
        except (AttributeError, TypeError, KeyError) as e:
                print('You have entered an incorrect argument, please enter an adjective synset')
                                  
                          
           
