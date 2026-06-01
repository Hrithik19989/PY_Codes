import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

# 1. Sample text to process
text = "The quick brown fox jumps over the lazy dog."

# 2. Tokenise: Break the string into a list of words
words = word_tokenize(text)
print("Tokenised Words:", words)
# Output: ['The', 'quick', 'brown', 'fox', 'jumps', 'over', 'the', 'lazy', 'dog', '.']

# 3. Filter: Remove standard English stopwords
stop_words = set(stopwords.words('english'))
filtered_words = [w for w in words if w.lower() not in stop_words]
print("Filtered Words:", filtered_words)
# Output: ['quick', 'brown', 'fox', 'jumps', 'lazy', 'dog', '.']
