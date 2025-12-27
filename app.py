import streamlit as st
import pandas as pd
from data_ingestion import load_data
from data_preprocessing import preprocess_data
from eda_analysis import perform_eda
from ai_chart_selector import ai_chart_selection
from visualization_generator import generate_chart, plot_correlation_heatmap, plot_time_series
from insight_generator import generate_insights
from report_generator import generate_report
from data_profiling import profile_data
from anomaly_detection import detect_anomalies
from correlation_analysis import calculate_correlations, get_significant_correlations, statistical_tests
from data_quality import quality_report, data_quality_summary
from outlier_analysis import detailed_outliers
from time_series_analysis import detect_datetime_columns, time_series_analysis
from predictive_models import simple_regression, classification_model
from ai_insights import generate_ai_insights

st.set_page_config(page_title="Advanced Automated Data Visualization Agent", layout="wide")
st.title("🎯 Advanced Automated Data Visualization Agent")

st.markdown("Upload your dataset and get AI-powered analysis including visualizations, insights, and predictions!")

uploaded_file = st.file_uploader("📁 Upload Dataset", type=["csv","xlsx","json"])

if uploaded_file:
    df = preprocess_data(load_data(uploaded_file))
    st.success(f"✅ Dataset loaded successfully! ({len(df)} rows, {len(df.columns)} columns)")
    
    with st.expander("📋 View Data Preview", expanded=True):
        st.dataframe(df.head(10), use_container_width=True)
    
    st.divider()
    
    # Tabs for different sections
    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
        "📊 EDA", 
        "🔍 Quality", 
        "🎨 Visualizations", 
        "📈 Analytics", 
        "🤖 AI Insights", 
        "⚡ Predictions",
        "📄 Report"
    ])
    
    # Tab 1: EDA
    with tab1:
        st.subheader("Exploratory Data Analysis")
        col1, col2, col3 = st.columns(3)
        eda = perform_eda(df)
        with col1:
            st.metric("Total Rows", eda['rows'])
        with col2:
            st.metric("Total Columns", eda['cols'])
        with col3:
            st.metric("Numeric Cols", len(df.select_dtypes(include='number').columns))
        st.json(eda)
        
        st.subheader("Data Profiling")
        profile = profile_data(df)
        st.json(profile)
    
    # Tab 2: Data Quality
    with tab2:
        st.subheader("📊 Data Quality Report")
        quality = quality_report(df)
        st.info(data_quality_summary(df))
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Missing Values", sum([col['missing_count'] for col in quality['columns'].values()]))
        with col2:
            st.metric("Duplicate Rows", quality['duplicates']['count'])
        with col3:
            st.metric("Memory Usage (MB)", quality['memory_usage_mb'])
        
        st.subheader("Column Details")
        quality_df = pd.DataFrame([
            {
                'Column': col_name,
                'Type': col_info['dtype'],
                'Missing %': col_info['missing_percentage'],
                'Unique': col_info['unique_values']
            }
            for col_name, col_info in quality['columns'].items()
        ])
        st.dataframe(quality_df, use_container_width=True)
    
    # Tab 3: Visualizations
    with tab3:
        st.subheader("🎨 AI-Selected Visualizations")
        st.write("The AI has selected the most relevant visualizations for your data:")
        
        for chart in ai_chart_selection(df):
            st.info(chart["reason"])
            generate_chart(df, chart)
            st.divider()
        
        # Correlation Matrix
        st.subheader("🔗 Correlation Analysis")
        corr = calculate_correlations(df)
        if corr is not None:
            plot_correlation_heatmap(corr)
            significant = get_significant_correlations(df, threshold=0.7)
            if significant:
                st.write("**Strong Correlations Found:**")
                for item in significant:
                    st.write(f"• {item['var1']} ↔ {item['var2']}: {item['correlation']} ({item['interpretation']})")
        else:
            st.warning("No numeric columns for correlation analysis")
    
    # Tab 4: Advanced Analytics
    with tab4:
        st.subheader("📊 Statistical Analysis")
        
        # Anomaly Detection
        st.write("**🔴 Anomaly Detection (Z-score > 3)**")
        anomalies = detect_anomalies(df)
        if any(anomalies.values()):
            st.json(anomalies)
        else:
            st.success("No anomalies detected!")
        
        # Detailed Outliers
        st.write("**📍 Outlier Analysis**")
        outliers = detailed_outliers(df)
        if outliers:
            for col, info in outliers.items():
                with st.expander(f"{col} ({info['count']} outliers)"):
                    st.write(f"Percentage: {info['percentage']}%")
                    st.write(f"Mean: {info['mean']}, Std Dev: {info['std']}")
                    st.write(f"Sample outlier values: {info['outlier_values']}")
        else:
            st.success("No outliers detected!")
        
        # Statistical Tests
        st.write("**🧪 Correlation Statistical Tests**")
        tests = statistical_tests(df)
        if tests:
            tests_df = pd.DataFrame(tests)
            st.dataframe(tests_df, use_container_width=True)
        
        # Time Series Analysis
        st.write("**⏰ Time Series Analysis**")
        datetime_cols = detect_datetime_columns(df)
        if datetime_cols:
            date_col = st.selectbox("Select Date Column", datetime_cols)
            num_cols = df.select_dtypes(include='number').columns.tolist()
            if num_cols:
                value_col = st.selectbox("Select Value Column", num_cols)
                analysis, df_ts = time_series_analysis(df, date_col, value_col)
                if analysis:
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric("Date Range", analysis['date_range'])
                    with col2:
                        st.metric("Total Days", analysis['total_days'])
                    with col3:
                        st.metric("Mean Value", analysis['value_mean'])
                    with col4:
                        st.metric("Trend", analysis['trend'])
                    plot_time_series(df_ts, date_col, value_col)
        else:
            st.info("No datetime columns detected for time series analysis")
    
    # Tab 5: AI Insights
    with tab5:
        st.subheader("🤖 AI-Powered Insights")
        if st.button("Generate AI Insights"):
            with st.spinner("Analyzing your data..."):
                eda = perform_eda(df)
                anomalies = detect_anomalies(df)
                corr = calculate_correlations(df)
                significant = get_significant_correlations(df, 0.7) if corr is not None else []
                insights = generate_ai_insights(df, eda, anomalies, significant)
                st.success(insights)
    
    # Tab 6: Predictions
    with tab6:
        st.subheader("⚡ Predictive Analytics")
        num_cols = df.select_dtypes(include='number').columns.tolist()
        
        if len(num_cols) >= 2:
            target = st.selectbox("Select Target Column", num_cols)
            model_type = st.radio("Model Type", ["Regression", "Classification"])
            
            if st.button("Train Model"):
                with st.spinner("Training model..."):
                    if model_type == "Regression":
                        result = simple_regression(df, target)
                    else:
                        result = classification_model(df, target)
                    
                    if result:
                        st.success("Model trained successfully!")
                        st.json(result)
                    else:
                        st.error("Could not train model with this data")
        else:
            st.warning("Need at least 2 numeric columns for predictions")
    
    # Tab 7: Report
    with tab7:
        st.subheader("📄 Comprehensive Report")
        eda = perform_eda(df)
        insights = list(generate_insights(df))
        report_text = generate_report(eda, insights)
        st.text(report_text)
        
        if st.button("📥 Download Report"):
            st.download_button(
                label="Download as Text",
                data=report_text,
                file_name="analysis_report.txt",
                mime="text/plain"
            )

else:
    st.info("👆 Upload a CSV, Excel, or JSON file to get started!")
