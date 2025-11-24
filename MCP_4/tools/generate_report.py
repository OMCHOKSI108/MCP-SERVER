import os
import json
import matplotlib.pyplot as plt
from datetime import datetime
from utils.data_utils import validate_dataset_loaded, get_sentiment_summary, get_cluster_summary, detect_rating_column, detect_text_column
from utils.logging_utils import setup_logging
from sklearn.preprocessing import StandardScaler
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import letter

logger = setup_logging()

def get_top_keywords(texts, top_n=5):
    if not texts or len(texts) < 2:
        return ["insufficient data"]
    vectorizer = TfidfVectorizer(stop_words='english', max_features=100)
    tfidf = vectorizer.fit_transform(texts)
    feature_names = vectorizer.get_feature_names_out()
    scores = tfidf.sum(axis=0).A1
    top_indices = scores.argsort()[-top_n:][::-1]
    return [feature_names[i] for i in top_indices]

def generate_report(data, options: str = "", output_dir: str = "outputs") -> str:
    """
    Generate a markdown report summarizing the analysis with charts.
    
    Args:
        data (pd.DataFrame): The dataset.
        options (str): Additional options (not used yet).
        output_dir (str): Directory to save report and plots.
    
    Returns:
        str: JSON string with paths to generated files.
    """
    if not validate_dataset_loaded(data):
        error_msg = "No dataset loaded."
        logger.error(error_msg)
        return json.dumps({"success": False, "error": error_msg})
    
    if not output_dir:
        output_dir = "."
    
    try:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_dir = os.path.abspath(os.path.join("outputs", f"run_{timestamp}"))
        os.makedirs(output_dir, exist_ok=True)
        report_lines = []
        report_lines.append("# AI Workflow Orchestrator MCP - Comprehensive Analysis Report")
        report_lines.append(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report_lines.append("")
        report_lines.append("## Executive Summary")
        report_lines.append("This report provides an automated analysis of customer reviews, including sentiment evaluation, customer segmentation through clustering, and key topic identification. The insights derived can inform product improvements, customer service strategies, and marketing efforts.")
        report_lines.append("")
        
        # Dataset Overview
        report_lines.append("## Dataset Overview")
        report_lines.append(f"- **Total Records**: {len(data)}")
        report_lines.append(f"- **Features Analyzed**: {len(data.columns)}")
        report_lines.append(f"- **Data Completeness**: {data.isnull().sum().sum()} missing values across all columns")
        report_lines.append("")
        
        generated_files = []
        
        # Sentiment Analysis
        if 'sentiment' in data.columns:
            report_lines.append("## Sentiment Analysis")
            sentiment_data = json.loads(get_sentiment_summary(data))
            total_reviews = sum(sentiment_data.values())
            report_lines.append(f"Analysis of {total_reviews} reviews reveals the following sentiment distribution:")
            for sentiment, count in sentiment_data.items():
                percentage = (count / total_reviews) * 100
                report_lines.append(f"{sentiment.capitalize()}: {percentage:.1f}%")
            report_lines.append("")
            
            # Sentiment bar chart
            sentiments = list(sentiment_data.keys())
            counts = list(sentiment_data.values())
            plt.figure(figsize=(10, 6))
            bars = plt.bar(sentiments, counts, color=['green', 'red', 'blue'])
            plt.title('Customer Sentiment Distribution', fontsize=14, fontweight='bold')
            plt.ylabel('Number of Reviews', fontsize=12)
            plt.xlabel('Sentiment Category', fontsize=12)
            plt.grid(axis='y', alpha=0.3)
            for bar, count in zip(bars, counts):
                plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1, str(count), ha='center', va='bottom')
            sentiment_chart = f"sentiment_distribution_{timestamp}.png"
            plt.savefig(os.path.join(output_dir, sentiment_chart))
            plt.close()
            report_lines.append(f"![Sentiment Distribution]({sentiment_chart})")
            generated_files.append(os.path.join(output_dir, sentiment_chart))
            report_lines.append("")
        
        skip_clustering = False
        if 'cluster' in data.columns:
            # Check variance of clustering features
            rating_col = detect_rating_column(data)
            features = []
            if rating_col:
                features.append(rating_col)
            if 'sentiment_score' in data.columns:
                features.append('sentiment_score')
            if features:
                data_subset = data[features].dropna()
                if len(data_subset) > 1:
                    scaler = StandardScaler()
                    scaled = scaler.fit_transform(data_subset)
                    variances = scaled.var(axis=0)
                    if variances.max() < 0.1:
                        skip_clustering = True
                        data = data.drop('cluster', axis=1, errors='ignore')
        
        # Clustering Results
        if 'cluster' in data.columns and not skip_clustering:
            report_lines.append("## Customer Segmentation Analysis")
            cluster_data = json.loads(get_cluster_summary(data))
            report_lines.append(f"Customers have been segmented into {len(cluster_data['cluster_sizes'])} distinct groups using K-Means clustering on rating and sentiment scores.")
            report_lines.append("")
            report_lines.append("### Cluster Profiles")
            
            rating_col = detect_rating_column(data)
            text_col = detect_text_column(data)
            
            for cluster_id, size in cluster_data['cluster_sizes'].items():
                report_lines.append(f"#### Cluster {cluster_id} ({size} customers)")
                tendencies = cluster_data['cluster_tendencies'][f"cluster_{cluster_id}"]
                avg_rating = tendencies.get(rating_col if rating_col else 'rating', tendencies.get('2', 0))
                avg_sentiment = tendencies.get('sentiment_score', 0)
                
                report_lines.append(f"- **Average Rating**: {avg_rating:.2f}/5")
                report_lines.append(f"- **Average Sentiment Score**: {avg_sentiment:.3f}")
                
                # Top keywords for this cluster
                if text_col:
                    cluster_texts = data[data['cluster'] == cluster_id][text_col].dropna().astype(str).tolist()
                    cluster_keywords = get_top_keywords(cluster_texts, 3)
                    if cluster_keywords and cluster_keywords[0] != "insufficient data":
                        report_lines.append(f"- **Key Themes**: {', '.join(cluster_keywords)}")
                
                report_lines.append("")
            
            # Cluster pie chart
            sizes = list(cluster_data['cluster_sizes'].values())
            labels = [f"Cluster {cid}" for cid in cluster_data['cluster_sizes'].keys()]
            plt.figure(figsize=(10, 8))
            plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140, colors=plt.cm.tab10.colors)
            plt.title('Customer Cluster Distribution', fontsize=14, fontweight='bold')
            cluster_pie = f"cluster_distribution_{timestamp}.png"
            plt.savefig(os.path.join(output_dir, cluster_pie))
            plt.close()
            report_lines.append(f"![Cluster Distribution]({cluster_pie})")
            generated_files.append(os.path.join(output_dir, cluster_pie))
            report_lines.append("")
            
            # Enhanced Scatter plot
            plt.figure(figsize=(12, 8))
            colors = plt.cm.tab10.colors
            for i, cluster_id in enumerate(sorted(data['cluster'].unique())):
                cluster_points = data[data['cluster'] == cluster_id]
                color = colors[i % len(colors)]
                plt.scatter(cluster_points[rating_col if rating_col else data.columns[0]], 
                           cluster_points['sentiment_score'], 
                           label=f'Cluster {cluster_id}', alpha=0.7, s=50, c=[color])
            plt.title('Customer Segmentation: Rating vs Sentiment Score', fontsize=14, fontweight='bold')
            plt.xlabel('Product Rating', fontsize=12)
            plt.ylabel('Sentiment Score', fontsize=12)
            plt.legend(title='Customer Segments')
            plt.grid(alpha=0.3)
            plt.axhline(y=0, color='gray', linestyle='--', alpha=0.5)
            plt.axvline(x=3, color='red', linestyle='--', alpha=0.5, label='Neutral Rating')
            scatter_plot = f"cluster_scatter_{timestamp}.png"
            plt.savefig(os.path.join(output_dir, scatter_plot))
            plt.close()
            report_lines.append(f"![Cluster Scatter Plot]({scatter_plot})")
            report_lines.append("*The scatter plot above shows how customers cluster based on their ratings and sentiment scores. The dashed lines indicate neutral sentiment (horizontal) and neutral rating (vertical) boundaries.*")
            generated_files.append(os.path.join(output_dir, scatter_plot))
            report_lines.append("")
        
        elif skip_clustering:
            report_lines.append("## Rating Distribution Analysis")
            report_lines.append("Due to limited variance in the data, traditional clustering was skipped. Here's a breakdown of ratings by sentiment:")
            report_lines.append("")
            rating_col = detect_rating_column(data)
            for sentiment in ['positive', 'negative', 'neutral']:
                sentiment_data_subset = data[data['sentiment'] == sentiment]
                if len(sentiment_data_subset) > 0:
                    low_count = (sentiment_data_subset[rating_col] <= 2).sum()
                    high_count = (sentiment_data_subset[rating_col] >= 4).sum()
                    total = len(sentiment_data_subset)
                    low_pct = (low_count / total) * 100 if total > 0 else 0
                    high_pct = (high_count / total) * 100 if total > 0 else 0
                    report_lines.append(f"**{sentiment.capitalize()} reviews**: {low_pct:.1f}% low ratings (1-2), {high_pct:.1f}% high ratings (4-5)")
            report_lines.append("")
        
        # Insights
        report_lines.append("## Key Business Insights")
        text_col = detect_text_column(data)
        rating_col = detect_rating_column(data)
        insights = []
        
        # Overall sentiment
        pos_pct = (data['sentiment'] == 'positive').mean() * 100
        neg_pct = (data['sentiment'] == 'negative').mean() * 100
        neu_pct = (data['sentiment'] == 'neutral').mean() * 100
        insights.append(f"The dataset shows {pos_pct:.1f}% positive, {neu_pct:.1f}% neutral, and {neg_pct:.1f}% negative sentiment across {len(data)} reviews.")
        
        if text_col:
            positive_texts = data[data['sentiment'] == 'positive'][text_col].dropna().astype(str).tolist()
            negative_texts = data[data['sentiment'] == 'negative'][text_col].dropna().astype(str).tolist()
            
            positive_keywords = get_top_keywords(positive_texts, 3)
            negative_keywords = get_top_keywords(negative_texts, 3)
            
            if positive_keywords and positive_keywords[0] != "insufficient data":
                insights.append(f"Customers expressing positive sentiment frequently mention: {', '.join(positive_keywords)}.")
            
            if negative_keywords and negative_keywords[0] != "insufficient data":
                insights.append(f"Negative reviews often highlight issues with: {', '.join(negative_keywords)}.")
            
            # Example reviews
            positive_examples = data[data['sentiment'] == 'positive'].nlargest(2, 'sentiment_score')[text_col].dropna().astype(str).tolist()
            negative_examples = data[data['sentiment'] == 'negative'].nsmallest(2, 'sentiment_score')[text_col].dropna().astype(str).tolist()
            
            if positive_examples:
                example = positive_examples[0][:200] + "..." if len(positive_examples[0]) > 200 else positive_examples[0]
                insights.append(f"Example positive feedback: \"{example}\".")
            
            if negative_examples:
                example = negative_examples[0][:200] + "..." if len(negative_examples[0]) > 200 else negative_examples[0]
                insights.append(f"Example negative feedback: \"{example}\".")
        
        # Cluster insights if applicable
        if 'cluster' in data.columns and not skip_clustering:
            for cluster_id in sorted(data['cluster'].unique()):
                cluster_data_subset = data[data['cluster'] == cluster_id]
                cluster_texts = cluster_data_subset[text_col].dropna().astype(str).tolist() if text_col else []
                cluster_keywords = get_top_keywords(cluster_texts, 3) if cluster_texts else []
                avg_rating = cluster_data_subset[rating_col].mean() if rating_col else 0
                avg_sentiment = cluster_data_subset['sentiment_score'].mean()
                if cluster_keywords and cluster_keywords[0] != "insufficient data":
                    insights.append(f"Cluster {cluster_id} (avg rating {avg_rating:.1f}, sentiment {avg_sentiment:.2f}) focuses on: {', '.join(cluster_keywords)}.")
                else:
                    insights.append(f"Cluster {cluster_id} has an average rating of {avg_rating:.1f} and sentiment score of {avg_sentiment:.2f}.")
        
        elif skip_clustering:
            insights.append("The data shows limited diversity in ratings and sentiment, suggesting a polarized customer base with mostly extreme opinions.")
        
        for insight in insights:
            report_lines.append(f"- {insight}")
        report_lines.append("")
        
        # Recommendations
        report_lines.append("## Recommendations")
        if pos_pct > 60:
            report_lines.append("- **Product Team**: Maintain current strengths and explore ways to convert neutral customers to positive.")
        elif neg_pct > 40:
            report_lines.append("- **Product Team**: Prioritize addressing the key pain points identified in negative reviews.")
        else:
            report_lines.append("- **Product Team**: Focus on features that differentiate from competitors to boost positive sentiment.")
        
        report_lines.append("- **Customer Service**: Reach out to negative sentiment customers with personalized support.")
        report_lines.append("- **Marketing**: Highlight positive aspects mentioned in reviews for targeted campaigns.")
        report_lines.append("- **Quality Assurance**: Monitor sentiment trends to catch issues early.")
        report_lines.append("")
        
        report_content = "\n".join(report_lines)
        
        report_file = f"analysis_report_{timestamp}.md"
        with open(os.path.join(output_dir, report_file), 'w') as f:
            f.write(report_content)
        
        generated_files.append(os.path.join(output_dir, report_file))
        
        # Generate PDF
        pdf_file = f"analysis_report_{timestamp}.pdf"
        pdf_path = os.path.join(output_dir, pdf_file)
        doc = SimpleDocTemplate(pdf_path, pagesize=letter)
        story = []
        styles = getSampleStyleSheet()
        story.append(Paragraph("AI Workflow Orchestrator MCP - Comprehensive Analysis Report", styles['Title']))
        story.append(Spacer(1, 12))
        story.append(Paragraph(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", styles['Normal']))
        story.append(Spacer(1, 12))
        story.append(Paragraph("Dataset Overview", styles['Heading2']))
        story.append(Paragraph(f"Total Records: {len(data)}", styles['Normal']))
        story.append(Paragraph(f"Features Analyzed: {len(data.columns)}", styles['Normal']))
        story.append(Paragraph(f"Data Completeness: {data.isnull().sum().sum()} missing values across all columns", styles['Normal']))
        story.append(Spacer(1, 12))
        if 'sentiment' in data.columns:
            story.append(Paragraph("Sentiment Analysis", styles['Heading2']))
            sentiment_data = json.loads(get_sentiment_summary(data))
            total_reviews = sum(sentiment_data.values())
            story.append(Paragraph(f"Analysis of {total_reviews} reviews reveals the following sentiment distribution:", styles['Normal']))
            for sentiment, count in sentiment_data.items():
                percentage = (count / total_reviews) * 100
                story.append(Paragraph(f"{sentiment.capitalize()}: {percentage:.1f}%", styles['Normal']))
            story.append(Spacer(1, 12))
            # Embed sentiment chart
            sentiment_chart_path = os.path.join(output_dir, sentiment_chart)
            if os.path.exists(sentiment_chart_path):
                story.append(Image(sentiment_chart_path, width=400, height=300))
                story.append(Spacer(1, 12))
        if 'cluster' in data.columns and not skip_clustering:
            story.append(Paragraph("Customer Segmentation Analysis", styles['Heading2']))
            cluster_data = json.loads(get_cluster_summary(data))
            story.append(Paragraph(f"Customers have been segmented into {len(cluster_data['cluster_sizes'])} distinct groups using K-Means clustering on rating and sentiment scores.", styles['Normal']))
            story.append(Spacer(1, 12))
            # Embed cluster pie chart
            cluster_pie_path = os.path.join(output_dir, cluster_pie)
            if os.path.exists(cluster_pie_path):
                story.append(Image(cluster_pie_path, width=400, height=300))
                story.append(Spacer(1, 12))
            # Embed scatter plot
            scatter_plot_path = os.path.join(output_dir, scatter_plot)
            if os.path.exists(scatter_plot_path):
                story.append(Image(scatter_plot_path, width=400, height=300))
                story.append(Spacer(1, 12))
        # Insights
        story.append(Paragraph("Key Business Insights", styles['Heading2']))
        insights_text = "\n".join([f"- {insight}" for insight in insights])
        story.append(Paragraph(insights_text, styles['Normal']))
        story.append(Spacer(1, 12))
        doc.build(story)
        generated_files.append(pdf_path)
        
        logger.info(f"Generated report and visualizations in {output_dir}")
        return json.dumps({"success": True, "generated_files": generated_files, "output_dir": output_dir})
    except Exception as e:
        error_msg = f"Error generating report: {str(e)}"
        logger.error(error_msg)
        return json.dumps({"success": False, "error": error_msg})