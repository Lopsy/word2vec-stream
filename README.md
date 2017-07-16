# py-word2vec
This is a Python 2 tool for parsing Google's pretrained word2vec vector file (which you can find at https://drive.google.com/file/d/0B7XkCwpI5KDYNlNUTTlSS21pQmM/edit) without having to load it all into RAM.

You don't even have to unzip it! Just edit the "gfile" variable in parse_word2vec.py to the filepath for your large .gz file.

The parse_word2vec.py file includes these functions:

- word2vec -- try word2vec("rabbit"); faster for more common words
- gvecs -- try gvecs(["rabbit", "carrot", "ghost"]); faster than word2vec for looking up multiple words at once; only as slow as the least common word
- gstream -- a generator that yields pairs (word, vec) in order from most common to least common word

Please credit Linus Hamilton if you use this program to make something cool.
