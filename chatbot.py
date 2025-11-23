import nltk
nltk.download("punkt")
nltk.download("stopwords")
nltk.download("wordnet")

import string
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer



# LOAD KNOWLEDGE BASE
with open('got_knowledge_base.txt', 'r', encoding='utf-8') as f:
    data = f.read().replace('\n', ' ')

sentences = sent_tokenize(data)


# PREPROCESSING SETUP
_stop_words = set(stopwords.words("english"))
_lemmatizer = WordNetLemmatizer()

def preprocess_to_tokens(text):
    words = word_tokenize(text)
    tokens = [
        _lemmatizer.lemmatize(w.lower())
        for w in words
        if w.lower() not in _stop_words and w not in string.punctuation
    ]
    return tokens


# CORPUS PREPARATION
corpus = [preprocess_to_tokens(s) for s in sentences]
original_sentences = sentences.copy()


# SPECIAL DIRECT ANSWERS (STRONG MATCHES)
special_answers = {
    "jaime": "Jaime Lannister is a knight of the Kingsguard known as the Kingslayer.",
    "jamie": "Jaime Lannister is a knight of the Kingsguard known as the Kingslayer.",
    "jon snow": "Jon Snow is Aegon Targaryen, the rightful heir to the Iron Throne.",
    "arya": "Arya Stark is a trained assassin who kills the Night King.",
    "dragons": "Daenerys' dragons are Drogon, Rhaegal, and Viserion.",
    "the wall": "The Wall protects the Seven Kingdoms from dangers beyond the North.",
    "starks": "The Starks are the ruling family of Winterfell and descendants of the First Men.",
}

_special_tokens = {k: set(preprocess_to_tokens(k)) for k in special_answers}


# IMPROVED RELEVANCE SCORING FUNCTION
def get_best_sentence(query):
    q_tokens = set(preprocess_to_tokens(query))
    q_lower = query.lower()

    # 1. STRONG SPECIAL DIRECT MATCH
    for key, answer in special_answers.items():
        if key in q_lower or _special_tokens[key].intersection(q_tokens):
            return answer

    # 2. SIMILARITY SCORING
    best_sentence = None
    best_score = 0

    for i, s_tokens in enumerate(corpus):
        # SKIP useless keyword sentences
        if "keywords" in original_sentences[i].lower():
            continue

        intersection = len(set(s_tokens).intersection(q_tokens))
        union = len(set(s_tokens).union(q_tokens))

        if union == 0:
            continue

        score = intersection / union

        if score > best_score:
            best_score = score
            best_sentence = original_sentences[i]

    # 3. GOOD THRESHOLD CHECK
    if best_sentence and best_score > 0:
        return best_sentence

    # 4. WEAK FALLBACK
    return "I’m not sure about that — try asking about characters, houses, dragons, or major events."


# FINAL CHATBOT FUNCTION
def chatbot(question):
    return get_best_sentence(question)
