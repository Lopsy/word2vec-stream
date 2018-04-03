# py-word2vec
This is a Python 2 tool for parsing Google's pretrained word2vec vector file (which you can find at https://drive.google.com/file/d/0B7XkCwpI5KDYNlNUTTlSS21pQmM/edit) without having to load it all into RAM.

# Getting Started
First, unzip the big vector file in the above link. Edit the filepath variable in word2vec.py appropriately.
Then, edit the WORD_FILEPATH variable in words2vec.py to whatever you want, and run the CREATE_WORD_FILE() function in words2vec.py. (This will create a file containing the list of words in the vector database.)
Now you're good to go.

# Useful functions

from word2vec import gstream

gstream(n=None) --> yields the first n (word, vec) pairs from the database. If n is None, instead yields all pairs.

from words2vec import V, nd

V("rabbit") --> Returns the 300-element vector for "rabbit"

"rabbit" in V --> True

nd(V("rabbit"), V("carrot")) --> normalized dot product

nd("rabbit", "carrot") --> automatically applies V to the inputs

Please credit Linus Hamilton if you use this program to make something cool.
