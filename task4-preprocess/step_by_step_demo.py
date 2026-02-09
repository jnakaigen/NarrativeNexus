import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer, WordNetLemmatizer
import warnings

warnings.filterwarnings('ignore')

# Download necessary data
nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)
nltk.download('wordnet', quiet=True)
nltk.download('omw-1.4', quiet=True)
nltk.download('punkt_tab', quiet=True)

# Initialize tools
STEMMER = PorterStemmer()
LEMMATIZER = WordNetLemmatizer()
STOP_WORDS = set(stopwords.words('english'))
CLEAN_PATTERN = re.compile(r'[^a-zA-Z\s]')

# Sample sentence from the financial document
sample_sentence = "The World Intellectual Property Organization's financial statements for the year ended December 31, 2020, show impressive growth and resilient performance."

print("=" * 80)
print("PREPROCESSING PIPELINE DEMONSTRATION")
print("=" * 80)

print("\nORIGINAL SENTENCE:")
print(f"   {sample_sentence}")

# Step 1: Clean
print("\n" + "─" * 80)
print("STEP 1: CLEAN - Remove symbols, numbers, and irrelevant characters")
print("─" * 80)
cleaned_text = CLEAN_PATTERN.sub('', sample_sentence).lower()
print(f"   {cleaned_text}")

# Step 2: Tokenize
print("\n" + "─" * 80)
print("STEP 2: TOKENIZE - Split text into individual words")
print("─" * 80)
tokens = cleaned_text.split()
print(f"   {tokens}")
print(f"   Total tokens: {len(tokens)}")

# Step 3: Remove Stopwords
print("\n" + "─" * 80)
print("STEP 3: REMOVE STOPWORDS - Filter out common words (the, and, is, etc.)")
print("─" * 80)
filtered_tokens = [word for word in tokens if word and word not in STOP_WORDS]
print(f"   Filtered tokens: {filtered_tokens}")
print(f"   Removed {len(tokens) - len(filtered_tokens)} stopwords")
print(f"   Tokens remaining: {len(filtered_tokens)}")

# Step 4: Stemming
print("\n" + "─" * 80)
print("STEP 4A: STEMMING - Apply Porter Stemmer")
print("─" * 80)
stemmed_tokens = [STEMMER.stem(word) for word in filtered_tokens]
print(f"   Stemmed tokens: {stemmed_tokens}")
stemmed_sentence = " ".join(stemmed_tokens)
print(f"\n   Full stemmed sentence:")
print(f"   {stemmed_sentence}")

# Step 5: Lemmatization
print("\n" + "─" * 80)
print("STEP 4B: LEMMATIZATION - Apply WordNet Lemmatizer")
print("─" * 80)
lemmatized_tokens = [LEMMATIZER.lemmatize(word) for word in filtered_tokens]
print(f"   Lemmatized tokens: {lemmatized_tokens}")
lemmatized_sentence = " ".join(lemmatized_tokens)
print(f"\n   Full lemmatized sentence:")
print(f"   {lemmatized_sentence}")

# Comparison
print("\n" + "=" * 80)
print("COMPARISON: STEMMING vs LEMMATIZATION")
print("=" * 80)
print(f"\n{'Original':<20} {'Stemmed':<20} {'Lemmatized':<20}")
print("─" * 80)
for orig, stem, lemma in zip(filtered_tokens, stemmed_tokens, lemmatized_tokens):
    print(f"{orig:<20} {stem:<20} {lemma:<20}")

print("\n" + "=" * 80)
