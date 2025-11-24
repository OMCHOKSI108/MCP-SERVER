import pandas as pd
import json
from utils.data_utils import get_dataset_info
from utils.logging_utils import setup_logging

logger = setup_logging()

def read_table_with_header_detection(path: str) -> pd.DataFrame:
    """
    Read a CSV/TSV file with intelligent header detection.
    
    Returns:
        pd.DataFrame: DataFrame with normalized column names.
    """
    if path.endswith('.tsv'):
        sep = '\t'
        read_func = lambda p, **kwargs: pd.read_csv(p, sep='\t', **kwargs)
    else:
        sep = ','
        read_func = pd.read_csv
    
    # Read sample without headers
    sample = read_func(path, header=None, nrows=5)
    if sample.empty:
        raise ValueError("File is empty or contains no data")
    
    first_row = sample.iloc[0]
    
    # Heuristic: check if first row looks like headers
    # Headers: mostly non-numeric, short strings (<=30 chars), and next rows look different
    is_header_like = True
    for val in first_row.dropna():
        if pd.api.types.is_number(val):
            is_header_like = False
            break
        if isinstance(val, str) and len(val) > 30:
            is_header_like = False
            break
    
    # Check if next rows look different (more numeric or longer text)
    if len(sample) > 1:
        second_row = sample.iloc[1]
        header_diff = 0
        for i, (h_val, d_val) in enumerate(zip(first_row, second_row)):
            if pd.api.types.is_number(d_val) and not pd.api.types.is_number(h_val):
                header_diff += 1
            elif isinstance(d_val, str) and isinstance(h_val, str) and len(d_val) > len(h_val):
                header_diff += 1
        if header_diff < len(first_row) * 0.5:  # Less than 50% different
            is_header_like = False
    
    if is_header_like:
        # Has headers
        df = read_func(path, header=0)
    else:
        # Headerless
        df = read_func(path, header=None)
        # Assign normalized names
        if len(df.columns) == 3:
            # Check pattern: [numeric, short text, long text]
            sample_row = df.iloc[0] if not df.empty else []
            if (len(sample_row) == 3 and 
                pd.api.types.is_number(sample_row[0]) and 
                isinstance(sample_row[1], str) and len(sample_row[1]) <= 50 and
                isinstance(sample_row[2], str) and len(sample_row[2]) > 50):
                df.columns = ['rating', 'title', 'review_text']
            else:
                df.columns = [f'col_{i}' for i in range(len(df.columns))]
        else:
            df.columns = [f'col_{i}' for i in range(len(df.columns))]
    
    return df
    """
    Load a dataset from CSV or Excel file.
    
    Args:
        path (str): Path to the CSV or Excel file.
        has_headers (bool): Whether the file has headers. If None, auto-detect.
    
    Returns:
        str: JSON string with dataset info and preview.
    """
def load_dataset(path: str, has_headers: bool = None) -> str:
    """
    Load a dataset from CSV or Excel file.
    
    Args:
        path (str): Path to the CSV or Excel file.
        has_headers (bool): Whether the file has headers. If None, auto-detect.
    
    Returns:
        str: JSON string with dataset info and preview.
    """
    try:
        if path.endswith('.csv') or path.endswith('.tsv'):
            data = read_table_with_header_detection(path)
        elif path.endswith(('.xlsx', '.xls')):
            data = pd.read_excel(path)
            # Excel usually has headers, but if has_headers False, could rename, but for now assume headers
            if has_headers is False:
                data.columns = [f"col_{i}" for i in range(len(data.columns))]
        elif path.endswith('.json'):
            # JSON files usually have structure, assume headers
            data = pd.read_json(path, orient='records')
            if has_headers is False:
                data.columns = [f"col_{i}" for i in range(len(data.columns))]
        elif path.endswith('.parquet'):
            try:
                data = pd.read_parquet(path)
                if has_headers is False:
                    data.columns = [f"col_{i}" for i in range(len(data.columns))]
            except ImportError:
                error_msg = "Parquet support requires 'pyarrow' or 'fastparquet'. Install with: pip install pyarrow"
                logger.error(error_msg)
                return json.dumps({"success": False, "error": error_msg})
        else:
            error_msg = "Unsupported file format. Supported: CSV, TSV, JSON, XLSX, XLS, Parquet."
            logger.error(error_msg)
            return json.dumps({"success": False, "error": error_msg})
        
        logger.info(f"Loaded dataset from {path}: {len(data)} rows, {len(data.columns)} columns")
        info = get_dataset_info(data)
        return json.dumps({"success": True, "data": json.loads(info)})
    except FileNotFoundError:
        error_msg = f"File not found: {path}"
        logger.error(error_msg)
        return json.dumps({"success": False, "error": error_msg})
    except pd.errors.EmptyDataError:
        error_msg = f"File is empty or contains no data: {path}"
        logger.error(error_msg)
        return json.dumps({"success": False, "error": error_msg})
    except pd.errors.ParserError:
        error_msg = f"Error parsing file (invalid format): {path}"
        logger.error(error_msg)
        return json.dumps({"success": False, "error": error_msg})
    except Exception as e:
        error_msg = f"Error loading dataset: {str(e)}"
        logger.error(error_msg)
        return json.dumps({"success": False, "error": error_msg})