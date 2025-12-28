import pandas as pd
import streamlit as st
import numpy as np

def random_sampling(df: pd.DataFrame) -> pd.DataFrame:
    """Random sampling"""
    st.markdown("### 🎲 Random Sampling")
    
    sample_type = st.radio("Sampling type", ["Absolute rows", "Percentage"])
    
    if sample_type == "Absolute rows":
        n_rows = st.slider("Number of rows", 1, len(df), min(1000, len(df)))
    else:
        percent = st.slider("Percentage", 1, 100, 50)
        n_rows = int(len(df) * percent / 100)
    
    if st.button("Apply Random Sampling"):
        sampled_df = df.sample(n=n_rows, random_state=42)
        st.success(f"✅ Sampled {n_rows} rows ({(n_rows/len(df)*100):.1f}%)")
        st.dataframe(sampled_df.head(10))
        return sampled_df
    
    return df

def stratified_sampling(df: pd.DataFrame) -> pd.DataFrame:
    """Stratified sampling"""
    st.markdown("### 🎯 Stratified Sampling")
    
    categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
    
    if not categorical_cols:
        st.warning("No categorical columns for stratification")
        return df
    
    strat_col = st.selectbox("Stratify by column", categorical_cols)
    sample_percent = st.slider("Sample percentage", 1, 100, 50)
    
    if st.button("Apply Stratified Sampling"):
        try:
            sampled_df = df.groupby(strat_col, group_keys=False).apply(
                lambda x: x.sample(frac=sample_percent/100, random_state=42)
            )
            st.success(f"✅ Stratified sample: {len(sampled_df)} rows")
            
            col1, col2 = st.columns(2)
            with col1:
                st.write("**Original Distribution:**")
                st.bar_chart(df[strat_col].value_counts())
            with col2:
                st.write("**Sample Distribution:**")
                st.bar_chart(sampled_df[strat_col].value_counts())
            
            return sampled_df
        except Exception as e:
            st.error(f"Error: {str(e)}")
    
    return df

def systematic_sampling(df: pd.DataFrame) -> pd.DataFrame:
    """Systematic sampling"""
    st.markdown("### 📊 Systematic Sampling")
    
    interval = st.slider("Sampling interval", 2, max(2, len(df)//100), 10)
    
    if st.button("Apply Systematic Sampling"):
        sampled_df = df.iloc[::interval]
        st.success(f"✅ Systematic sample: {len(sampled_df)} rows (every {interval}th row)")
        return sampled_df
    
    return df

def data_sampling_ui(df: pd.DataFrame) -> pd.DataFrame:
    """Main data sampling UI"""
    st.markdown("## 📊 Data Sampling")
    
    st.info(f"Original dataset: {len(df)} rows")
    
    sampling_method = st.radio(
        "Select sampling method",
        ["Random", "Stratified", "Systematic"],
        horizontal=True
    )
    
    if sampling_method == "Random":
        df = random_sampling(df)
    elif sampling_method == "Stratified":
        df = stratified_sampling(df)
    elif sampling_method == "Systematic":
        df = systematic_sampling(df)
    
    return df
