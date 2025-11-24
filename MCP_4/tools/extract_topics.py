import pandas as pd
import json
from sklearn.feature_extraction.text import TfidfVectorizer
from utils.data_utils import validate_dataset_loaded, validate_column_exists, detect_text_column
from utils.logging_utils import setup_logging

logger = setup_logging()

def extract_topics(data, column: str = None, top_n: int = 10) -> str:
    """
    Extract top topics/keywords from a text column using TF-IDF.
    
    Args:
        data (pd.DataFrame): The dataset.
        column (str): Name of the text column.
        top_n (int): Number of top keywords to extract.
    
    Returns:
        str: JSON string with top keywords.
    """
    if not validate_dataset_loaded(data):
        error_msg = "No dataset loaded."
        logger.error(error_msg)
        return json.dumps({"success": False, "error": error_msg})
    
    if column is None:
        column = detect_text_column(data)
        if column is None:
            error_msg = "No suitable text column found for topic extraction. Ensure your dataset has a column with text data."
            logger.error(error_msg)
            return json.dumps({"success": False, "error": error_msg})
    
    if not validate_column_exists(data, column):
        error_msg = f"Column '{column}' not found."
        logger.error(error_msg)
        return json.dumps({"success": False, "error": error_msg})
    
    if data[column].dtype != 'object':
        error_msg = f"Column '{column}' must be text/string type for topic extraction."
        logger.error(error_msg)
        return json.dumps({"success": False, "error": error_msg})
    
    if not isinstance(top_n, int) or top_n < 1:
        error_msg = "top_n must be a positive integer."
        logger.error(error_msg)
        return json.dumps({"success": False, "error": error_msg})
    
    try:
        texts = data[column].fillna('').astype(str)
        if texts.str.len().sum() == 0:
            error_msg = f"Column '{column}' contains no text data."
            logger.error(error_msg)
            return json.dumps({"success": False, "error": error_msg})
        
        vectorizer = TfidfVectorizer(stop_words='english', max_features=top_n)
        tfidf = vectorizer.fit_transform(texts)
        features = vectorizer.get_feature_names_out()
        logger.info(f"Extracted top {top_n} topics from column '{column}'")
        return json.dumps({"success": True, "data": {"top_keywords": list(features)}})
    except Exception as e:
        error_msg = f"Error in topic extraction: {str(e)}"
        logger.error(error_msg)
        return json.dumps({"success": False, "error": error_msg})