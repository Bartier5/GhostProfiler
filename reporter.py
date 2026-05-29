from groq import Groq
from config import GROQ_API_KEY, GROQ_MODEL
from sentiment import get_sentiment_trend
from clustering import cluster_messages, interpret_clusters
from topics import extract_topics, summarize_topics
from anomaly import detect_anomalies, interpret_anomalies
from patterns import extract_time_patterns, extract_behavioral_sequences, extract_vocabulary_patterns

client = Groq(api_key=GROQ_API_KEY)
def compile_analysis(messages: list) -> dict:
    sentiment_data = get_sentiment_trend([msg[0] for msg in messages])
    cluster_data = interpret_clusters(cluster_messages(messages))
    topic_data = summarize_topics(extract_topics(messages))
    anomaly_data = interpret_anomalies(detect_anomalies(messages))
    time_patterns = extract_time_patterns(messages)
    sequences = extract_behavioral_sequences(messages)
    vocab = extract_vocabulary_patterns(messages)
    
    return {
        "sentiment": sentiment_data,
        "clusters": cluster_data,
        "topics": topic_data,
        "anomalies": anomaly_data,
        "time_patterns": time_patterns,
        "sequences": sequences,
        "vocabulary": vocab,
        "message_count": len(messages)
    }
def generate_ghost_report(analysis: dict, report_type: str = "weekly") -> str:
    if report_type == "weekly":
        instruction = """
        You are GhostProfiler — a brutally honest AI that has been silently 
        watching this person's messages for a week. You speak with zero filter, 
        zero corporate softness. You curse if it fits. You don't encourage. 
        You don't comfort. You just tell them exactly what their data shows 
        about them, like a cold mirror. Be direct. Be real. Be specific.
        Write in second person — talk TO them, not about them.
        """
    else:
        instruction = """
        You are GhostProfiler — you have watched this person silently for 
        a full month. This is The Mirror — your monthly full psychological 
        profile of them based purely on their behavioral data. Be ruthless 
        with honesty. Identify their patterns, their recurring struggles, 
        their moments of life. No sugarcoating. Speak like someone who 
        knows them better than they know themselves.
        """
    
    prompt = f"""
    {instruction}
    
    Here is their behavioral data:
    
    SENTIMENT: Average score {analysis['sentiment'].get('average_score', 0)}, 
    trend is {analysis['sentiment'].get('trend', 'unknown')}.
    
    BEHAVIORAL CLUSTERS: {analysis['clusters']}
    
    RECURRING TOPICS: {analysis['topics']}
    
    ANOMALIES: {analysis['anomalies']}
    
    TIME PATTERNS: Most active hour — {analysis['time_patterns'].get('peak_hour')}.
    Worst emotional hour — {analysis['time_patterns'].get('worst_hour')}.
    Best emotional hour — {analysis['time_patterns'].get('best_hour')}.
    
    BEHAVIORAL SEQUENCES: {analysis['sequences']}
    
    VOCABULARY: Most used words — {analysis['vocabulary'].get('most_used_words')}.
    Words when negative — {analysis['vocabulary'].get('words_when_negative')}.
    Words when positive — {analysis['vocabulary'].get('words_when_positive')}.
    
    Total messages analyzed: {analysis['message_count']}
    
    Write the report now.
    """
    
    response = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1000,
        temperature=0.85
    )
    
    return response.choices[0].message.content
async def generate_and_save_report(user_id: int, messages: list, 
                                    report_type: str, save_func) -> str:
    if len(messages) < 10:
        return "not enough data yet. keep talking."
    
    analysis = compile_analysis(messages)
    report = generate_ghost_report(analysis, report_type)
    
    await save_func(user_id, report_type, report)
    
    return report