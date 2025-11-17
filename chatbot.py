import nltk
nltk.download("punkt_tab")
nltk.download("punkt")
nltk.download("stopwords")
nltk.download("wordnet")

import string
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer


# Load knowledge base
with open('got_knowledge_base.txt', 'r', encoding='utf-8') as f:
    data = f.read().replace('\n', ' ')


# Sentence tokenization
sentences = sent_tokenize(data)


# Preprocessing helpers
_stop_words = set(stopwords.words('english'))
_lemmatizer = WordNetLemmatizer()

def preprocess_to_tokens(text):
    words = word_tokenize(text)
    tokens = [
        _lemmatizer.lemmatize(w.lower())
        for w in words
        if w.lower() not in _stop_words and w not in string.punctuation
    ]
    return tokens

# ❗ CREATE CORPUS BEFORE DEFINING FUNCTIONS
corpus = [preprocess_to_tokens(s) for s in sentences]
original_sentences = sentences.copy()

# Special direct answers 
special_answers = {
"dragons": "Drogon, Rhaegal, and Viserion are Daenerys' dragons.",
"jaime": "Jaime Lannister (sometimes spelled Jamie) is a Lannister knight, known as the Kingslayer.",
"jon snow": "Jon Snow is raised as Ned Stark's illegitimate son and later revealed as Aegon Targaryen.",
"arya": "Arya Stark is a trained assassin who kills the Night King.",
"the wall": "The Wall was built by Bran the Builder and is guarded by the Night's Watch to protect the realms of men.",
}


# Precompute tokens for specials
_special_tokens = {k: set(preprocess_to_tokens(k)) for k in special_answers}

def get_top_relevant_sentences(query, top_n=5):
    q_tokens = set(preprocess_to_tokens(query))


    # check special answers first
    q_lower = query.lower()
    for key, answer in special_answers.items():
        if key in q_lower or _special_tokens[key].intersection(q_tokens):
            return [answer]


    scores = []
    for i, s_tokens in enumerate(corpus):
        union = len(set(s_tokens).union(q_tokens))
        sim = 0.0
    if union > 0:
        sim = len(set(s_tokens).intersection(q_tokens)) / union
        scores.append((sim, original_sentences[i]))


    scores.sort(reverse=True, key=lambda x: x[0])
    top = [s for sim, s in scores if sim > 0][:top_n]


    if not top:
    # fallback: return sentences that share any token
        for i, s_tokens in enumerate(corpus):
            if set(s_tokens).intersection(q_tokens):
                top.append(original_sentences[i])
                if len(top) >= top_n:
                    break


    if not top:
        return ["I'm not sure about that — try asking about characters, houses, or events."]


    # remove duplicates while preserving order
    seen = set()
    unique_top = []
    for s in top:
        if s not in seen:
            unique_top.append(s)
        seen.add(s)


    return unique_top



def chatbot(question, top_n=5):
    parts = get_top_relevant_sentences(question, top_n=top_n)
    # join into a coherent paragraph; optionally do minor deduplication
    answer = " ".join(parts)
    return answer




if __name__ == '__main__':
    while True:
        q = input('Ask (or "quit"): ')
        if q.strip().lower() in ('quit', 'exit'):
            break
        print(chatbot(q))