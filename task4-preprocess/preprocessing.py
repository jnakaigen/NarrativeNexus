#task4
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer, WordNetLemmatizer
import warnings

# Suppress NLTK warnings
warnings.filterwarnings('ignore')

# --- SETUP: Download necessary NLTK data (only runs once) ---
nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)
nltk.download('wordnet', quiet=True)
nltk.download('omw-1.4', quiet=True)
nltk.download('punkt_tab', quiet=True)


STEMMER = PorterStemmer()
LEMMATIZER = WordNetLemmatizer()
STOP_WORDS = set(stopwords.words('english'))
CLEAN_PATTERN = re.compile(r'[^a-zA-Z\s]')

# --- INPUT: Financial Document ---
with open(r'..\processed_data\financial doc.md', 'r', encoding='utf-8') as file:
    financial_text = file.read()

def preprocess_financial_data(text):
    """
    Preprocessing pipeline for financial documents.
    Args:
        text (str): Raw text to preprocess
    Returns:
        tuple: (filtered_tokens, stemmed_version, lemmatized_version)
    """
    # 1. CLEAN: Remove symbols, numbers, and irrelevant characters
    cleaned_text = CLEAN_PATTERN.sub('', text).lower()
    
    # 2. TOKENIZE: Split text into individual words (using split for cleaned text)
    tokens = cleaned_text.split()
    
    # 3. REMOVE STOPWORDS: Filter out common words in one pass
    filtered_tokens = [word for word in tokens if word and word not in STOP_WORDS]
    
    # 4. STEMMING & LEMMATIZATION: Process in single pass with mapping
    stemmed_version = [STEMMER.stem(word) for word in filtered_tokens]
    lemmatized_version = [LEMMATIZER.lemmatize(word) for word in filtered_tokens]
    
    return filtered_tokens, stemmed_version, lemmatized_version

clean_tokens, stemmed, lemmatized = preprocess_financial_data(financial_text)

print(f"ORIGINAL (Filtered): {clean_tokens[:10]}...")
print("-" * 50)
print(f"VERSION A (Stemming):     {stemmed[:10]}...")
print(f"VERSION B (Lemmatization):{lemmatized[:10]}...")


print("\n--- SPECIFIC DIFFERENCES ---")
token_to_indices = {word: [] for word in clean_tokens}
for idx, word in enumerate(clean_tokens):
    token_to_indices[word].append(idx)

words_to_check = ["balanced", "financial", "grew", "cash", "accounting" , "years", "profit", "loss", "assets", "liabilities"]
for word in words_to_check:
    if word in token_to_indices:
        idx = token_to_indices[word][0]  # Get first occurrence
        print(f"Word: {word:12} | Stem: {stemmed[idx]:12} | Lemma: {lemmatized[idx]}")

# --- OUTPUT: Write stemming and lemmatization results to separate .md files ---

# Create Stemming Results
stemming_text = " ".join(stemmed)
stemming_output = "# Stemming Results\n\n"
stemming_output += stemming_text

with open(r'..\processed_data\stemming_results.md', 'w', encoding='utf-8') as file:
    file.write(stemming_output)

# Create Lemmatization Results
lemmatization_text = " ".join(lemmatized)
lemmatization_output = "# Lemmatization Results\n\n"
lemmatization_output += lemmatization_text

with open(r'..\processed_data\lemmatization_results.md', 'w', encoding='utf-8') as file:
    file.write(lemmatization_output)

print("\n✓ Stemming results saved to: processed_data/stemming_results.md")
print("✓ Lemmatization results saved to: processed_data/lemmatization_results.md")