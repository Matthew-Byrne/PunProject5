import xml.etree.cElementTree as ET
from nltk.corpus import wordnet as wn
from collections import defaultdict
noun_tree = ET.ElementTree(file = 'adv.xml')
wordnet = noun_tree.getroot()
tagged_glosses = defaultdict(list)
for index in range(3621):   
    synsetkey = wordnet.getchildren()[index].getchildren()[1].getchildren()[0].text
    synset = wn.lemma_from_key(synsetkey).synset()
    if synset not in tagged_glosses:
        definition = wordnet.getchildren()[index].getchildren()[4].getchildren()[0].getchildren()
        def_synsets = []
        for index in range(len(definition)):
            attributes = definition[index].attrib
            if 'tag' in attributes: 
                if (attributes['tag'] == 'man' or attributes['tag'] == 'auto'):
                    def_synset_key = definition[index].getchildren()[0].attrib['sk']
                    if(def_synset_key != 'purposefully_ignored%0:00:00::'):
                        print(def_synset_key)
                        def_synsets.append(wn.lemma_from_key(def_synset_key).synset())
    tagged_glosses[synset] = def_synsets
    
