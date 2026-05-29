from collections import defaultdict, Counter
from itertools import combinations

def extract_time_patterns(messages: list) -> dict:
    hour_counts = Counter()
    day_counts = Counter()
    hour_sentiment = defaultdict(list)
    
    for msg in messages:
        content, timestamp, hour, day_of_week, msg_length, sentiment_score = msg
        
        if hour is not None:
            hour_counts[hour] += 1
            if sentiment_score is not None:
                hour_sentiment[hour].append(sentiment_score)
        
        if day_of_week is not None:
            day_counts[day_of_week] += 1
    
    peak_hour = hour_counts.most_common(1)[0] if hour_counts else None
    peak_day = day_counts.most_common(1)[0] if day_counts else None
    
    worst_hour = min(
        hour_sentiment.keys(),
        key=lambda h: sum(hour_sentiment[h]) / len(hour_sentiment[h])
    ) if hour_sentiment else None
    
    best_hour = max(
        hour_sentiment.keys(),
        key=lambda h: sum(hour_sentiment[h]) / len(hour_sentiment[h])
    ) if hour_sentiment else None
    
    return {
        "peak_hour": peak_hour,
        "peak_day": peak_day,
        "worst_hour": worst_hour,
        "best_hour": best_hour,
        "hour_distribution": dict(hour_counts.most_common(5)),
    }
def extract_behavioral_sequences(messages: list) -> list:
    sequences = []
    
    for i in range(len(messages) - 1):
        current = messages[i]
        next_msg = messages[i + 1]
        
        curr_sentiment = current[5] or 0
        next_sentiment = next_msg[5] or 0
        curr_hour = current[2] or 0
        next_hour = next_msg[2] or 0
        curr_length = current[4] or 0
        
        if curr_hour >= 22 and curr_sentiment < -0.2:
            sequences.append("late_night_negative")
        
        if curr_length > 200 and next_sentiment < curr_sentiment:
            sequences.append("long_message_mood_drop")
            
        if curr_sentiment < -0.3 and next_sentiment > 0.3:
            sequences.append("rapid_mood_recovery")
            
        if curr_hour >= 22 and curr_length > 150:
            sequences.append("late_night_long_rant")
    
    sequence_counts = Counter(sequences)
    
    return [
        {"pattern": pattern, "occurrences": count}
        for pattern, count in sequence_counts.most_common()
        if count >= 2
    ]
def extract_vocabulary_patterns(messages: list) -> dict:
    all_words = []
    negative_words = []
    positive_words = []
    
    negative_threshold = -0.2
    positive_threshold = 0.2
    
    for msg in messages:
        content, timestamp, hour, day_of_week, msg_length, sentiment_score = msg
        words = content.lower().split() if content else []
        all_words.extend(words)
        
        if sentiment_score and sentiment_score < negative_threshold:
            negative_words.extend(words)
        elif sentiment_score and sentiment_score > positive_threshold:
            positive_words.extend(words)
    
    filler_words = {'the', 'a', 'an', 'is', 'it', 'i', 'to', 'and', 
                    'of', 'in', 'that', 'you', 'was', 'for', 'on',
                    'are', 'with', 'as', 'at', 'be', 'this', 'have'}
    
    def top_words(word_list, n=10):
        filtered = [w for w in word_list if w not in filler_words and len(w) > 2]
        return Counter(filtered).most_common(n)
    
    return {
        "most_used_words": top_words(all_words),
        "words_when_negative": top_words(negative_words),
        "words_when_positive": top_words(positive_words),
    }