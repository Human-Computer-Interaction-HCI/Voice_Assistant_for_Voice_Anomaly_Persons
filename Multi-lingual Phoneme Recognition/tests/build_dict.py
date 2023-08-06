import nltk
words: set[str] = set()
with open('text.txt') as f:
    for line in f:
        words = words | set(nltk.word_tokenize(line, 'russian'))
print([i.lower() for i in words if all(map(str.isalpha, i))])