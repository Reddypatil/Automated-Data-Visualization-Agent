import pandas as pd
import streamlit as st
from typing import Dict, List

def rename_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Rename columns interactively"""
    st.markdown("### 📝 Rename Columns")
    rename_dict = {}
    cols = st.multiselect("Select columns to rename", df.columns)
    
    for col in cols:
        new_name = st.text_input(f"New name for '{col}'", value=col)
        if new_name and new_name != col:
            rename_dict[col] = new_name
    
    if rename_dict and st.button("Apply Rename"):
        df = df.rename(columns=rename_dict)
        st.success(f"✅ Renamed {len(rename_dict)} columns")
    
    return df

def drop_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Drop columns interactively"""
    st.markdown("### 🗑️ Drop Columns")
    cols_to_drop = st.multiselect("Select columns to drop", df.columns, key="drop_cols")
    
    if cols_to_drop and st.button("Drop Columns"):
        df = df.drop(columns=cols_to_drop)
        st.success(f"✅ Dropped {len(cols_to_drop)} columns")
    
    return df

def convert_types(df: pd.DataFrame) -> pd.DataFrame:
    """Convert column data types"""
    st.markdown("### 🔄 Convert Data Types")
    col = st.selectbox("Select column to convert", df.columns)
    
    if col:
        current_type = str(df[col].dtype)
        st.info(f"Current type: {current_type}")
        
        new_type = st.selectbox("Convert to:", [
            "int64", "float64", "string", "datetime64[ns]", "category", "boolean"
        ])
        
        if st.button("Convert Type"):
            try:
                if new_type == "datetime64[ns]":
                    df[col] = pd.to_datetime(df[col])
                elif new_type == "int64":
                    df[col] = df[col].astype('int64')
                elif new_type == "float64":
                    df[col] = df[col].astype('float64')
                elif new_type == "category":
                    df[col] = df[col].astype('category')
                elif new_type == "boolean":
                    df[col] = df[col].astype('boolean')
                else:
                    df[col] = df[col].astype(new_type)
                st.success(f"✅ Converted to {new_type}")
            except Exception as e:
                st.error(f"❌ Conversion failed: {str(e)}")
    
    return df

def filter_data(df: pd.DataFrame) -> pd.DataFrame:
    """Filter data based on column values"""
    st.markdown("### 🔍 Filter Data")
    col = st.selectbox("Filter by column", df.columns)
    
    if col:
        if df[col].dtype in ['int64', 'float64']:
            min_val, max_val = st.slider(
                f"Select range for {col}",
                float(df[col].min()),
                float(df[col].max()),
                (float(df[col].min()), float(df[col].max()))
            )
            df = df[(df[col] >= min_val) & (df[col] <= max_val)]
        else:
            values = st.multiselect(f"Select values for {col}", df[col].unique())
            if values:
                df = df[df[col].isin(values)]
        
        st.success(f"✅ Filtered to {len(df)} rows")
    
    return df

def handle_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    """Handle missing values"""
    st.markdown("### ⚠️ Handle Missing Values")
    
    if df.isnull().sum().sum() == 0:
        st.success("✅ No missing values!")
        return df
    
    missing = df.isnull().sum()
    missing = missing[missing > 0]
    
    st.write(f"Missing values found in {len(missing)} columns:")
    st.json(missing.to_dict())
    
    method = st.selectbox("Handling method", [
        "Drop rows with missing values",
        "Fill with mean (numeric)",
        "Fill with median (numeric)",
        "Fill with forward fill",
        "Fill with backward fill",
        "Fill with specific value"
    ])
    
    if st.button("Apply"):
        try:
            if method == "Drop rows with missing values":
                df = df.dropna()
            elif method == "Fill with mean (numeric)":
                df = df.fillna(df.select_dtypes(include=['number']).mean())
            elif method == "Fill with median (numeric)":
                df = df.fillna(df.select_dtypes(include=['number']).median())
            elif method == "Fill with forward fill":
                df = df.fillna(method='ffill')
            elif method == "Fill with backward fill":
                df = df.fillna(method='bfill')
            elif method == "Fill with specific value":
                fill_val = st.text_input("Enter fill value")
                if fill_val:
                    df = df.fillna(fill_val)
            
            st.success("✅ Applied missing value handling")
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
    
    return df

def remove_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    """Remove duplicate rows"""
    st.markdown("### 🔄 Remove Duplicates")
    
    duplicates = df.duplicated().sum()
    st.info(f"Found {duplicates} duplicate rows")
    
    if duplicates > 0 and st.button("Remove Duplicates"):
        df = df.drop_duplicates()
        st.success(f"✅ Removed {duplicates} duplicate rows")
    
    return df

def data_transformation_ui(df: pd.DataFrame) -> pd.DataFrame:
    """Main transformation UI"""
    st.markdown("## 🔧 Data Transformation")
    
    action = st.radio(
        "Select transformation",
        ["Rename Columns", "Drop Columns", "Convert Types", "Filter Data",
         "Handle Missing", "Remove Duplicates"],
        horizontal=True
    )
    
    if action == "Rename Columns":
        df = rename_columns(df)
    elif action == "Drop Columns":
        df = drop_columns(df)
    elif action == "Convert Types":
        df = convert_types(df)
    elif action == "Filter Data":
        df = filter_data(df)
    elif action == "Handle Missing":
        df = handle_missing_values(df)
    elif action == "Remove Duplicates":
        df = remove_duplicates(df)
    
    return df
