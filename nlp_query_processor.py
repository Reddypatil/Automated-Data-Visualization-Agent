import pandas as pd
import streamlit as st
from ai_insights import generate_ai_insights
from eda_analysis import perform_eda
from anomaly_detection import detect_anomalies
from correlation_analysis import get_significant_correlations

def parse_nlp_query(query: str, df: pd.DataFrame) -> str:
    """Process natural language queries about data"""
    
    query_lower = query.lower()
    
    if "summary" in query_lower or "overview" in query_lower:
        eda = perform_eda(df)
        return f"Dataset Summary: {len(df)} rows, {len(df.columns)} columns. Key stats: {eda}"
    
    elif "correlation" in query_lower or "correlated" in query_lower:
        corr = get_significant_correlations(df, threshold=0.7)
        if corr:
            return f"Strong correlations found: {corr}"
        return "No strong correlations detected"
    
    elif "missing" in query_lower or "null" in query_lower:
        missing = df.isnull().sum()
        missing = missing[missing > 0]
        if missing.empty:
            return "No missing values detected"
        return f"Missing values: {missing.to_dict()}"
    
    elif "anomal" in query_lower or "outlier" in query_lower:
        anomalies = detect_anomalies(df)
        return f"Anomalies detected: {anomalies}"
    
    elif "distribution" in query_lower or "histogram" in query_lower:
        numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
        if numeric_cols:
            return f"Found {len(numeric_cols)} numeric columns for distribution analysis: {numeric_cols[:5]}"
        return "No numeric columns found"
    
    elif "trend" in query_lower or "increase" in query_lower:
        return "Perform time series analysis to detect trends"
    
    elif "group" in query_lower or "by" in query_lower:
        categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
        if categorical_cols:
            return f"Available columns for grouping: {categorical_cols}"
        return "No categorical columns found"
    
    elif "compare" in query_lower or "difference" in query_lower:
        return "Use hypothesis testing tab for statistical comparisons"
    
    else:
        return "Query not recognized. Try asking about: summary, correlation, missing values, anomalies, distribution, trends, grouping, or comparisons"

def nlp_query_ui(df: pd.DataFrame):
    """Main NLP query UI"""
    st.markdown("## 💬 Natural Language Queries")
    st.info("Ask questions about your data in natural language!")
    
    query = st.text_area(
        "Ask a question about your data:",
        placeholder="e.g., 'Show me correlations', 'Find anomalies', 'What columns are missing values?'",
        height=100
    )
    
    if st.button("🔍 Analyze"):
        if query.strip():
            response = parse_nlp_query(query, df)
            st.success(response)
        else:
            st.warning("Please enter a query")
    
    # Suggested queries
    st.markdown("### 💡 Try these queries:")
    suggestions = [
        "Show me a summary of the data",
        "What correlations exist?",
        "Find missing values",
        "Detect anomalies",
        "Show distribution of numeric columns",
        "Group by categorical columns",
        "Detect trends in the data"
    ]
    
    for suggestion in suggestions:
        if st.button(suggestion):
            response = parse_nlp_query(suggestion, df)
            st.info(response)
