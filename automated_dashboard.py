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

def automated_dashboard(df: pd.DataFrame):
    """Generate automated insights dashboard"""
    
    st.markdown("## 🎯 Automated Insights Dashboard")
    
    # Key Metrics
    st.markdown("### 📊 Key Metrics")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric("📈 Total Rows", len(df))
    with col2:
        st.metric("📌 Columns", len(df.columns))
    with col3:
        st.metric("📊 Numeric", len(df.select_dtypes(include=['number']).columns))
    with col4:
        st.metric("🔡 Categorical", len(df.select_dtypes(include=['object']).columns))
    with col5:
        st.metric("💾 Size (MB)", f"{df.memory_usage(deep=True).sum() / 1024**2:.2f}")
    
    st.divider()
    
    # Data Quality Summary
    st.markdown("### 🔍 Data Quality Summary")
    quality = quality_report(df)
    missing_pct = (df.isnull().sum().sum() / (len(df) * len(df.columns))) * 100
    dup_pct = (df.duplicated().sum() / len(df)) * 100

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("❌ Missing Data %", f"{missing_pct:.1f}%")
    with col2:
        st.metric("♻️ Duplicates %", f"{dup_pct:.1f}%")
    with col3:
        st.metric("💾 Memory (MB)", f"{quality['memory_usage_mb']:.2f}")
    with col4:
        st.metric("📊 Data Types", len(set(df.dtypes)))
    
    st.divider()

    # Automated Visualizations
    st.markdown("### 🎨 Automated Visualizations")
    st.info("Visualizing key patterns detected in your data")
    
    num_cols = df.select_dtypes(include=['number']).columns.tolist()
    cat_cols = df.select_dtypes(include=['object']).columns.tolist()
    
    v_col1, v_col2 = st.columns(2)
    
    with v_col1:
        # 1. Distribution of top numeric column
        if num_cols:
            st.markdown(f"**Distribution of {num_cols[0]}**")
            generate_chart(df, {'type': 'hist', 'x': num_cols[0]})
            
        # 3. Box plot if both exist
        if cat_cols and num_cols:
            st.markdown(f"**{num_cols[0]} by {cat_cols[0]}**")
            generate_chart(df, {'type': 'box', 'x': cat_cols[0], 'y': num_cols[0]})

    with v_col2:
        # 2. Composition of top categorical column
        if cat_cols:
            st.markdown(f"**Composition of {cat_cols[0]}**")
            generate_chart(df, {'type': 'pie', 'x': cat_cols[0]})
            
        # 4. Correlation Heatmap snippet or Scatter
        if len(num_cols) >= 2:
            st.markdown(f"**{num_cols[1]} vs {num_cols[0]}**")
            generate_chart(df, {'type': 'scatter', 'x': num_cols[0], 'y': num_cols[1]})

    st.divider()
    
    # Anomalies
    st.markdown("### 🔴 Anomalies Detected")
    anomalies = detect_anomalies(df)
    
    if any(anomalies.values()):
        anomaly_count = sum(1 for col, is_anomaly in anomalies.items() if is_anomaly)
        st.error(f"⚠️ {anomaly_count} columns have anomalies")
        for col, is_anomaly in anomalies.items():
            if is_anomaly:
                st.write(f"• {col}")
    else:
        st.success("✅ No anomalies detected")
    
    st.divider()
    
    # Top Correlations
    st.markdown("### 🔗 Top Correlations")
    corr = calculate_correlations(df)
    
    if corr is not None:
        significant = get_significant_correlations(df, threshold=0.7)
        if significant:
            st.success(f"Found {len(significant)} strong correlations")
            for item in significant[:5]:
                st.info(f"**{item['var1']}** ↔ **{item['var2']}**: {item['correlation']:.3f}")
        else:
            st.info("No strong correlations detected")
    
    st.divider()
    
    # Recommendations
    st.markdown("### 💡 Recommendations")
    recommendations = []
    
    if missing_pct > 10:
        recommendations.append("⚠️ High missing data percentage - consider imputation or deletion")
    if dup_pct > 5:
        recommendations.append("⚠️ High duplication rate - check for data quality issues")
    if len(detailed_outliers(df)) > 0:
        recommendations.append("📍 Remove or handle outliers before modeling")
    
    if recommendations:
        for rec in recommendations:
            st.info(rec)
    else:
        st.success("✅ Dataset looks good for analysis!")
