import pandas as pd
import json
from utils.data_utils import validate_dataset_loaded
from utils.logging_utils import setup_logging

logger = setup_logging()

def clean_data(data, options: dict = {}) -> str:
    """
    Perform data cleaning operations on the dataset.
    
    Args:
        data (pd.DataFrame): The dataset.
        options (dict): Cleaning options like fill_missing, drop_duplicates, etc.
    
    Returns:
        str: JSON string with cleaning results.
    """
    if not validate_dataset_loaded(data):
        error_msg = "No dataset loaded."
        logger.error(error_msg)
        return json.dumps({"error": error_msg})
    
    try:
        original_shape = data.shape
        changes = []
        
        # Drop duplicates
        if options.get('drop_duplicates', True):
            before = len(data)
            data = data.drop_duplicates()
            after = len(data)
            if before != after:
                changes.append(f"Dropped {before - after} duplicate rows")
        
        # Handle missing values
        if options.get('fill_missing', True):
            for col in data.columns:
                if data[col].dtype in ['float64', 'int64']:
                    # Numeric: fill with mean
                    if data[col].isnull().sum() > 0:
                        mean_val = data[col].mean()
                        data[col] = data[col].fillna(mean_val)
                        changes.append(f"Filled missing values in numeric column '{col}' with mean: {mean_val:.2f}")
                elif data[col].dtype == 'object':
                    # Categorical/Text: fill with mode
                    if data[col].isnull().sum() > 0:
                        mode_val = data[col].mode()
                        if not mode_val.empty:
                            data[col] = data[col].fillna(mode_val[0])
                            changes.append(f"Filled missing values in column '{col}' with mode: {mode_val[0]}")
        
        # Remove columns with too many missing values
        if options.get('remove_high_missing', True):
            threshold = options.get('missing_threshold', 0.5)  # 50%
            cols_to_drop = []
            for col in data.columns:
                missing_ratio = data[col].isnull().sum() / len(data)
                if missing_ratio > threshold:
                    cols_to_drop.append(col)
                    changes.append(f"Removed column '{col}' with {missing_ratio:.1%} missing values")
            data = data.drop(columns=cols_to_drop)
        
        new_shape = data.shape
        changes.insert(0, f"Dataset shape changed from {original_shape} to {new_shape}")
        
        logger.info(f"Data cleaning completed: {changes}")
        return json.dumps({
            "success": True,
            "data": {
                "changes": changes,
                "new_shape": new_shape,
                "columns": list(data.columns)
            }
        })
    except Exception as e:
        error_msg = f"Error during data cleaning: {str(e)}"
        logger.error(error_msg)
        return json.dumps({"success": False, "error": error_msg})