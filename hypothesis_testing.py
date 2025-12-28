import pandas as pd
import numpy as np
import streamlit as st
from scipy import stats

def ttest_analysis(df: pd.DataFrame):
    """Independent t-test"""
    st.markdown("### 📊 Independent T-Test")
    
    numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
    categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
    
    if not numeric_cols or not categorical_cols:
        st.warning("Need numeric and categorical columns")
        return
    
    numeric_col = st.selectbox("Select numeric column", numeric_cols)
    categorical_col = st.selectbox("Select grouping column", categorical_cols)
    
    if st.button("Run T-Test"):
        groups = df[categorical_col].unique()
        if len(groups) != 2:
            st.warning("T-test requires exactly 2 groups")
            return
        
        group1 = df[df[categorical_col] == groups[0]][numeric_col].dropna()
        group2 = df[df[categorical_col] == groups[1]][numeric_col].dropna()
        
        t_stat, p_value = stats.ttest_ind(group1, group2)
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("T-Statistic", f"{t_stat:.4f}")
        with col2:
            st.metric("P-Value", f"{p_value:.6f}")
        with col3:
            st.metric(f"Group 1 Mean", f"{group1.mean():.2f}")
        with col4:
            st.metric(f"Group 2 Mean", f"{group2.mean():.2f}")
        
        if p_value < 0.05:
            st.success("✅ Statistically significant difference (p < 0.05)")
        else:
            st.info("❌ No significant difference (p >= 0.05)")
        
        st.write(f"**Interpretation:** p-value = {p_value:.6f}")

def anova_analysis(df: pd.DataFrame):
    """One-way ANOVA"""
    st.markdown("### 📊 One-Way ANOVA")
    
    numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
    categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
    
    if not numeric_cols or not categorical_cols:
        st.warning("Need numeric and categorical columns")
        return
    
    numeric_col = st.selectbox("Select numeric column", numeric_cols, key="anova_num")
    categorical_col = st.selectbox("Select grouping column", categorical_cols, key="anova_cat")
    
    if st.button("Run ANOVA"):
        groups = [group[numeric_col].dropna().values for name, group in df.groupby(categorical_col)]
        
        f_stat, p_value = stats.f_oneway(*groups)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("F-Statistic", f"{f_stat:.4f}")
        with col2:
            st.metric("P-Value", f"{p_value:.6f}")
        with col3:
            st.metric("Number of Groups", len(groups))
        
        if p_value < 0.05:
            st.success("✅ Significant difference between groups (p < 0.05)")
        else:
            st.info("❌ No significant difference (p >= 0.05)")
        
        st.write(f"**Interpretation:** p-value = {p_value:.6f}")

def chi_square_test(df: pd.DataFrame):
    """Chi-square test of independence"""
    st.markdown("### 📊 Chi-Square Test")
    
    categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
    
    if len(categorical_cols) < 2:
        st.warning("Need at least 2 categorical columns")
        return
    
    col1 = st.selectbox("Select first categorical column", categorical_cols)
    col2 = st.selectbox("Select second categorical column", 
                       [c for c in categorical_cols if c != col1])
    
    if st.button("Run Chi-Square Test"):
        contingency_table = pd.crosstab(df[col1], df[col2])
        chi2, p_value, dof, expected = stats.chi2_contingency(contingency_table)
        
        col1_metric, col2_metric, col3_metric, col4_metric = st.columns(4)
        with col1_metric:
            st.metric("Chi-Square", f"{chi2:.4f}")
        with col2_metric:
            st.metric("P-Value", f"{p_value:.6f}")
        with col3_metric:
            st.metric("Degrees of Freedom", dof)
        with col4_metric:
            st.metric("Cramér's V", f"{np.sqrt(chi2/len(df)):.3f}")
        
        if p_value < 0.05:
            st.success("✅ Variables are dependent (p < 0.05)")
        else:
            st.info("❌ Variables are independent (p >= 0.05)")
        
        st.markdown("**Contingency Table:**")
        st.dataframe(contingency_table)

def mannwhitneyu_test(df: pd.DataFrame):
    """Mann-Whitney U test (non-parametric)"""
    st.markdown("### 📊 Mann-Whitney U Test (Non-parametric)")
    
    numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
    categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
    
    if not numeric_cols or not categorical_cols:
        st.warning("Need numeric and categorical columns")
        return
    
    numeric_col = st.selectbox("Select numeric column", numeric_cols, key="mw_num")
    categorical_col = st.selectbox("Select grouping column", categorical_cols, key="mw_cat")
    
    if st.button("Run Mann-Whitney U"):
        groups = df[categorical_col].unique()
        if len(groups) != 2:
            st.warning("Mann-Whitney U requires exactly 2 groups")
            return
        
        group1 = df[df[categorical_col] == groups[0]][numeric_col].dropna()
        group2 = df[df[categorical_col] == groups[1]][numeric_col].dropna()
        
        u_stat, p_value = stats.mannwhitneyu(group1, group2)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("U-Statistic", f"{u_stat:.4f}")
        with col2:
            st.metric("P-Value", f"{p_value:.6f}")
        with col3:
            st.metric("Median Diff", f"{group1.median() - group2.median():.2f}")
        
        if p_value < 0.05:
            st.success("✅ Significant difference (p < 0.05)")
        else:
            st.info("❌ No significant difference (p >= 0.05)")

def hypothesis_testing_ui(df: pd.DataFrame):
    """Main hypothesis testing UI"""
    st.markdown("## 🧪 Hypothesis Testing")
    
    test_type = st.radio(
        "Select statistical test",
        ["T-Test", "ANOVA", "Chi-Square", "Mann-Whitney U"],
        horizontal=True
    )
    
    if test_type == "T-Test":
        ttest_analysis(df)
    elif test_type == "ANOVA":
        anova_analysis(df)
    elif test_type == "Chi-Square":
        chi_square_test(df)
    elif test_type == "Mann-Whitney U":
        mannwhitneyu_test(df)
