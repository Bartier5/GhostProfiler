from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
analyzer = SentimentIntensityAnalyzer()
def get_sentiment(text: str) -> dict:
    scores = analyzer.polarity_scores(text)
    compound = scores['compound']
    
    if compound >= 0.05:
        label = "positive"
    elif compound <= -0.05:
        label = "negative"
    else:
        label = "neutral"
    
    return {
        "score": compound,
        "label": label,
        "detail": scores
    }

def get_sentiment_trend(messages: list) -> dict:
    if not messages:
        return {}
    
    scores = [get_sentiment(msg)['score'] for msg in messages]
    average = sum(scores) / len(scores)
    
    first_half = scores[:len(scores)//2]
    second_half = scores[len(scores)//2:]
    
    first_avg = sum(first_half) / len(first_half) if first_half else 0
    second_avg = sum(second_half) / len(second_half) if second_half else 0
    
    drift = second_avg - first_avg
    
    if drift > 0.1:
        trend = "improving"
    elif drift < -0.1:
        trend = "declining"
    else:
        trend = "stable"
    
    return {
        "average_score": round(average, 3),
        "trend": trend,
        "drift": round(drift, 3),
        "scores": scores
    }