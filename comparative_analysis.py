import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

def compare_datasets(df1: pd.DataFrame, df2: pd.DataFrame):
    """Compare two datasets"""
    st.markdown("## 📊 Dataset Comparison")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Dataset 1 Rows", len(df1))
    with col2:
        st.metric("Dataset 2 Rows", len(df2))
    with col3:
        st.metric("Dataset 1 Cols", len(df1.columns))
    with col4:
        st.metric("Dataset 2 Cols", len(df2.columns))
    
    st.divider()
    
    # Column comparison
    st.markdown("### 📋 Column Comparison")
    
    cols1 = set(df1.columns)
    cols2 = set(df2.columns)
    
    common_cols = cols1.intersection(cols2)
    only_in_1 = cols1 - cols2
    only_in_2 = cols2 - cols1
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Common Columns", len(common_cols))
    with col2:
        st.metric("Only in Dataset 1", len(only_in_1))
    with col3:
        st.metric("Only in Dataset 2", len(only_in_2))
    
    if only_in_1:
        st.warning(f"Only in Dataset 1: {', '.join(list(only_in_1)[:5])}")
    if only_in_2:
        st.warning(f"Only in Dataset 2: {', '.join(list(only_in_2)[:5])}")
    
    # Statistical comparison
    if common_cols:
        st.markdown("### 📈 Statistical Comparison")
        
        numeric_common = [col for col in common_cols 
                         if df1[col].dtype in ['int64', 'float64'] and 
                         df2[col].dtype in ['int64', 'float64']]
        
        if numeric_common:
            for col in numeric_common[:3]:
                col1, col2 = st.columns(2)
                with col1:
                    st.metric(f"{col} - Dataset 1 Mean", f"{df1[col].mean():.2f}")
                with col2:
                    st.metric(f"{col} - Dataset 2 Mean", f"{df2[col].mean():.2f}")
            
            # Visualization
            comparison_cols = numeric_common[:2]
            if len(comparison_cols) >= 2:
                fig, axes = plt.subplots(1, 2, figsize=(12, 4))
                
                for idx, col in enumerate(comparison_cols):
                    axes[idx].hist(df1[col].dropna(), alpha=0.5, label='Dataset 1', bins=20)
                    axes[idx].hist(df2[col].dropna(), alpha=0.5, label='Dataset 2', bins=20)
                    axes[idx].set_xlabel(col)
                    axes[idx].set_ylabel('Frequency')
                    axes[idx].legend()
                
                st.pyplot(fig)

def comparative_analysis_ui():
    """Main comparative analysis UI"""
    st.markdown("## 🔄 Comparative Analysis")
    
    st.warning("This feature requires uploading two datasets. Use the main interface to upload multiple files.")
    
    file1 = st.file_uploader("Upload first dataset", type=["csv", "xlsx", "json"], key="comp_file1")
    file2 = st.file_uploader("Upload second dataset", type=["csv", "xlsx", "json"], key="comp_file2")
    
    if file1 and file2:
        from data_ingestion import load_data
        from data_preprocessing import preprocess_data
        
        try:
            df1 = preprocess_data(load_data(file1))
            df2 = preprocess_data(load_data(file2))
            
            st.success("✅ Both datasets loaded")
            compare_datasets(df1, df2)
            
        except Exception as e:
            st.error(f"Error: {str(e)}")
    else:
        st.info("📤 Upload two datasets to compare")
