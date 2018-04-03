"""

V is an object behaving like a function.
V("rabbit") is the 300-element vector for rabbit.

You can also query whether strings are in the word2vec database:
> "rabbit" in V

    (V also kind of behaves like a dict -- V[word] returns the word's location
    in the big file -- but ignore that.)

nd is the normalized dot product:
> nd(V("rabbit"), V("carrot")) # 0.3630643116925243
> nd("rabbit", "carrot") # 0.3630643116925243

"""

# Replace this with the filepath to your gwords.txt file

WORD_FILEPATH = "random_files/gwords.txt"

import struct
from word2vec import add, neg, gstream, normalizedDot, unit
from heapq import nlargest # nlargest(3, L, key=None) -> largest 3 from L


class VecDatabase(dict):
    def __init__(self, *args):
        dict.__init__(self, *args)
        self.loaded = False
        self.wordlist = None

    def __iter__(self):
        if not self.wordlist: self.loadWordlist()
        for word in self.wordlist: yield word

    def loadWordlist(self):
        self.wordlist = S()

    def __len__(self):
        if not self.loaded: self.loadWordLocations()
        return dict.__len__(self)
        
    def __call__(self, word):
        if not self.loaded: self.loadWordLocations()
        if word not in self: raise KeyError(word) # not in dictionary
        with open("random_files/google_word2vec.bin", "rb") as f:
            f.seek(self[word])
            return struct.unpack("<"+"f"*300, f.read(1200))

    def loadWordLocations(self):
        with open(WORD_FILEPATH,"r") as f:
            fileloc = 1217
            for line in f.readlines():
                word = line[:-1]
                fileloc += len(word)+1
                self[word] = fileloc
                fileloc += 1200
        self.loaded = True

    def __getitem__(self, key):
        # Thanks stackoverflow.
        if isinstance(key, str):
            return dict.__getitem__(self, key)
        if not self.wordlist: self.loadWordlist()
        if isinstance(key, slice):
            return [self.wordlist[ii] for ii in xrange(*key.indices(len(self)))]
        elif isinstance(key, int):
            if key < 0:
                key += len(self)
            if key < 0 or key >= len(self):
                raise IndexError, "The index (%d) is out of range."%key
            return self.wordlist[key]
        else:
            raise TypeError, "Invalid argument type."

def V():
    """returns a function identical to word2vec... which is also a dictionary"""
    w2v = VecDatabase()
    w2v.loadWordLocations()
    return w2v
V = V()

def S():
    """ Returns the list of words in the word2vec database """
    with open(WORD_FILEPATH,"r") as f:
        return [word[:-1] for word in f.readlines()]

def nd(v,w):
    """ Normalized dot product. """
    if type(v) == str: v = V(v)
    if type(w) == str: w = V(w)
    return normalizedDot(v, w)

def together(word):
    """ For example, together("canoe") is a list that includes "rental" and
    "usa" (among other strings) because "Canoe_Rental" and "USA_Canoe_Kayak"
    are both in the word2vec database. """
    phrases = [thing for thing in V if word in thing.lower().split("_")]
    return {word for phrase in phrases for word in phrase.lower().split("_")}

def parse(equation, unitVectors=True):
    """ equation is like 'water - boat + car'. Returns a vector.
    Assumes +, -, and # never appears in the words. """
    equation = equation.replace(" ","")
    if equation[0] != "-": equation = "+" + equation
    equation = equation+"#"
    total = [0 for i in xrange(300)]
    index = 0
    while True:
        sign = equation[index]
        index += 1
        assert sign in "+-#"
        if sign == "#": return total
        word = ""
        while equation[index] not in "+-#":
            word += equation[index]
            index += 1
        wordVector = V(word)
        if unitVectors: wordVector = unit(wordVector)
        total=add(total,wordVector) if sign=="+" else add(total,neg(wordVector))
        
    
    


