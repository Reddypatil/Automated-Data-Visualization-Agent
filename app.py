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

# Page configuration with custom theme
st.set_page_config(
    page_title="DataWizard - AI Analytics",
    page_icon="🧙‍♂️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for beautiful design
st.markdown("""
<style>
    /* Main container */
    .main {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    
    /* Header styling */
    .header-title {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 40px 20px;
        border-radius: 15px;
        text-align: center;
        box-shadow: 0 10px 40px rgba(102, 126, 234, 0.4);
        margin-bottom: 30px;
    }
    
    .header-title h1 {
        font-size: 3em;
        font-weight: 800;
        margin: 0;
        text-shadow: 0 2px 10px rgba(0,0,0,0.2);
    }
    
    .header-title p {
        font-size: 1.1em;
        margin: 10px 0 0 0;
        opacity: 0.95;
    }
    
    /* Feature cards */
    .feature-card {
        background: white;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
        border-top: 4px solid #667eea;
        margin-bottom: 15px;
        transition: all 0.3s ease;
    }
    
    .feature-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.12);
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 12px 30px;
        font-weight: 600;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.6);
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background-color: rgba(255, 255, 255, 0.9);
        padding: 15px;
        border-radius: 12px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
    }
    
    .stTabs [data-baseweb="tab"] {
        color: #667eea;
        font-weight: 600;
        border-radius: 8px;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
    
    /* Metric cards */
    .stMetric {
        background: white;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
        border-left: 4px solid #667eea;
    }
    
    /* Alert boxes */
    .stSuccess {
        background-color: rgba(16, 185, 129, 0.1);
        border-left: 4px solid #10b981;
    }
    
    .stInfo {
        background-color: rgba(102, 126, 234, 0.1);
        border-left: 4px solid #667eea;
    }
    
    .stWarning {
        background-color: rgba(245, 158, 11, 0.1);
        border-left: 4px solid #f59e0b;
    }
    
    /* Dataframe styling */
    .stDataFrame {
        border-radius: 8px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
    }
    
    /* File uploader */
    .stFileUploader {
        border: 2px dashed #667eea;
        border-radius: 12px;
        padding: 30px;
        background-color: rgba(102, 126, 234, 0.05);
    }
    
    /* Divider */
    hr {
        border: none;
        height: 2px;
        background: linear-gradient(90deg, transparent, #667eea, transparent);
        margin: 30px 0;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="header-title">
    <h1>🧙‍♂️ DataWizard</h1>
    <p>AI-Powered Data Analytics & Visualization Platform</p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
### 📊 Transform Your Data Into Intelligence
Upload your dataset and unlock powerful insights with AI-driven analysis, beautiful visualizations, and predictive intelligence!
""")

# Sidebar with feature overview
with st.sidebar:
    st.title("🎯 Quick Guide")
    st.markdown("""
    ### Features:
    - 📊 **EDA** - Exploratory data analysis
    - 🔍 **Quality** - Data quality metrics
    - 🎨 **Visualizations** - AI-selected charts
    - 📈 **Analytics** - Advanced statistics
    - 🤖 **AI Insights** - Smart recommendations
    - ⚡ **Predictions** - ML models
    - 📄 **Reports** - Full analysis export
    """)
    st.divider()
    st.markdown("**Tips:**")
    st.markdown("• Start with small datasets")
    st.markdown("• Check data quality first")
    st.markdown("• Use AI insights for understanding")

# File uploader
st.markdown("### 📁 Upload Your Data")
uploaded_file = st.file_uploader("Drag and drop or browse", type=["csv","xlsx","json"])

if uploaded_file:
    df = preprocess_data(load_data(uploaded_file))
    st.success(f"✅ Loaded: {len(df)} rows × {len(df.columns)} columns")
    
    # Data preview
    with st.expander("📋 View Data Preview", expanded=True):
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("📊 Rows", len(df))
        with col2:
            st.metric("📌 Columns", len(df.columns))
        with col3:
            st.metric("🔢 Numeric", len(df.select_dtypes(include='number').columns))
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
        st.markdown("## Exploratory Data Analysis")
        col1, col2, col3 = st.columns(3)
        eda = perform_eda(df)
        with col1:
            st.metric("📊 Total Rows", eda['rows'])
        with col2:
            st.metric("📌 Total Columns", eda['cols'])
        with col3:
            st.metric("🔢 Numeric Cols", len(df.select_dtypes(include='number').columns))
        
        st.markdown("### Data Summary")
        st.json(eda)
        
        st.markdown("### Data Profiling")
        profile = profile_data(df)
        st.json(profile)
    
    # Tab 2: Data Quality
    with tab2:
        st.markdown("## 📊 Data Quality Report")
        quality = quality_report(df)
        st.info(data_quality_summary(df))
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("⚠️ Missing Values", sum([col['missing_count'] for col in quality['columns'].values()]))
        with col2:
            st.metric("♻️ Duplicate Rows", quality['duplicates']['count'])
        with col3:
            st.metric("💾 Memory (MB)", quality['memory_usage_mb'])
        
        st.markdown("### Column Details")
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
        st.markdown("## 🎨 AI-Selected Visualizations")
        st.info("🤖 The AI has chosen the best visualizations for your data type and structure")
        
        for i, chart in enumerate(ai_chart_selection(df)):
            col1, col2 = st.columns([1, 4])
            with col1:
                if '📊' in chart["reason"]:
                    st.markdown("📊")
                elif '📈' in chart["reason"]:
                    st.markdown("📈")
                elif '🔗' in chart["reason"]:
                    st.markdown("🔗")
                elif '📦' in chart["reason"]:
                    st.markdown("📦")
            with col2:
                st.markdown(f"**{chart['reason'].split(':')[1].split('.')[0]}**")
            
            st.info(chart["reason"])
            generate_chart(df, chart)
            st.divider()
        
        # Correlation Matrix
        st.markdown("## 🔗 Correlation Analysis")
        corr = calculate_correlations(df)
        if corr is not None:
            plot_correlation_heatmap(corr)
            significant = get_significant_correlations(df, threshold=0.7)
            if significant:
                st.success("**Strong Correlations Found:**")
                for item in significant:
                    st.markdown(f"• **{item['var1']}** ↔ **{item['var2']}**: {item['correlation']} ({item['interpretation']})")
        else:
            st.warning("No numeric columns for correlation analysis")
    
    # Tab 4: Advanced Analytics
    with tab4:
        st.markdown("## 📊 Statistical Analysis")
        
        # Anomaly Detection
        st.markdown("### 🔴 Anomaly Detection (Z-score > 3)")
        anomalies = detect_anomalies(df)
        if any(anomalies.values()):
            st.json(anomalies)
        else:
            st.success("✅ No anomalies detected!")
        
        # Detailed Outliers
        st.markdown("### 📍 Outlier Analysis")
        outliers = detailed_outliers(df)
        if outliers:
            for col, info in outliers.items():
                with st.expander(f"{col} - {info['count']} outliers ({info['percentage']}%)"):
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Mean", info['mean'])
                    with col2:
                        st.metric("Std Dev", info['std'])
                    with col3:
                        st.metric("Threshold", info['threshold'])
                    st.write(f"**Sample outlier values:** {info['outlier_values']}")
        else:
            st.success("✅ No outliers detected!")
        
        # Statistical Tests
        st.markdown("### 🧪 Correlation Statistical Tests")
        tests = statistical_tests(df)
        if tests:
            tests_df = pd.DataFrame(tests)
            st.dataframe(tests_df, use_container_width=True)
        
        # Time Series Analysis
        st.markdown("### ⏰ Time Series Analysis")
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
                        st.metric("📅 Date Range", analysis['date_range'])
                    with col2:
                        st.metric("📊 Days", analysis['total_days'])
                    with col3:
                        st.metric("📈 Mean", analysis['value_mean'])
                    with col4:
                        st.metric("📉 Trend", analysis['trend'])
                    plot_time_series(df_ts, date_col, value_col)
        else:
            st.info("No datetime columns detected for time series analysis")
    
    # Tab 5: AI Insights
    with tab5:
        st.markdown("## 🤖 AI-Powered Insights")
        st.markdown("Get AI-generated recommendations and insights about your data")
        if st.button("✨ Generate AI Insights"):
            with st.spinner("🔮 Analyzing your data..."):
                eda = perform_eda(df)
                anomalies = detect_anomalies(df)
                corr = calculate_correlations(df)
                significant = get_significant_correlations(df, 0.7) if corr is not None else []
                insights = generate_ai_insights(df, eda, anomalies, significant)
                st.success(insights)
    
    # Tab 6: Predictions
    with tab6:
        st.markdown("## ⚡ Predictive Analytics")
        num_cols = df.select_dtypes(include='number').columns.tolist()
        
        if len(num_cols) >= 2:
            target = st.selectbox("Select Target Column", num_cols)
            model_type = st.radio("Model Type", ["📊 Regression", "📈 Classification"], horizontal=True)
            
            if st.button("🚀 Train Model"):
                with st.spinner("Training model..."):
                    if "Regression" in model_type:
                        result = simple_regression(df, target)
                    else:
                        result = classification_model(df, target)
                    
                    if result:
                        st.success("✅ Model trained successfully!")
                        st.json(result)
                    else:
                        st.error("Could not train model with this data")
        else:
            st.warning("Need at least 2 numeric columns for predictions")
    
    # Tab 7: Report
    with tab7:
        st.markdown("## 📄 Comprehensive Report")
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
    st.markdown("""
    <div style="text-align: center; padding: 50px;">
        <h2>👆 Get Started</h2>
        <p style="font-size: 1.2em; color: #667eea;">Upload a CSV, Excel, or JSON file to unlock powerful data analysis</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.divider()
    
    # Feature cards
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
        <h3>📊 Smart Visualizations</h3>
        <p>AI-selected charts that best represent your data</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
        <h3>🤖 AI Insights</h3>
        <p>Get intelligent recommendations powered by ChatGPT</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="feature-card">
        <h3>⚡ Predictions</h3>
        <p>Train ML models and make predictions</p>
        </div>
        """, unsafe_allow_html=True)
