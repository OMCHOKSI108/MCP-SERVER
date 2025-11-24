import os
import json
import pandas as pd
from datetime import datetime
from tools.load_dataset import read_table_with_header_detection
from tools.analyze_sentiment import analyze_sentiment
from tools.cluster_data import cluster_data
from tools.extract_topics import extract_topics
from tools.generate_report import generate_report
from utils.data_utils import validate_dataset_loaded, get_dataset_info, get_sentiment_summary, get_cluster_summary, detect_text_column, detect_rating_column
from utils.logging_utils import setup_logging

logger = setup_logging()

def run_full_analysis(options: str) -> str:
    """
    Run a complete analysis workflow: load, clean, sentiment, cluster, topics, report.
    
    Args:
        options (str): JSON string with analysis options.
    
    Returns:
        str: JSON string with complete analysis results or error.
    """
    try:
        opts = json.loads(options)
        dataset_path = opts.get("dataset_path")
        text_column = opts.get("text_column")
        rating_column = opts.get("rating_column")
        k = opts.get("k", 3)
        
        if not dataset_path:
            return json.dumps({
                "success": False,
                "error": "Missing required option: dataset_path"
            })
        
        # Validate dataset path
        if not os.path.exists(dataset_path):
            return json.dumps({
                "success": False,
                "error": f"Dataset file not found: {dataset_path}"
            })
        
        # Create output directory
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_dir = f"outputs/run_{timestamp}"
        os.makedirs(output_dir, exist_ok=True)
        
        # Load DataFrame with normalized column names
        try:
            if dataset_path.endswith('.csv') or dataset_path.endswith('.tsv'):
                data = read_table_with_header_detection(dataset_path)
            elif dataset_path.endswith(('.xlsx', '.xls')):
                data = pd.read_excel(dataset_path)
            elif dataset_path.endswith('.json'):
                data = pd.read_json(dataset_path, orient='records')
            elif dataset_path.endswith('.parquet'):
                data = pd.read_parquet(dataset_path)
            else:
                return json.dumps({
                    "success": False,
                    "error": "Unsupported file format."
                })
        except Exception as e:
            return json.dumps({
                "success": False,
                "error": f"Failed to load dataset: {str(e)}"
            })
        
        # Auto-detect columns if not provided
        if not text_column:
            text_column = detect_text_column(data)
        if not rating_column:
            rating_column = detect_rating_column(data)
        
        # Validate detected columns
        if not text_column or text_column not in data.columns:
            return json.dumps({
                "success": False,
                "error": "No suitable text column detected or provided."
            })
        if not rating_column or rating_column not in data.columns:
            return json.dumps({
                "success": False,
                "error": "No suitable rating column detected or provided."
            })
        
        sentiment_result = analyze_sentiment(data, text_column)
        if not json.loads(sentiment_result).get("success", False):
            return sentiment_result
        
        cluster_result = cluster_data(data, None, k)  # Auto-detect features
        if not json.loads(cluster_result).get("success", False):
            return cluster_result
        
        topics_result = extract_topics(data, text_column, 10)
        if not json.loads(topics_result).get("success", False):
            return topics_result
        
        report_result = generate_report(data, "", output_dir)
        if not json.loads(report_result).get("success", False):
            return report_result
        
        # Parse results for summary
        try:
            dataset_info = json.loads(get_dataset_info(data))
            sentiment_summary = json.loads(get_sentiment_summary(data))
            cluster_summary = json.loads(get_cluster_summary(data))
            topics_data = json.loads(topics_result)
            generated_files_data = json.loads(report_result)
            
            # Build full file paths
            full_file_paths = []
            for file_name in generated_files_data.get("generated_files", []):
                full_path = os.path.join(output_dir, file_name)
                full_file_paths.append(full_path)
            
            # Collect summary
            summary = {
                "run_timestamp": timestamp,
                "output_directory": output_dir,
                "dataset_stats": {
                    "total_records": dataset_info.get("rows", 0),
                    "total_features": dataset_info.get("columns", 0),
                    "missing_values": dataset_info.get("missing_values", {})
                },
                "sentiment_summary": sentiment_summary,
                "cluster_summary": {
                    "cluster_sizes": cluster_summary.get("cluster_sizes", {}),
                    "cluster_means": cluster_summary.get("cluster_tendencies", {})
                },
                "top_topics": topics_data.get("data", {}).get("top_keywords", []),
                "generated_files": full_file_paths
            }
            
            logger.info(f"Completed full analysis run: {timestamp}")
            return json.dumps({"success": True, "data": summary})
            
        except json.JSONDecodeError as e:
            return json.dumps({
                "success": False,
                "error": f"Failed to parse analysis results: {str(e)}"
            })
    
    except json.JSONDecodeError:
        return json.dumps({
            "success": False,
            "error": "Invalid JSON in options parameter"
        })
    except Exception as e:
        error_msg = f"Unexpected error in full analysis: {str(e)}"
        logger.error(error_msg)
        return json.dumps({
            "success": False,
            "error": error_msg
        })