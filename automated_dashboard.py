import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
from eda_analysis import perform_eda
from anomaly_detection import detect_anomalies
from correlation_analysis import calculate_correlations, get_significant_correlations
from outlier_analysis import detailed_outliers
from data_quality import quality_report
from visualization_generator import generate_chart
from ai_insights import generate_ai_insights

def automated_dashboard(df: pd.DataFrame):
    """Generate a comprehensive automated insights dashboard for the whole dataset"""
    
    st.markdown("## Whole Dataset Intelligence Report")
    
    # --- 1. Executive Summary ---
    st.markdown("### Executive Summary")
    with st.container():
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Dataset Vitality", f"{len(df)} rows")
        with col2:
            st.metric("Features", f"{len(df.columns)} columns")
        with col3:
            missing_pct = (df.isnull().sum().sum() / (len(df) * len(df.columns))) * 100
            st.metric("Data Health", f"{100 - missing_pct:.1f}% Score")

    # --- 2. AI Strategic Insights ---
    st.markdown("### AI-Generated Strategic Insights")
    if st.button("Refresh AI Brain"):
        with st.spinner("Syncing with AI..."):
            eda = perform_eda(df)
            anomalies = detect_anomalies(df)
            corr = calculate_correlations(df)
            significant = get_significant_correlations(df, 0.7) if corr is not None else []
            insights = generate_ai_insights(df, eda, anomalies, significant)
            st.success(insights)
    else:
        st.info("Click the button above to generate a deep-dive AI analysis of your entire dataset.")

    st.divider()

    # --- 3. Automated Visual Storytelling ---
    st.markdown("### Visual Storytelling")
    num_cols = df.select_dtypes(include=['number']).columns.tolist()
    cat_cols = df.select_dtypes(include=['object']).columns.tolist()
    
    v_col1, v_col2 = st.columns(2)
    with v_col1:
        if num_cols:
            st.markdown(f"**Main Distribution: {num_cols[0]}**")
            generate_chart(df, {'type': 'hist', 'x': num_cols[0]})
        if cat_cols and num_cols:
            st.markdown(f"**Grouped Variance: {num_cols[0]} by {cat_cols[0]}**")
            generate_chart(df, {'type': 'box', 'x': cat_cols[0], 'y': num_cols[0]})
    with v_col2:
        if cat_cols:
            st.markdown(f"**Composition: {cat_cols[0]}**")
            generate_chart(df, {'type': 'pie', 'x': cat_cols[0]})
        if len(num_cols) >= 2:
            st.markdown(f"**Key Relationship: {num_cols[1]} vs {num_cols[0]}**")
            generate_chart(df, {'type': 'scatter', 'x': num_cols[0], 'y': num_cols[1]})

    st.divider()

    # --- 4. Deep-Dive Metrics ---
    st.markdown("### Deep-Dive Statistics")
    d_col1, d_col2 = st.columns(2)
    
    with d_col1:
        st.markdown("**Top Relationships (Strongest Links)**")
        corr = calculate_correlations(df)
        if corr is not None:
            significant = get_significant_correlations(df, threshold=0.7)
            if significant:
                for item in significant[:3]:
                    st.success(f"**{item['var1']}** ↔ **{item['var2']}**: {item['correlation']:.3f}")
            else:
                st.write("No extreme correlations found.")
    
    with d_col2:
        st.markdown("**Data Red Flags (Anomalies & Outliers)**")
        anomalies = detect_anomalies(df)
        anomaly_count = sum(1 for col, is_anomaly in anomalies.items() if is_anomaly)
        if anomaly_count > 0:
            st.error(f"{anomaly_count} potential data anomalies detected")
        else:
            st.success("Statistical distributions look normal")

    # --- 5. Data Quality & Readiness ---
    st.markdown("### Data Quality & Readiness")
    quality = quality_report(df)
    dup_pct = (df.duplicated().sum() / len(df)) * 100
    
    col_q1, col_q2, col_q3 = st.columns(3)
    col_q1.metric("Duplicates", f"{dup_pct:.1f}%")
    col_q2.metric("Footprint", f"{quality['memory_usage_mb']:.2f} MB")
    col_q3.metric("Ready for ML", "Yes" if missing_pct < 20 else "Partial")

    # --- 6. Automated Roadmap ---
    st.markdown("### Recommended Roadmap")
    recommendations = []
    if missing_pct > 10:
        recommendations.append("Data Imputation: High missing values detected. Consider filling gaps before analysis.")
    if dup_pct > 5:
        recommendations.append("Deduplication: Clean duplicate records to avoid biased results.")
    if anomaly_count > 0:
        recommendations.append("Manual Review: Examine red-flagged columns for sensor errors or fraud.")
    if not recommendations:
        recommendations.append("Full Steam Ahead: Data is pristine. Ready for advanced predictive modeling.")
    
    for rec in recommendations:
        st.info(rec)
