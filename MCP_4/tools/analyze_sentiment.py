import pandas as pd
import json
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from utils.data_utils import validate_dataset_loaded, validate_column_exists, get_sentiment_summary, detect_text_column
from utils.logging_utils import setup_logging

logger = setup_logging()
analyzer = SentimentIntensityAnalyzer()

def analyze_sentiment(data, column: str = None) -> str:
    """
    Perform sentiment analysis on a text column using VADER.
    
    Args:
        data (pd.DataFrame): The dataset.
        column (str): Name of the text column. If None, auto-detect.
    
    Returns:
        str: JSON string with sentiment results.
    """
    try:
        if not validate_dataset_loaded(data):
            error_msg = "No dataset loaded. Please load a dataset first."
            logger.error(error_msg)
            return json.dumps({"success": False, "error": error_msg})
        
        if column is None:
            column = detect_text_column(data)
            if column is None:
                error_msg = "No suitable text column found for sentiment analysis. Ensure your dataset has a column with text data."
                logger.error(error_msg)
                return json.dumps({"success": False, "error": error_msg})
        
        if not validate_column_exists(data, column):
            error_msg = f"Column '{column}' not found in the dataset."
            logger.error(error_msg)
            return json.dumps({"success": False, "error": error_msg})
        
        if data[column].dtype != 'object':
            error_msg = f"Column '{column}' must be text/string type for sentiment analysis."
            logger.error(error_msg)
            return json.dumps({"success": False, "error": error_msg})
        
        if len(data) < 1:
            error_msg = "Dataset is empty. Cannot perform sentiment analysis."
            logger.error(error_msg)
            return json.dumps({"success": False, "error": error_msg})
        
        def get_sentiment(text):
            if pd.isna(text):
                return 'neutral', 0.0
            scores = analyzer.polarity_scores(str(text))
            compound = scores['compound']
            if compound >= 0.05:
                sentiment = 'positive'
            elif compound <= -0.05:
                sentiment = 'negative'
            else:
                sentiment = 'neutral'
            return sentiment, compound
        
        sentiments_and_scores = data[column].apply(get_sentiment)
        data['sentiment'] = sentiments_and_scores.apply(lambda x: x[0])
        data['sentiment_score'] = sentiments_and_scores.apply(lambda x: x[1])
        logger.info(f"Performed sentiment analysis on column '{column}'")
        summary = get_sentiment_summary(data)
        return json.dumps({"success": True, "data": json.loads(summary)})
    except Exception as e:
        error_msg = f"Unexpected error during sentiment analysis: {str(e)}"
        logger.error(error_msg)
        return json.dumps({"success": False, "error": error_msg})