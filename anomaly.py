import numpy as np
from sklearn.ensemble import IsolationForest
from collections import defaultdict

def build_behavioral_profile(messages: list) -> list:
    daily_stats = defaultdict(lambda: {
        "count": 0, 
        "total_sentiment": 0, 
        "total_length": 0
    })
    
    for msg in messages:
        content, timestamp, hour, day_of_week, msg_length, sentiment_score = msg
        date = timestamp.split(" ")[0] if timestamp else "unknown"
        
        daily_stats[date]["count"] += 1
        daily_stats[date]["total_sentiment"] += sentiment_score or 0
        daily_stats[date]["total_length"] += msg_length or 0
    
    profile = []
    for date, stats in daily_stats.items():
        count = stats["count"]
        avg_sentiment = stats["total_sentiment"] / count if count else 0
        avg_length = stats["total_length"] / count if count else 0
        profile.append([count, avg_sentiment, avg_length])
    
    return profile
def detect_anomalies(messages: list) -> dict:
    if len(messages) < 10:
        return {"anomalies": [], "status": "not enough data"}
    
    profile = build_behavioral_profile(messages)
    
    if len(profile) < 5:
        return {"anomalies": [], "status": "need more days of data"}
    
    data = np.array(profile)
    
    model = IsolationForest(
        contamination=0.15,
        random_state=42
    )
    
    predictions = model.fit_predict(data)
    scores = model.decision_function(data)
    
    anomalies = []
    for i, pred in enumerate(predictions):
        if pred == -1:
            anomalies.append({
                "day_index": i,
                "deviation_score": round(float(scores[i]), 3),
                "messages_that_day": int(profile[i][0]),
                "avg_sentiment": round(float(profile[i][1]), 3),
                "avg_length": round(float(profile[i][2]), 3),
            })
    
    return {
        "anomalies": anomalies,
        "total_days_analyzed": len(profile),
        "anomaly_count": len(anomalies),
        "status": "complete"
    }
def interpret_anomalies(anomaly_data: dict) -> str:
    anomalies = anomaly_data.get("anomalies", [])
    
    if not anomalies:
        return "your behavior has been consistent. no significant deviations detected."
    
    insights = []
    for a in anomalies:
        sentiment = a['avg_sentiment']
        msg_count = a['messages_that_day']
        length = a['avg_length']
        
        if msg_count == 0:
            insight = "you went completely silent that day. said nothing."
        elif sentiment < -0.3 and length > 100:
            insight = f"you were sending long, heavy messages that day. sentiment was low at {sentiment}. something was eating at you."
        elif sentiment > 0.3 and msg_count > 10:
            insight = f"unusually active and positive that day — {msg_count} messages. something good happened."
        else:
            insight = f"something was off that day. {msg_count} messages, average mood: {sentiment}."
        
        insights.append(insight)
    
    return "\n".join(insights)