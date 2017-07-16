import gzip
import struct


# REPLACE THIS WITH THE FILEPATH FOR YOUR 1.5GB WORD2VEC FILE
gfile = "C:/Python27/random_files/google_word2vec.gz"



def word2vec(word, matchCase=True):
    """ Returns the 300-element vector corresponding to `word`.
    If you want to vectorize more than one word at once, gvecs is faster.
    matchCase: if True, then angel is different from Angel """
    return gvecs([word], matchCase=matchCase, verbose=0)[0]


def gvecs(targetWords, matchCase=True, asDict=False, verbose=True):
    """ Finds the vector for each word in targetWords.
        If asDict==True, then returns a dict {word: vec}.
        Else, returns a list of vectors, one for each word in targetWords.
        matchCase: if True, then angel is different from Angel
        verbose: print words as you find them """
    if not asDict: assert type(targetWords) in (list, tuple)
    targetWords = list(targetWords)
    wordsToFind = len(targetWords)
    # get locations of unfound words:
    unfound = {word.replace("_"," "):i for i,word in enumerate(targetWords)}
    if not matchCase: unfound = {w.lower():i for (w,i) in unfound.items()}
    D = {} if asDict else [None for word in targetWords] # return objects
    #i=0
    with gzip.GzipFile(gfile) as f:
        f.read(1217) # up to right before first "in"
        while len(unfound) > 0:
            word = ""
            while True:
                c = f.read(1)
                if c == " ":
                    break
                else:
                    word += c
            #i += 1
            #if i%1000==1: print i, word
            nums = f.read(1200)
            normalizedWord = word.replace("_"," ")
            if not matchCase: normalizedWord = normalizedWord.lower()
            if normalizedWord in unfound:
                vec = struct.unpack('<'+'f'*300, nums)
                if asDict:
                    D[targetWords[unfound[word]]] = vec
                else:
                    D[unfound[word]] = vec
                del unfound[normalizedWord]
                if verbose and len(targetWords)>1: print word,
    return D
                


def gstream():
    """ Yields pairs (word, vec) from the 300-dimensional Google .gz file,
    from most common to least common word.
    Example use:
    for (word, vec) in gstream(): [do something]"""
    with gzip.GzipFile(gfile) as f:
        f.read(1217) # up to right before first "in"
        while True:
            word = ""
            while True:
                c = f.read(1)
                if c == " ":
                    break
                else:
                    word += c
            nums = f.read(1200)
            # The next line interprets every 4-byte chunk as a floating point.
            # See the "value = sign * exp * pre" answer here:
            # https://stackoverflow.com/questions/27324292
            vec = struct.unpack('<'+'f'*300, nums)
            yield (word, vec)
    
def unit(vec):
    vecnorm = norm(vec)
    return [x/vecnorm for x in vec]
def norm(vec):
    return dot(vec,vec)**0.5
def dot(v,w): return sum(x*y for x,y in zip(v,w))
def normalizedDot(v, w):
    """ cosine of the angle between v and w. """
    return dot(v,w)/(norm(v)*norm(w))
    
