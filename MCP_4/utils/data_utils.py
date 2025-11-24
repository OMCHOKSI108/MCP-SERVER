import pandas as pd
import json

def validate_dataset_loaded(data):
    """Check if dataset is loaded."""
    return data is not None

def validate_column_exists(data, column):
    """Check if column exists in dataset."""
    return column in data.columns

def get_dataset_info(data):
    """Get basic info about the dataset."""
    info = {
        "rows": len(data),
        "columns": len(data.columns),
        "column_names": list(data.columns),
        "missing_values": data.isnull().sum().to_dict(),
        "preview": data.head(10).to_dict(orient='records')
    }
    return json.dumps(info, indent=2)

def detect_rating_column(data):
    """Detect the most likely rating column: numeric with small integer range (1-5 or 1-10)."""
    if data is None or data.empty:
        return None
    for col in data.columns:
        if pd.api.types.is_numeric_dtype(data[col]):
            unique_vals = data[col].dropna().unique()
            if len(unique_vals) <= 10 and all(pd.api.types.is_number(v) and 1 <= v <= 10 for v in unique_vals):
                return col
    return None

def detect_text_column(data):
    """Detect the most likely text column: string dtype with largest average length."""
    if data is None or data.empty:
        return None
    text_cols = [col for col in data.columns if data[col].dtype == 'object']
    if not text_cols:
        return None
    avg_lengths = {col: data[col].astype(str).str.len().mean() for col in text_cols}
    return max(avg_lengths, key=avg_lengths.get)

def get_sentiment_summary(data):
    """Get sentiment distribution summary."""
    if 'sentiment' not in data.columns:
        return json.dumps({"error": "Sentiment analysis not performed."})
    summary = data['sentiment'].value_counts(normalize=True).mul(100).round(2).to_dict()
    return json.dumps(summary, indent=2)

def get_cluster_summary(data):
    """Get cluster size and tendencies."""
    if 'cluster' not in data.columns:
        return json.dumps({"error": "Clustering not performed."})
    cluster_counts = data['cluster'].value_counts().sort_index().to_dict()
    tendencies = {}
    numeric_cols = data.select_dtypes(include=[float, int]).columns
    for cluster in sorted(data['cluster'].unique()):
        cluster_data = data[data['cluster'] == cluster]
        tendencies[f"cluster_{cluster}"] = cluster_data[numeric_cols].mean().to_dict()
    summary = {
        "cluster_sizes": cluster_counts,
        "cluster_tendencies": tendencies
    }
    return json.dumps(summary, indent=2)