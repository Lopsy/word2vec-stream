import struct


# REPLACE THIS WITH THE FILEPATH FOR YOUR 3.5 GB WORD2VEC FILE
gfile = "C:/Python27/random_files/google_word2vec.bin"


def gstream(n=None):
    """ Yields pairs (word, vec) from the 300-dimensional Google .gz file.
    If n is given, stops after n pairs. """
    #with gzip.GzipFile(gfile) as f:
    with open("random_files/google_word2vec.bin", "rb") as f:
        f.read(1217) # up to right before first "in"
        i = 0 # words processed so far
        while n==None or i < n:
            i += 1
            word = ""
            while True:
                c = f.read(1)
                assert c # An assertion error here means we finished the file
                if c == " ":
                    break
                elif c: # as long as c isn't empty
                    word += c
                else: # done with file!
                    raise StopIteration
            nums = f.read(1200)
            # The next line interprets every 4-byte chunk as a floating point.
            # See the "value = sign * exp * pre" answer here:
            # https://stackoverflow.com/questions/27324292
            """vec = [struct.unpack('>f',
                    nums[4*i+3:4*i-1:-1] if i>0 else nums[3::-1])[0] \
                   for i in xrange(300)]"""
            vec = struct.unpack('<'+'f'*300, nums)
            yield (word, vec)

def add(*vecs):
    return [sum(xs) for xs in zip(*vecs)]
def neg(vec):
    return [-x for x in vec]

def unit(vec):
    vecnorm = norm(vec)
    return [x/vecnorm for x in vec]
def norm(vec):
    return dot(vec,vec)**0.5
def dot(v,w): return sum(x*y for x,y in zip(v,w))
def normalizedDot(v, w):
    """ cosine of the angle between v and w. """
    return dot(v,w)/(norm(v)*norm(w))
    
