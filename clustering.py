import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from collections import Counter

def build_feature_matrix(messages: list) -> np.ndarray:
    features = []
    for msg in messages:
        content, timestamp, hour, day_of_week, msg_length, sentiment_score = msg
        features.append([
            hour if hour else 0,
            day_of_week if day_of_week else 0,
            msg_length if msg_length else 0,
            sentiment_score if sentiment_score else 0.0,
        ])
    return np.array(features)
def cluster_messages(messages: list, n_clusters: int = 3) -> dict:
    if len(messages) < n_clusters:
        return {"error": "not enough messages to cluster"}
    
    matrix = build_feature_matrix(messages)
    
    scaler = StandardScaler()
    scaled = scaler.fit_transform(matrix)
    
    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    labels = kmeans.fit_predict(scaled)
    
    clusters = {}
    for i in range(n_clusters):
        cluster_indices = np.where(labels == i)[0]
        cluster_messages = [messages[j] for j in cluster_indices]
        
        hours = [messages[j][2] for j in cluster_indices]
        days = [messages[j][3] for j in cluster_indices]
        sentiments = [messages[j][5] for j in cluster_indices if messages[j][5]]
        lengths = [messages[j][4] for j in cluster_indices]
        
        clusters[f"cluster_{i}"] = {
            "size": len(cluster_messages),
            "avg_hour": round(np.mean(hours), 1) if hours else 0,
            "avg_sentiment": round(np.mean(sentiments), 3) if sentiments else 0,
            "avg_length": round(np.mean(lengths), 1) if lengths else 0,
            "common_days": Counter(days).most_common(2),
        }
    
    return clusters
def interpret_clusters(clusters: dict) -> list:
    insights = []
    for name, data in clusters.items():
        hour = data['avg_hour']
        sentiment = data['avg_sentiment']
        length = data['avg_length']
        
        if hour >= 22 or hour <= 4:
            time_label = "late night"
        elif hour >= 5 and hour <= 11:
            time_label = "morning"
        elif hour >= 12 and hour <= 17:
            time_label = "afternoon"
        else:
            time_label = "evening"
        
        mood = "positive" if sentiment > 0.05 else "negative" if sentiment < -0.05 else "neutral"
        
        insights.append({
            "time": time_label,
            "mood": mood,
            "avg_message_length": length,
            "message_count": data['size']
        })
    
    return insights