# SpellCheck
This is a NLP algorithm implemented on a corrupted file of Jane Austen's "Sense and Sensibility"

I build from scratch a spelling corrector in Python. It includes:
1. tokenization
2. Levenshtein distance-based non-word spelling correction
3. de-tokenization

As an example use case, I consider a version of Jane Austen’s Sense and Sensibility (available via nltk’s gutenberg corpus) corrupted by random insertions,
deletions, and substitutions. 

My spelling correction function:
• accepts a document as a single string and returns the corrected document as a single string.
• uses only standard libraries and numpy.
• use a English word list of 10,000 most popular words to correct my corrupted words from 
