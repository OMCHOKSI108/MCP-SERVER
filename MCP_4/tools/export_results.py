import pandas as pd
import json
import os
from datetime import datetime
from utils.data_utils import validate_dataset_loaded
from utils.logging_utils import setup_logging

logger = setup_logging()

def export_results(data, format: str) -> str:
    """
    Export the processed dataset to CSV or JSON.
    
    Args:
        data (pd.DataFrame): The dataset.
        format (str): Export format ('csv' or 'json').
    
    Returns:
        str: JSON string with export result.
    """
    if not validate_dataset_loaded(data):
        error_msg = "No dataset loaded."
        logger.error(error_msg)
        return json.dumps({"success": False, "error": error_msg})
    
    if format.lower() not in ['csv', 'json']:
        error_msg = "Format must be 'csv' or 'json'."
        logger.error(error_msg)
        return json.dumps({"success": False, "error": error_msg})
    
    try:
        os.makedirs("outputs", exist_ok=True)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"outputs/processed_data_{timestamp}.{format.lower()}"
        
        if format.lower() == 'csv':
            data.to_csv(filename, index=False)
        elif format.lower() == 'json':
            data.to_json(filename, orient='records', indent=2)
        
        logger.info(f"Exported data to {filename}")
        return json.dumps({"success": True, "data": {"export_path": filename}})
    except Exception as e:
        error_msg = f"Error exporting data: {str(e)}"
        logger.error(error_msg)
        return json.dumps({"success": False, "error": error_msg})