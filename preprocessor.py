import re
import nltk
import spacy
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

nltk.download('stopwords', quiet=True)
nltk.download('punkt', quiet=True)
nltk.download('punkt_tab', quiet=True)

nlp = spacy.load("en_core_web_sm")

STOP_WORDS = set(stopwords.words('english'))

NOISE_PATTERNS = [
    r'http\S+',
    r'www\S+',
    r'@\w+',
    r'#\w+',
    r'\d+',
    r'[^\w\s]',
]

def clean_text(text:str) -> str:
    text = text.lower()
    for pattern in NOISE_PATTERNS:
        text = re.sub(pattern, '', text)
    text = ' '.join(text.split())
    return text
def remove_stopwords(text: str) -> str:
    tokens = word_tokenize(text)
    filtered = [word for word in tokens if word not in STOP_WORDS and len(word) > 2]
    return ' '.join(filtered)
def extract_entities(text: str) -> dict:
    doc = nlp(text)
    entities = {
        "times": [],
        "dates": [],
        "people": [],
        "places": [],
    }
    for ent in doc.ents:
        if ent.label_ == "TIME":
            entities["times"].append(ent.text)
        elif ent.label_ == "DATE":
            entities["dates"].append(ent.text)
        elif ent.label_ == "PERSON":
            entities["people"].append(ent.text)
        elif ent.label_ in ("GPE", "LOC"):
            entities["places"].append(ent.text)
    return entities
def extract_keywords(text: str) -> list:
    doc = nlp(text)
    keywords = [
        token.lemma_ for token in doc
        if not token.is_stop
        and not token.is_punct
        and token.pos_ in ("NOUN", "VERB", "ADJ")
        and len(token.text) > 2
    ]
    return keywords

def preprocess(text: str) -> dict:
    cleaned = clean_text(text)
    no_stops = remove_stopwords(cleaned)
    entities = extract_entities(text)
    keywords = extract_keywords(text)
    return {
        "cleaned": cleaned,
        "filtered": no_stops,
        "entities": entities,
        "keywords": keywords,
        "word_count": len(cleaned.split()),
    }