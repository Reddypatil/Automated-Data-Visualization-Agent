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

from feature_selection import feature_selection_ui
import streamlit.components.v1 as components

st.set_page_config(page_title="Automated Data Visualization Agent",
                   layout="wide",
                   initial_sidebar_state="expanded")

# Force Dark Mode and apply theme
st.markdown("""
<style>
    /* Force dark theme colors */
    :root {
        --primary-color: #ff4b4b;
        --background-color: #0e1117;
        --secondary-background-color: #262730;
        --text-color: #fafafa;
        --font: sans-serif;
    }
    .main { background: #0e1117; color: #fafafa; }
    .header-title {
        background: #1e1e1e;
        color: white; padding: 40px 20px; border-radius: 15px;
        text-align: center; box-shadow: 0 10px 40px rgba(0,0,0,0.5);
        margin-bottom: 30px;
        border: 1px solid #333;
    }
    .header-title h1 { 
        font-size: 3em; 
        font-weight: 800; 
        margin: 0; 
        text-shadow: 0 2px 10px rgba(0,0,0,0.5);
        background: #ff4b4b;
        padding: 10px 20px;
        border-radius: 10px;
        display: inline-block;
    }
    /* Style for the sidebar navigation box */
    [data-testid="stSidebarNav"] {
        background-color: rgba(255, 255, 255, 0.05);
        border-radius: 15px;
        padding: 10px;
        margin-bottom: 20px;
    }
    [data-testid="stSidebar"] {
        background-color: #262730;
    }
    [data-testid="stSidebar"] .stRadio {
        background-color: rgba(255, 255, 255, 0.05);
        padding: 20px;
        border-radius: 15px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
    }
    [data-testid="stSidebar"] .stRadio div[role="radiogroup"] > label {
        background-color: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 8px 12px;
        border-radius: 8px;
        margin-bottom: 8px;
        transition: all 0.3s ease;
        cursor: pointer;
    }
    [data-testid="stSidebar"] .stRadio div[role="radiogroup"] > label:hover {
        background-color: rgba(255, 255, 255, 0.1);
        border-color: #ff4b4b;
        transform: translateX(5px);
    }
    [data-testid="stSidebar"] .stRadio div[role="radiogroup"] [data-testid="stWidgetLabel"] {
        color: #fafafa !important;
        font-weight: 600;
    }
    /* Metric styling for dark mode */
    [data-testid="stMetricValue"] {
        color: #ff4b4b !important;
    }
</style>
""",
            unsafe_allow_html=True)

# Toggle dark mode - Removed to keep always in dark mode
# with st.sidebar:
#    toggle_dark_mode()

# Header
st.markdown("""
<div class="header-title">
    <h1>Automated Data Visualization Agent</h1>
    <p>Complete AI-Powered Analytics & Intelligence Platform</p>
</div>
""", unsafe_allow_html=True)

# Zoom In / Zoom Out floating widget - uses component to bypass React onclick restrictions
components.html("""
<style>
    body { margin: 0; padding: 0; background: transparent; overflow: hidden; }
    .zoom-controls {
        position: fixed;
        bottom: 20px;
        right: 10px;
        z-index: 9999;
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 6px;
        background: #1e1e1e;
        padding: 10px 8px;
        border-radius: 14px;
        border: 1px solid #ff4b4b;
        box-shadow: 0 4px 20px rgba(255,75,75,0.4);
    }
    .zoom-label {
        color: #aaa;
        font-size: 10px;
        font-weight: 700;
        letter-spacing: 1px;
        font-family: sans-serif;
    }
    .zoom-btn {
        background: #ff4b4b;
        color: white;
        border: none;
        border-radius: 8px;
        width: 38px;
        height: 38px;
        font-size: 22px;
        font-weight: bold;
        cursor: pointer;
        transition: background 0.2s, transform 0.15s;
        line-height: 1;
    }
    .zoom-btn:hover { background: #cc2222; transform: scale(1.1); }
    .zoom-level {
        color: #ff4b4b;
        font-size: 12px;
        font-weight: 700;
        font-family: monospace;
    }
    .zoom-reset {
        background: #333;
        color: #ccc;
        border: 1px solid #555;
        border-radius: 6px;
        width: 38px;
        height: 22px;
        font-size: 9px;
        cursor: pointer;
        font-family: sans-serif;
    }
    .zoom-reset:hover { background: #555; }
</style>

<div class="zoom-controls">
    <span class="zoom-label">ZOOM</span>
    <button class="zoom-btn" id="btnIn">+</button>
    <div class="zoom-level" id="lvl">100%</div>
    <button class="zoom-btn" id="btnOut">−</button>
    <button class="zoom-reset" id="btnReset">Reset</button>
</div>

<script>
    var zoom = 1.0;
    var target = window.parent.document.body;

    function apply() {
        target.style.zoom = zoom;
        document.getElementById('lvl').innerText = Math.round(zoom * 100) + '%';
    }

    document.getElementById('btnIn').addEventListener('click', function() {
        if (zoom < 2.0) { zoom = Math.round((zoom + 0.1) * 10) / 10; apply(); }
    });
    document.getElementById('btnOut').addEventListener('click', function() {
        if (zoom > 0.4) { zoom = Math.round((zoom - 0.1) * 10) / 10; apply(); }
    });
    document.getElementById('btnReset').addEventListener('click', function() {
        zoom = 1.0; apply();
    });
</script>
""", height=180)

# Sidebar
with st.sidebar:
    st.title("🎯 Navigation")
    nav_option = st.radio("Select Module:", [
        "EDA", "Quality", "Visualizations", "Advanced Analytics",
        "AI Insights", "Predictions", "Clustering", "Explainability",
        "Transformation", "Hypothesis Testing", "Feature Engineering", "Feature Selection",
        "Sampling", "NLP Queries", "Compare Datasets", "Collaboration",
        "Export/PDF", "Automated Dashboard"
    ])

    st.divider()
    st.markdown("""
    **Modules Overview:**
    - **Core:** EDA, Quality, Viz, Analytics
    - **AI/ML:** Insights, Models, Clustering, Explainability
    - **Tools:** Transform, Testing, Features, Sampling
    - **System:** NLP, Compare, Collab, Export
    """)

# File upload
st.markdown("### 📁 Upload Your Data")
uploaded_file = st.file_uploader("Select CSV, Excel, or JSON",
                                 type=["csv", "xlsx", "json"])

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
            st.metric("🔢 Numeric",
                      len(df.select_dtypes(include='number').columns))
        st.dataframe(df.head(10), use_container_width=True)

    st.divider()

    # Map navigation to content
    st.markdown(f'<div id="{nav_option.lower()}"></div>',
                unsafe_allow_html=True)

    if nav_option == "EDA":
        st.markdown("## Exploratory Data Analysis")
        col1, col2, col3 = st.columns(3)
        eda = perform_eda(df)
        with col1:
            st.metric("Total Rows", eda['rows'])
        with col2:
            st.metric("Total Columns", eda['cols'])
        with col3:
            st.metric("Numeric Cols",
                      len(df.select_dtypes(include='number').columns))
        st.json(eda)

        st.markdown("### Data Profiling")
        profile = profile_data(df)
        st.json(profile)

    elif nav_option == "Quality":
        st.markdown("## Data Quality Report")
        quality = quality_report(df)
        st.info(data_quality_summary(df))

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(
                "Missing",
                sum([
                    col['missing_count']
                    for col in quality['columns'].values()
                ]))
        with col2:
            st.metric("Duplicates", quality['duplicates']['count'])
        with col3:
            st.metric("Memory (MB)", quality['memory_usage_mb'])

        quality_df = pd.DataFrame([{
            'Column': col_name,
            'Type': col_info['dtype'],
            'Missing %': col_info['missing_percentage'],
            'Unique': col_info['unique_values']
        } for col_name, col_info in quality['columns'].items()])
        st.dataframe(quality_df, use_container_width=True)

    elif nav_option == "Visualizations":
        viz_choice = st.radio("Visualization Mode",
                              ["AI Recommended", "All Charts"],
                              horizontal=True)

        if viz_choice == "AI Recommended":
            st.markdown("## AI-Selected Visualizations")
            st.info("AI-chosen visualizations for your data")

            for chart in ai_chart_selection(df):
                st.info(chart["reason"])
                generate_chart(df, chart)
                st.divider()
        else:
            st.markdown("## Explore All Visualizations")

            num_cols = df.select_dtypes(include=['number']).columns.tolist()

            col1, col2, col3 = st.columns(3)
            with col1:
                chart_type = st.selectbox(
                    "Select Chart Type",
                    ["Bar", "Histogram", "Pie", "Scatter", "Box", "Line"])
            with col2:
                x_axis = st.selectbox("X-Axis / Category", df.columns.tolist())
            with col3:
                y_axis = st.selectbox("Y-Axis / Value (if needed)",
                                      ["None"] + num_cols)

            c = {
                'type': chart_type.lower(),
                'x': x_axis,
                'y': y_axis if y_axis != "None" else x_axis
            }

            if st.button("Generate Custom Chart"):
                generate_chart(df, c)

        st.markdown("## Correlation Heatmap")
        corr = calculate_correlations(df)
        if corr is not None:
            plot_correlation_heatmap(corr)
            significant = get_significant_correlations(df, threshold=0.7)
            if significant:
                st.success("**Strong Correlations:**")
                for item in significant:
                    st.markdown(
                        f"• **{item['var1']}** ↔ **{item['var2']}**: {item['correlation']}"
                    )

    elif nav_option == "Advanced Analytics":
        st.markdown("## Statistical Analysis")

        st.markdown("### Anomaly Detection")
        anomalies = detect_anomalies(df)
        if any(anomalies.values()):
            st.json(anomalies)
        else:
            st.success("No anomalies detected!")

        st.markdown("### Outlier Analysis")
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
            st.success("No outliers detected!")

        st.markdown("### Statistical Tests")
        tests = statistical_tests(df)
        if tests:
            st.dataframe(pd.DataFrame(tests), use_container_width=True)

        st.markdown("### Time Series Analysis")
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
                        st.metric("Date Range", analysis['date_range'])
                    with col2:
                        st.metric("Days", analysis['total_days'])
                    with col3:
                        st.metric("Mean", analysis['value_mean'])
                    with col4:
                        st.metric("Trend", analysis['trend'])
                    plot_time_series(df_ts, date_col, value_col)

    elif nav_option == "AI Insights":
        st.markdown("## AI-Powered Insights")
        if st.button("Generate AI Insights"):
            with st.spinner("Analyzing..."):
                eda = perform_eda(df)
                anomalies = detect_anomalies(df)
                corr = calculate_correlations(df)
                significant = get_significant_correlations(
                    df, 0.7) if corr is not None else []
                insights = generate_ai_insights(df, eda, anomalies,
                                                significant)
                st.success(insights)

    elif nav_option == "Predictions":
        st.markdown("## Predictive Analytics")
        num_cols = df.select_dtypes(include='number').columns.tolist()
        if len(num_cols) >= 2:
            target = st.selectbox("Target Column", num_cols)
            model_type = st.radio("Model Type",
                                  ["Regression", "Classification"],
                                  horizontal=True)
            if st.button("Train Model"):
                with st.spinner("Training..."):
                    result = simple_regression(
                        df, target
                    ) if "Regression" in model_type else classification_model(
                        df, target)
                    if result:
                        st.success("Model trained!")
                        st.json(result)

    elif nav_option == "Clustering":
        df = clustering_ui(df)

    elif nav_option == "Explainability":
        model_explainability_ui(df)

    elif nav_option == "Transformation":
        df = data_transformation_ui(df)

    elif nav_option == "Hypothesis Testing":
        hypothesis_testing_ui(df)

    elif nav_option == "Feature Engineering":
        df = feature_engineering_ui(df)

    elif nav_option == "Feature Selection":
        df = feature_selection_ui(df)

    elif nav_option == "Sampling":
        df = data_sampling_ui(df)

    elif nav_option == "NLP Queries":
        nlp_query_ui(df)

    elif nav_option == "Compare Datasets":
        comparative_analysis_ui()

    elif nav_option == "Collaboration":
        collaborative_features_ui(df)

    elif nav_option == "Export/PDF":
        export_functionality_ui(df)
        st.divider()
        pdf_report_ui(df)

    elif nav_option == "Automated Dashboard":
        automated_dashboard(df)

else:
    st.markdown("""
    <div style="text-align: center; padding: 50px;">
        <h2>👆 Get Started</h2>
        <p style="font-size: 1.2em; color: #667eea;">Upload a CSV, Excel, or JSON file to unlock all features</p>
    </div>
    """,
                unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div style="background: white; padding: 20px; border-radius: 12px; box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08); border-top: 4px solid #667eea;">
        <h3>📊 Smart Visualizations</h3>
        <p>AI-selected charts for your data</p>
        </div>
        """,
                    unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div style="background: white; padding: 20px; border-radius: 12px; box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08); border-top: 4px solid #667eea;">
        <h3>🤖 AI Insights</h3>
        <p>Intelligent recommendations powered by LLM</p>
        </div>
        """,
                    unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div style="background: white; padding: 20px; border-radius: 12px; box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08); border-top: 4px solid #667eea;">
        <h3>⚡ Advanced ML</h3>
        <p>Clustering, predictions, and explainability</p>
        </div>
        """,
                    unsafe_allow_html=True)
