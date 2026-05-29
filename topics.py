import gensim
from gensim import corpora
from gensim.models import LdaModel
from preprocessor import clean_text, remove_stopwords

def prepare_corpus(messages: list) -> tuple:
    texts = []
    for msg in messages:
        content = msg[0]
        cleaned = clean_text(content)
        filtered = remove_stopwords(cleaned)
        tokens = filtered.split()
        if tokens:
            texts.append(tokens)
    
    if not texts:
        return None, None
    
    dictionary = corpora.Dictionary(texts)
    dictionary.filter_extremes(no_below=2, no_above=0.9)
    corpus = [dictionary.doc2bow(text) for text in texts]
    
    return corpus, dictionary

def extract_topics(messages: list, num_topics: int = 3) -> list:
    if len(messages) < 10:
        return []
    
    corpus, dictionary = prepare_corpus(messages)
    
    if not corpus or not dictionary:
        return []
    
    lda_model = LdaModel(
        corpus=corpus,
        id2word=dictionary,
        num_topics=num_topics,
        random_state=42,
        passes=10,
        alpha='auto'
    )
    
    topics = []
    for idx, topic in lda_model.show_topics(
        num_topics=num_topics,
        num_words=5,
        formatted=False
    ):
        words = [word for word, prob in topic]
        topics.append({
            "topic_id": idx,
            "keywords": words,
        })
    
    return topics

def summarize_topics(topics: list) -> str:
    if not topics:
        return "not enough data to identify topics yet"
    
    summary = []
    for topic in topics:
        keywords = ", ".join(topic['keywords'])
        summary.append(f"Theme {topic['topic_id'] + 1}: {keywords}")
    
    return "\n".join(summary)