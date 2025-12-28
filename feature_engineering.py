import pandas as pd
import numpy as np
import streamlit as st
from sklearn.preprocessing import StandardScaler, MinMaxScaler, PolynomialFeatures

def polynomial_features_suggestion(df: pd.DataFrame) -> pd.DataFrame:
    """Suggest and create polynomial features"""
    st.markdown("### 🔢 Polynomial Features")
    
    numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
    if not numeric_cols:
        st.warning("No numeric columns")
        return df
    
    col = st.selectbox("Select column for polynomial expansion", numeric_cols)
    degree = st.slider("Polynomial degree", 2, 4, 2)
    
    if st.button("Create Polynomial Features"):
        try:
            poly = PolynomialFeatures(degree=degree, include_bias=False)
            poly_features = poly.fit_transform(df[[col]])
            feature_names = poly.get_feature_names_out([col])
            
            for i, feat in enumerate(feature_names):
                if feat != col:
                    df[feat] = poly_features[:, i]
            
            st.success(f"✅ Created {len(feature_names)-1} polynomial features")
        except Exception as e:
            st.error(f"Error: {str(e)}")
    
    return df

def interaction_features(df: pd.DataFrame) -> pd.DataFrame:
    """Create interaction features"""
    st.markdown("### 🔗 Interaction Features")
    
    numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
    if len(numeric_cols) < 2:
        st.warning("Need at least 2 numeric columns")
        return df
    
    col1 = st.selectbox("Select first column", numeric_cols)
    col2 = st.selectbox("Select second column", [c for c in numeric_cols if c != col1])
    
    if st.button("Create Interaction Feature"):
        feature_name = f"{col1}_×_{col2}"
        df[feature_name] = df[col1] * df[col2]
        st.success(f"✅ Created: {feature_name}")
    
    return df

def binning_features(df: pd.DataFrame) -> pd.DataFrame:
    """Create binned/categorical features"""
    st.markdown("### 📊 Binning Features")
    
    numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
    if not numeric_cols:
        st.warning("No numeric columns")
        return df
    
    col = st.selectbox("Select column to bin", numeric_cols)
    n_bins = st.slider("Number of bins", 2, 10, 5)
    
    if st.button("Create Binned Feature"):
        bin_name = f"{col}_binned"
        df[bin_name] = pd.cut(df[col], bins=n_bins, labels=[f"Bin_{i}" for i in range(n_bins)])
        st.success(f"✅ Created: {bin_name}")
    
    return df

def log_transformation(df: pd.DataFrame) -> pd.DataFrame:
    """Apply log transformation"""
    st.markdown("### 📈 Log Transformation")
    
    numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
    if not numeric_cols:
        st.warning("No numeric columns")
        return df
    
    col = st.selectbox("Select column for log transform", numeric_cols)
    
    if st.button("Apply Log Transform"):
        if (df[col] <= 0).any():
            st.warning("Column contains non-positive values. Adding offset...")
            offset = abs(df[col].min()) + 1
            df[f"{col}_log"] = np.log(df[col] + offset)
        else:
            df[f"{col}_log"] = np.log(df[col])
        st.success(f"✅ Created: {col}_log")
    
    return df

def scaling_features(df: pd.DataFrame) -> pd.DataFrame:
    """Scale features"""
    st.markdown("### 📐 Feature Scaling")
    
    numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
    if not numeric_cols:
        st.warning("No numeric columns")
        return df
    
    cols_to_scale = st.multiselect("Select columns to scale", numeric_cols)
    
    if cols_to_scale:
        scale_method = st.selectbox("Scaling method", ["Standard (Z-score)", "Min-Max"])
        
        if st.button("Apply Scaling"):
            try:
                if scale_method == "Standard (Z-score)":
                    scaler = StandardScaler()
                else:
                    scaler = MinMaxScaler()
                
                for col in cols_to_scale:
                    df[f"{col}_scaled"] = scaler.fit_transform(df[[col]])
                
                st.success(f"✅ Scaled {len(cols_to_scale)} features")
            except Exception as e:
                st.error(f"Error: {str(e)}")
    
    return df

def feature_aggregation(df: pd.DataFrame) -> pd.DataFrame:
    """Aggregate features (rolling statistics)"""
    st.markdown("### 📊 Feature Aggregation")
    
    numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
    if not numeric_cols:
        st.warning("No numeric columns")
        return df
    
    col = st.selectbox("Select column for aggregation", numeric_cols)
    window = st.slider("Window size", 2, 20, 5)
    
    if st.button("Create Rolling Features"):
        try:
            df[f"{col}_rolling_mean"] = df[col].rolling(window=window).mean()
            df[f"{col}_rolling_std"] = df[col].rolling(window=window).std()
            df[f"{col}_rolling_max"] = df[col].rolling(window=window).max()
            df[f"{col}_rolling_min"] = df[col].rolling(window=window).min()
            st.success(f"✅ Created 4 rolling features (window={window})")
        except Exception as e:
            st.error(f"Error: {str(e)}")
    
    return df

def feature_engineering_ui(df: pd.DataFrame) -> pd.DataFrame:
    """Main feature engineering UI"""
    st.markdown("## 🔧 Feature Engineering")
    
    feature_type = st.radio(
        "Select feature engineering technique",
        ["Polynomial", "Interactions", "Binning", "Log Transform", "Scaling", "Rolling Stats"],
        horizontal=False
    )
    
    if feature_type == "Polynomial":
        df = polynomial_features_suggestion(df)
    elif feature_type == "Interactions":
        df = interaction_features(df)
    elif feature_type == "Binning":
        df = binning_features(df)
    elif feature_type == "Log Transform":
        df = log_transformation(df)
    elif feature_type == "Scaling":
        df = scaling_features(df)
    elif feature_type == "Rolling Stats":
        df = feature_aggregation(df)
    
    return df
