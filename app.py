import streamlit as st
from data_ingestion import load_data
from data_preprocessing import preprocess_data
from eda_analysis import perform_eda
from ai_chart_selector import ai_chart_selection
from visualization_generator import generate_chart
from insight_generator import generate_insights
from report_generator import generate_report
from data_profiling import profile_data
from anomaly_detection import detect_anomalies

st.set_page_config(page_title="Advanced Automated Data Visualization Agent", layout="wide")
st.title("Advanced Automated Data Visualization Agent")

uploaded_file = st.file_uploader("Upload Dataset", type=["csv","xlsx","json"])

if uploaded_file:
    df = preprocess_data(load_data(uploaded_file))
    st.dataframe(df.head())

    st.subheader("EDA")
    st.json(perform_eda(df))

    st.subheader("Data Profiling")
    st.json(profile_data(df))

    st.subheader("Anomaly Detection")
    st.json(detect_anomalies(df))

    st.subheader("AI Visualizations")
    for chart in ai_chart_selection(df):
        st.info(chart["reason"])
        generate_chart(df, chart)

    st.subheader("Insights")
    for i in generate_insights(df):
        st.write(i)

    st.subheader("Report")
    st.text(generate_report(perform_eda(df), generate_insights(df)))
