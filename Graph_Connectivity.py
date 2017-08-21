from GC_methods import *
import pydot
from anytree import Node, RenderTree
import PIL
from PIL import Image
import time

#This script shows my implementation of the Graph Connectivity algorithm using methods from the GC methods script. 
try:
        tree = ET.ElementTree(file='subtask1-homographic-test.xml') #retrieve xml file of homographic puns as Tree
        corpus = tree.getroot() #find corpus
        global dict1
        global dict2
        dict1 = defaultdict(list) #create empty dictionary for storing all words in every context from the xml file.
        dict2 = defaultdict(list) #create second empty dictionary for storing verbs, adverbs, nouns and adjectives
        for index in range(len(corpus)):
                dict1[index] = corpus.getchildren()[index].getchildren()
                for index2 in range(len(dict1[index])):
                       dict1[index][index2] = dict1[index][index2].text.lower()
        for index in range(len(corpus)):
                tags = nltk.pos_tag(dict1[index]) #pos tags for word in context
                dict2[index] = []
                for index2 in range(len(tags)):
                        tag = tags[index2][1]
                        word = tags[index2][0]
                        if word not in stopwords.words('english'):
                                if tag.startswith('J'):
                                        dict2[index].append(word)
                                if tag.startswith('V'):
                                        dict2[index].append(word)
                                if tag.startswith('N'):
                                        dict2[index].append(word)
                                if tag.startswith('R'):
                                        dict2[index].append(word)
except FileNotFoundError as e:
        print('File not Found, please enter a correct filename')
        
#For each context I need to store a list of possible synsets as these will make up the vertices for each indiviual graph.
global vertices_dict
vertices_dict = defaultdict(list)
#After each iteration of the outer loop the synsets for every word of a context have been added to the dictionary
for index in range(len(corpus)):
        vertices_dict[index] = []
        #after each iteration of the inner loop the synsets for a word have been added to the list stored at an index in the dictionary
        for index2 in range(len(dict2[index])):
                synsets2 = wn.synsets(dict2[index][index2])                
                for synset in synsets2:                       
                        if synset not in vertices_dict[index]:
                                vertices_dict[index].append(synset)
                                
#This method requires an index of where the context is stored in the dictionary and through using Depth First Search to expand WordNet to a maximum height
# of 3 it builds a tree for each vertex within the context. When it finds a relation between two vertices the intermediate nodes along the path are added
# to the set of vertices stored for the context and the connections between them are added to the edges. The method returns a tuple containing the vertices,
# edges and the context index.
def tree(index):
        try:
                start = time.time()
                edges = []
                global vertices_dict
                vertices = vertices_dict[index]
                size = len(vertices)
                for vertex in vertices[:size]:
                        tree = Node(vertex)
                        hypers = vertex.hypernyms()#hypernyms of vertex
                        hypos = vertex.hyponyms() #hyponyms of vertex
                        dvss = dev_synsets(vertex)#derivationally related forms of a vertex

                        if vertex.pos() == 'n':
                                ds = defn_synsets_nouns(vertex) #definition relationship between noun vertex and other synsets
                        if vertex.pos() == 'v':
                                ds = defn_synsets_verbs(vertex) #definition relationship between verb vertex and other synsets
                        if vertex.pos() == 'a' or vertex.pos() == 's':
                                ds = defn_synsets_adjectives(vertex)#definition relationship between adjective vertex and other synsets
                        if vertex.pos() == 'r':
                                ds = defn_synsets_adverbs(vertex) #definition relationship between adverb vertex and other synsets

                        #derivationally related forms (nominalization relation)
                        for dvs in dvss:
                                dvschild = Node(dvs, parent=tree)
                                if dvs in vertices and (vertex, dvs) not in edges and (dvs, vertex) not in edges:
                                        edges.append((vertex, dvs))
                                if dvs.pos() == 'n':
                                        def_dvss = defn_synsets_nouns(dvs) 
                                if dvs.pos() == 'v':
                                        def_dvss = defn_synsets_verbs(dvs) 
                                if dvs.pos() == 'a' or dvs.pos() == 's':
                                        def_dvss = defn_synsets_adjectives(dvs)
                                if dvs.pos() == 'r':
                                        def_dvss = defn_synsets_adverbs(dvs)

                                for def_dvs in def_dvss:
                                        defdvschild = Node(def_dvs, parent=dvschild)
                                        if def_dvs in vertices and def_dvs != vertex:
                                                if(vertex, dvs) not in edges and (dvs, vertex) not in edges:
                                                                edges.append((vertex,dvs))
                                                if(dvs, def_dvs) not in edges and (def_dvs, dvs) not in edges:
                                                                edges.append((dvs, def_dvs))
                                                if dvs not in vertices:
                                                        vertices.append(dvs)
                        
                        #hypernyms                                              
                        for hyper in hypers:
                                hyperchild = Node(hyper, parent=tree)
                                if hyper in vertices and (vertex, hyper) not in edges and (hyper, vertex) not in edges:
                                        edges.append((vertex,hyper))
                                if hyper.pos() == 'n':
                                        defhypers = defn_synsets_nouns(hyper)
                                if hyper.pos() == 'v':
                                        defhypers = defn_synsets_verbs(hyper)
                                if hyper.pos() == 'a' or hyper.pos()== 's':
                                        defhypers = defn_synsets_adjectives(hyper)
                                if hyper.pos() =='r':
                                        defhypers = defn_synsets_adverbs(hyper)
                                #defintionHypernyms
                                for defhyper in defhypers:
                                        defhyperchild = Node(defhyper, parent=hyperchild)
                                        if defhyper in vertices and defhyper != vertex:
                                                if(vertex, hyper) not in edges and (hyper, vertex) not in edges:
                                                        edges.append((vertex,hyper))
                                                if(hyper, defhyper) not in edges and (defhyper, hyper) not in edges:
                                                        edges.append((hyper, defhyper))
                                                if hyper not in vertices:
                                                        vertices.append(hyper)
                                hypers2 = hyper.hypernyms()
                                for hyper2 in hypers2:
                                        hyper2child = Node(hyper2, parent = hyperchild)
                                        if hyper2 in vertices and hyper2 != vertex:
                                                if (vertex, hyper) not in edges and (hyper, vertex) not in edges:
                                                        edges.append((vertex, hyper))
                                                if (hyper, hyper2) not in edges and (hyper2, hyper) not in edges:
                                                        edges.append((hyper, hyper2))
                                                if hyper not in vertices :
                                                        vertices.append(hyper)
                        #hyponyms                                                                                              
                        for hypo in hypos:
                                hypochild = Node(hypo, parent=tree)
                                if hypo in vertices and (vertex, hypo) not in edges and (hypo, vertex) not in edges:
                                        edges.append((vertex, hypo))
                                if hypo.pos() == 'n':
                                        defhypos = defn_synsets_nouns(hypo)
                                if hypo.pos() == 'v':
                                        defhypos = defn_synsets_verbs(hypo)
                                if hypo.pos() == 'a' or hypo.pos()== 's':
                                        defhypos = defn_synsets_adjectives(hypo)
                                if hypo.pos() == 'r':
                                        defhypos = defn_synsets_adverbs(hypo)
                                #definitionHyoponyms
                                for defhypo in defhypos:
                                        defhypochild = Node(defhypo, parent=hypochild)
                                        if defhypo in vertices and defhypo != vertex:
                                                if(vertex, hypo) not in edges and (hypo, vertex) not in edges:
                                                                edges.append((vertex,hypo))
                                                if(hypo, defhypo) not in edges and (defhypo, hypo) not in edges:
                                                                edges.append((hypo, defhypo))
                                                if hypo not in vertices:
                                                        vertices.append(hypo)                                                       
                                hypos2 = hypo.hyponyms()
                                for hypo2 in hypos2:
                                        hypo2child = Node(hypo2, parent = hypochild)
                                        if hypo2 in vertices and hypo2 != vertex:
                                                if(vertex, hypo) not in edges and (hypo, vertex) not in edges:
                                                        edges.append((vertex, hypo))
                                                if(hypo, hypo2) not in edges and (hypo2, hypo) not in edges:
                                                        edges.append((hypo, hypo2))
                                                if hypo not in vertices:
                                                        vertices.append(hypo)

                         #gloss relations                       
                        for synset in ds:
                                child2 = Node(synset, parent=tree)
                                if synset in vertices and (vertex, synset) not in edges and (synset, vertex) not in edges:
                                        edges.append((vertex, synset))
                                dshyponyms = synset.hyponyms()
                                for dshyponym in dshyponyms:
                                        dshchild = Node(dshyponym, parent=child2)
                                        if dshyponym in vertices and dshyponym != vertex:
                                                if (vertex, synset) not in edges and (synset, vertex) not in edges:
                                                        edges.append((vertex,synset))
                                                if (synset, dshyponym) not in edges and (dshyponym, synset) not in edges:
                                                        edges.append((synset, dshyponym))
                                                if synset not in vertices:
                                                       vertices.append(synset)

                        #method to draw tree using anytree
                        for pre, fill, node in RenderTree(tree):
                                print("%s%s" % (pre, node.name))
                end = time.time()
                print(end - start)
                return (vertices, edges, index)
        except (AttributeError, TypeError, KeyError) as e:
                print('Incorrect input entered, please enter an index')
                
#A method that takes a tuple as an input which is made up of the vertices, edges of a graph along with the index of the context for which the subgraph is being created.
#It prints out a subgraph using Python Imaging Library and pydot displaying the relations between contexts.
#A node is added displaying the classification the system has applied to the context, either a pun or not a pun.
def graph (tuple):
        try:
                vertices = tuple[0]
                edges = tuple[1]
                index = tuple[2]
                global dict2
                centrality2 = centrality(vertices, edges)
                graph = pydot.Dot(graph_type='graph')
                for vertex in vertices:
                        graph.add_node(pydot.Node(str(vertex)))
                for edge in edges:
                        node1 = str(edge[0])
                        node2 = str(edge[1])
                        graph.add_edge(pydot.Edge(node1, node2))
                pun = [] 
                for word in dict2[index]:
                        print(top_three_centrality(centrality2, word))
                        t3c = top_three_centrality(centrality2, word)
                        if (len(t3c) > 2 and t3c[0][1] < t3c[1][1] and t3c[1][1]==t3c[2][1] and t3c[1][1] > 0 and t3c[2][1]>0):
                                        graph.add_node(pydot.Node("A pun!", style="filled", fillcolor="yellow"))
                                        pun.append(1)
                        if (len(t3c) == 2 and t3c[0][1] == t3c[1][1] and t3c[0][1] > 0 and t3c[1][1]>0):
                                        graph.add_node(pydot.Node("A pun!", style="filled", fillcolor="yellow"))
                                        pun.append(1)  
                if 1 not in pun:
                        graph.add_node(pydot.Node("Not a pun!", style="filled", fillcolor="red"))
                                                 
                graph.write_png('example_graph.png')
                im = Image.open("example_graph.png")
                im.show()
        except (AttributeError, TypeError, KeyError) as e:
                print('Incorrect input entered, please enter a tuple, consisting of the vertices, edges and index of graph')
        
#A method that takes a list of synsets (vertices) and a list of tuples (edges) as input and returns a dictionary.
# this dictionary contains the vertices as keys and their centrality scores as values.
# centrality being the degree of each vertex i.e the number of edges terminating at the vertex.
def centrality (vertices, edges):
        try:
                centrality = {}
                for vertex in vertices:
                        count = 0
                        for edge in edges:
                                if vertex == edge[0] or vertex==edge[1]:
                                        count = count + 1
                        centrality[vertex] = count/(len(vertices)-1)
                return  centrality
        except (AttributeError, TypeError, KeyError) as e:
                print('Incorrect input entered, please enter a list of vertices anda list of edges which make up the subgraph')
        
#A method that returns the top three centrality scores for senses of a word, given a word and a dictionary containing all of the centrality scores for a word.       
def top_three_centrality (centrality, word):
        try:
                synset_centrality = []
                for key,value in centrality.items():
                      if key in wn.synsets(word):
                              synset_centrality.append((key, value))
                sorted_list = sorted(synset_centrality, key=lambda x:x[1])
                return sorted_list[-3:]
        except (AttributeError, TypeError, KeyError) as e:
                print('Incorrect input entered, please enter a centrality dictionary and a word as input')
        
                      
list_index = []
for index in range(len(vertices_dict)):
	if len(vertices_dict[index]) <30:
		list_index.append(index)                     
                
       
                                
                                
                        
                                
        
                
                
        
