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
from data_transformation import data_transformation_ui
from clustering_analysis import clustering_ui
from hypothesis_testing import hypothesis_testing_ui
from feature_engineering import feature_engineering_ui
from export_functionality import export_functionality_ui
from pdf_report_generator import pdf_report_ui
from model_explainability import model_explainability_ui
from nlp_query_processor import nlp_query_ui
from comparative_analysis import comparative_analysis_ui
from data_sampling import data_sampling_ui
from automated_dashboard import automated_dashboard
from dark_mode import toggle_dark_mode
from collaborative_features import collaborative_features_ui

st.set_page_config(
    page_title="DataWizard Pro - Advanced Analytics",
    page_icon="🧙‍♂️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply theme
st.markdown("""
<style>
    .main { background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); }
    .header-title {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white; padding: 40px 20px; border-radius: 15px;
        text-align: center; box-shadow: 0 10px 40px rgba(102, 126, 234, 0.4);
        margin-bottom: 30px;
    }
    .header-title h1 { font-size: 3em; font-weight: 800; margin: 0; text-shadow: 0 2px 10px rgba(0,0,0,0.2); }
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white; border: none; border-radius: 8px; padding: 12px 30px;
        font-weight: 600; box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    }
    .stButton > button:hover { transform: translateY(-2px); box-shadow: 0 8px 25px rgba(102, 126, 234, 0.6); }
    .stTabs [data-baseweb="tab-list"] { gap: 10px; background-color: rgba(255, 255, 255, 0.9);
        padding: 15px; border-radius: 12px; box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08); }
    .stTabs [aria-selected="true"] { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; }
    .stMetric { background: white; padding: 20px; border-radius: 12px; box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
        border-left: 4px solid #667eea; }
</style>
""", unsafe_allow_html=True)

# Toggle dark mode
with st.sidebar:
    toggle_dark_mode()

# Header
st.markdown("""
<div class="header-title">
    <h1>🧙‍♂️ DataWizard Pro</h1>
    <p>Complete AI-Powered Analytics & Intelligence Platform</p>
</div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.title("🎯 Navigation")
    st.markdown("""
    **Core Analytics:**
    - 📊 EDA
    - 🔍 Quality
    - 🎨 Visualizations
    - 📈 Advanced Analytics
    
    **AI & ML:**
    - 🤖 AI Insights
    - ⚡ Predictions
    - 🎯 Clustering
    - 🔍 Explainability
    
    **Data Tools:**
    - 🔧 Transformation
    - 🧪 Hypothesis Testing
    - 🔧 Feature Engineering
    - 📊 Sampling
    
    **Advanced:**
    - 💬 NLP Queries
    - 🔄 Compare Datasets
    - 👥 Collaboration
    - 📥 Export/PDF
    """)

# File upload
st.markdown("### 📁 Upload Your Data")
uploaded_file = st.file_uploader("Select CSV, Excel, or JSON", type=["csv", "xlsx", "json"])

if uploaded_file:
    df = preprocess_data(load_data(uploaded_file))
    st.success(f"✅ Loaded: {len(df)} rows × {len(df.columns)} columns")
    
    # Quick preview
    with st.expander("📋 Data Preview", expanded=True):
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("📊 Rows", len(df))
        with col2:
            st.metric("📌 Columns", len(df.columns))
        with col3:
            st.metric("🔢 Numeric", len(df.select_dtypes(include='number').columns))
        st.dataframe(df.head(10), use_container_width=True)
    
    st.divider()
    
    # Main tabs
    tabs = st.tabs([
        "📊 EDA", "🔍 Quality", "🎨 Visualizations", "📈 Analytics",
        "🤖 AI Insights", "⚡ Predictions", "🔄 Clustering", "🧪 Testing",
        "🔧 Transform", "🔧 Features", "📍 Explainability", "💬 NLP",
        "🔄 Compare", "📊 Sampling", "⭐ Dashboard", "👥 Collab", "📥 Export"
    ])
    
    # Tab 1: EDA
    with tabs[0]:
        st.markdown("## 📊 Exploratory Data Analysis")
        col1, col2, col3 = st.columns(3)
        eda = perform_eda(df)
        with col1:
            st.metric("Total Rows", eda['rows'])
        with col2:
            st.metric("Total Columns", eda['cols'])
        with col3:
            st.metric("Numeric Cols", len(df.select_dtypes(include='number').columns))
        st.json(eda)
        
        st.markdown("### Data Profiling")
        profile = profile_data(df)
        st.json(profile)
    
    # Tab 2: Quality
    with tabs[1]:
        st.markdown("## 🔍 Data Quality Report")
        quality = quality_report(df)
        st.info(data_quality_summary(df))
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("⚠️ Missing", sum([col['missing_count'] for col in quality['columns'].values()]))
        with col2:
            st.metric("♻️ Duplicates", quality['duplicates']['count'])
        with col3:
            st.metric("💾 Memory (MB)", quality['memory_usage_mb'])
        
        quality_df = pd.DataFrame([
            {'Column': col_name, 'Type': col_info['dtype'], 'Missing %': col_info['missing_percentage'], 'Unique': col_info['unique_values']}
            for col_name, col_info in quality['columns'].items()
        ])
        st.dataframe(quality_df, use_container_width=True)
    
    # Tab 3: Visualizations
    with tabs[2]:
        st.markdown("## 🎨 AI-Selected Visualizations")
        st.info("🤖 AI-chosen visualizations for your data")
        
        for chart in ai_chart_selection(df):
            st.info(chart["reason"])
            generate_chart(df, chart)
            st.divider()
        
        st.markdown("## 🔗 Correlation Heatmap")
        corr = calculate_correlations(df)
        if corr is not None:
            plot_correlation_heatmap(corr)
            significant = get_significant_correlations(df, threshold=0.7)
            if significant:
                st.success("**Strong Correlations:**")
                for item in significant:
                    st.markdown(f"• **{item['var1']}** ↔ **{item['var2']}**: {item['correlation']}")
    
    # Tab 4: Advanced Analytics
    with tabs[3]:
        st.markdown("## 📊 Statistical Analysis")
        
        st.markdown("### 🔴 Anomaly Detection")
        anomalies = detect_anomalies(df)
        if any(anomalies.values()):
            st.json(anomalies)
        else:
            st.success("✅ No anomalies detected!")
        
        st.markdown("### 📍 Outlier Analysis")
        outliers = detailed_outliers(df)
        if outliers:
            for col, info in outliers.items():
                with st.expander(f"{col} - {info['count']} outliers"):
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Mean", info['mean'])
                    with col2:
                        st.metric("Std Dev", info['std'])
                    with col3:
                        st.metric("Threshold", info['threshold'])
        else:
            st.success("✅ No outliers detected!")
        
        st.markdown("### 🧪 Statistical Tests")
        tests = statistical_tests(df)
        if tests:
            st.dataframe(pd.DataFrame(tests), use_container_width=True)
        
        st.markdown("### ⏰ Time Series Analysis")
        datetime_cols = detect_datetime_columns(df)
        if datetime_cols:
            date_col = st.selectbox("Date Column", datetime_cols)
            num_cols = df.select_dtypes(include='number').columns.tolist()
            if num_cols:
                value_col = st.selectbox("Value Column", num_cols)
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
    
    # Tab 5: AI Insights
    with tabs[4]:
        st.markdown("## 🤖 AI-Powered Insights")
        if st.button("✨ Generate AI Insights"):
            with st.spinner("🔮 Analyzing..."):
                eda = perform_eda(df)
                anomalies = detect_anomalies(df)
                corr = calculate_correlations(df)
                significant = get_significant_correlations(df, 0.7) if corr is not None else []
                insights = generate_ai_insights(df, eda, anomalies, significant)
                st.success(insights)
    
    # Tab 6: Predictions
    with tabs[5]:
        st.markdown("## ⚡ Predictive Analytics")
        num_cols = df.select_dtypes(include='number').columns.tolist()
        if len(num_cols) >= 2:
            target = st.selectbox("Target Column", num_cols)
            model_type = st.radio("Model Type", ["📊 Regression", "📈 Classification"], horizontal=True)
            if st.button("🚀 Train Model"):
                with st.spinner("Training..."):
                    result = simple_regression(df, target) if "Regression" in model_type else classification_model(df, target)
                    if result:
                        st.success("✅ Model trained!")
                        st.json(result)
    
    # Tab 7: Clustering
    with tabs[6]:
        df = clustering_ui(df)
    
    # Tab 8: Hypothesis Testing
    with tabs[7]:
        hypothesis_testing_ui(df)
    
    # Tab 9: Data Transformation
    with tabs[8]:
        df = data_transformation_ui(df)
    
    # Tab 10: Feature Engineering
    with tabs[9]:
        df = feature_engineering_ui(df)
    
    # Tab 11: Model Explainability
    with tabs[10]:
        model_explainability_ui(df)
    
    # Tab 12: NLP Queries
    with tabs[11]:
        nlp_query_ui(df)
    
    # Tab 13: Compare Datasets
    with tabs[12]:
        comparative_analysis_ui()
    
    # Tab 14: Data Sampling
    with tabs[13]:
        df = data_sampling_ui(df)
    
    # Tab 15: Automated Dashboard
    with tabs[14]:
        automated_dashboard(df)
    
    # Tab 16: Collaboration
    with tabs[15]:
        collaborative_features_ui(df)
    
    # Tab 17: Export
    with tabs[16]:
        export_functionality_ui(df)
        st.divider()
        pdf_report_ui(df)

else:
    st.markdown("""
    <div style="text-align: center; padding: 50px;">
        <h2>👆 Get Started</h2>
        <p style="font-size: 1.2em; color: #667eea;">Upload a CSV, Excel, or JSON file to unlock all features</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div style="background: white; padding: 20px; border-radius: 12px; box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08); border-top: 4px solid #667eea;">
        <h3>📊 Smart Visualizations</h3>
        <p>AI-selected charts for your data</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background: white; padding: 20px; border-radius: 12px; box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08); border-top: 4px solid #667eea;">
        <h3>🤖 AI Insights</h3>
        <p>Intelligent recommendations powered by LLM</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style="background: white; padding: 20px; border-radius: 12px; box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08); border-top: 4px solid #667eea;">
        <h3>⚡ Advanced ML</h3>
        <p>Clustering, predictions, and explainability</p>
        </div>
        """, unsafe_allow_html=True)
