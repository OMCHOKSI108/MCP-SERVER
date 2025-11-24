import pandas as pd
import json
from fastmcp import FastMCP
from tools.load_dataset import load_dataset
from tools.analyze_sentiment import analyze_sentiment
from tools.cluster_data import cluster_data
from tools.extract_topics import extract_topics
from tools.generate_report import generate_report
from tools.run_full_analysis import run_full_analysis
from tools.data_cleaning import clean_data
from tools.export_results import export_results
from utils.logging_utils import setup_logging

logger = setup_logging()

# Global state for current dataset
current_data = None

mcp = FastMCP("AI Workflow Orchestrator MCP")

@mcp.tool()
def load_dataset_tool(path: str) -> str:
    """Load a dataset from CSV or Excel file."""
    global current_data
    result_str = load_dataset(path)
    result = json.loads(result_str)
    if result.get("success"):
        # Load data for current_data
        if path.endswith('.csv'):
            current_data = pd.read_csv(path)
        elif path.endswith(('.xlsx', '.xls')):
            current_data = pd.read_excel(path)
    return result_str

@mcp.tool()
def clean_data_tool(options: str = "{}") -> str:
    """Clean the loaded dataset (remove duplicates, fill missing values, etc.)."""
    global current_data
    try:
        opts = json.loads(options) if options else {}
    except:
        opts = {}
    result = clean_data(current_data, opts)
    if "error" not in result:
        # Update current_data after cleaning
        # But since clean_data modifies in place, it's already updated
        pass
    return result

@mcp.tool()
def analyze_sentiment_tool(column: str) -> str:
    """Analyze sentiment on a text column."""
    global current_data
    return analyze_sentiment(current_data, column)

@mcp.tool()
def cluster_data_tool(features: list, k: int) -> str:
    """Cluster data using K-Means."""
    global current_data
    return cluster_data(current_data, features, k)

@mcp.tool()
def extract_topics_tool(column: str, top_n: int = 10) -> str:
    """Extract top topics/keywords from text."""
    global current_data
    return extract_topics(current_data, column, top_n)

@mcp.tool()
def generate_report_tool(options: str = "") -> str:
    """Generate a summary report."""
    global current_data
    return generate_report(current_data, options)

@mcp.tool()
def export_results_tool(format: str) -> str:
    """Export processed results."""
    global current_data
    return export_results(current_data, format)

@mcp.tool()
def run_full_analysis_tool(options: str) -> str:
    """Run a complete automated analysis workflow."""
    return run_full_analysis(options)