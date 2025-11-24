import pandas as pd
import json
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from utils.data_utils import validate_dataset_loaded, get_cluster_summary, detect_rating_column
from utils.logging_utils import setup_logging

logger = setup_logging()

def cluster_data(data, features: list = None, k: int = 3) -> str:
    """
    Perform K-Means clustering on selected features.
    
    Args:
        data (pd.DataFrame): The dataset.
        features (list): List of feature column names.
        k (int): Number of clusters.
    
    Returns:
        str: JSON string with clustering results.
    """
    if not validate_dataset_loaded(data):
        error_msg = "No dataset loaded."
        logger.error(error_msg)
        return json.dumps({"success": False, "error": error_msg})
    
    if not isinstance(k, int) or k < 2:
        error_msg = "Number of clusters (k) must be an integer >= 2."
        logger.error(error_msg)
        return json.dumps({"success": False, "error": error_msg})
    
    if features is None or len(features) == 0:
        # Auto-detect features: prefer rating + sentiment_score, else all numeric columns
        rating_col = detect_rating_column(data)
        features = []
        if rating_col:
            features.append(rating_col)
        if 'sentiment_score' in data.columns:
            features.append('sentiment_score')
        if not features:
            # Fallback: all numeric columns
            numeric_cols = [col for col in data.columns if pd.api.types.is_numeric_dtype(data[col])]
            features = numeric_cols[:5]  # Limit to first 5 to avoid too many dimensions
        if not features:
            error_msg = "No suitable numeric features found for clustering. Ensure your dataset has numeric columns."
            logger.error(error_msg)
            return json.dumps({"success": False, "error": error_msg})
    
    missing_features = [f for f in features if f not in data.columns]
    if missing_features:
        error_msg = f"Features not found: {missing_features}"
        logger.error(error_msg)
        return json.dumps({"success": False, "error": error_msg})
    
    # Check if features are numeric
    non_numeric = [f for f in features if not pd.api.types.is_numeric_dtype(data[f])]
    if non_numeric:
        error_msg = f"Features must be numeric for clustering: {non_numeric}"
        logger.error(error_msg)
        return json.dumps({"success": False, "error": error_msg})
    
    try:
        data_subset = data[features].dropna()
        if len(data_subset) < k:
            error_msg = f"Insufficient data for {k} clusters. Only {len(data_subset)} valid rows after dropping NaN."
            logger.error(error_msg)
            return json.dumps({"success": False, "error": error_msg})
        
        scaler = StandardScaler()
        scaled = scaler.fit_transform(data_subset)
        kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
        clusters = kmeans.fit_predict(scaled)
        data.loc[data_subset.index, 'cluster'] = clusters
        logger.info(f"Performed K-Means clustering with {k} clusters on features: {features}")
        summary = get_cluster_summary(data)
        return json.dumps({"success": True, "data": json.loads(summary)})
    except Exception as e:
        error_msg = f"Error in clustering: {str(e)}"
        logger.error(error_msg)
        return json.dumps({"success": False, "error": error_msg})