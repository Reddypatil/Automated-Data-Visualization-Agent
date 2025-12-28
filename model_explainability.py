import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import seaborn as sns

def feature_importance_analysis(df: pd.DataFrame):
    """Calculate feature importance using Random Forest"""
    st.markdown("### 🎯 Feature Importance Analysis")
    
    numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
    
    if len(numeric_cols) < 2:
        st.warning("Need at least 2 numeric columns")
        return
    
    target = st.selectbox("Select target column", numeric_cols)
    features = [c for c in numeric_cols if c != target]
    
    if not features:
        st.warning("Need feature columns")
        return
    
    if st.button("Calculate Feature Importance"):
        try:
            X = df[features].fillna(df[features].mean())
            y = df[target].fillna(df[target].mean())
            
            model = RandomForestRegressor(n_estimators=100, random_state=42, max_depth=10)
            model.fit(X, y)
            
            importances = model.feature_importances_
            importance_df = pd.DataFrame({
                'Feature': features,
                'Importance': importances,
                'Percentage': (importances / importances.sum()) * 100
            }).sort_values('Importance', ascending=False)
            
            st.markdown("**Feature Importance Scores:**")
            st.dataframe(importance_df)
            
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.barh(importance_df['Feature'], importance_df['Percentage'], color='#667eea')
            ax.set_xlabel('Importance (%)')
            ax.set_title('Feature Importance')
            plt.tight_layout()
            st.pyplot(fig)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Top Feature", importance_df.iloc[0]['Feature'])
            with col2:
                st.metric("Top Importance", f"{importance_df.iloc[0]['Percentage']:.1f}%")
            with col3:
                st.metric("Model R² Score", f"{model.score(X, y):.3f}")
            
        except Exception as e:
            st.error(f"Error: {str(e)}")

def permutation_importance(df: pd.DataFrame):
    """Calculate permutation importance"""
    st.markdown("### 🔄 Permutation Importance")
    
    numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
    
    if len(numeric_cols) < 2:
        st.warning("Need at least 2 numeric columns")
        return
    
    target = st.selectbox("Select target column", numeric_cols, key="perm_target")
    features = [c for c in numeric_cols if c != target]
    
    if not features:
        st.warning("Need feature columns")
        return
    
    if st.button("Calculate Permutation Importance"):
        try:
            from sklearn.inspection import permutation_importance
            
            X = df[features].fillna(df[features].mean())
            y = df[target].fillna(df[target].mean())
            
            model = RandomForestRegressor(n_estimators=100, random_state=42, max_depth=10)
            model.fit(X, y)
            
            perm_importance = permutation_importance(model, X, y, n_repeats=10, random_state=42)
            
            perm_df = pd.DataFrame({
                'Feature': features,
                'Importance': perm_importance.importances_mean,
                'Std Dev': perm_importance.importances_std
            }).sort_values('Importance', ascending=False)
            
            st.dataframe(perm_df)
            
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.barh(perm_df['Feature'], perm_df['Importance'], 
                   xerr=perm_df['Std Dev'], color='#764ba2', capsize=5)
            ax.set_xlabel('Importance')
            ax.set_title('Permutation Importance')
            plt.tight_layout()
            st.pyplot(fig)
            
        except Exception as e:
            st.error(f"Error: {str(e)}")

def pdp_analysis(df: pd.DataFrame):
    """Partial Dependence Plot analysis"""
    st.markdown("### 📊 Partial Dependence Plots")
    
    numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
    
    if len(numeric_cols) < 2:
        st.warning("Need at least 2 numeric columns")
        return
    
    target = st.selectbox("Select target column", numeric_cols, key="pdp_target")
    features = [c for c in numeric_cols if c != target]
    feature = st.selectbox("Select feature for PDP", features)
    
    if st.button("Generate PDP"):
        try:
            X = df[features].fillna(df[features].mean())
            y = df[target].fillna(df[target].mean())
            
            model = RandomForestRegressor(n_estimators=100, random_state=42, max_depth=10)
            model.fit(X, y)
            
            feature_idx = features.index(feature)
            
            x_range = np.linspace(df[feature].min(), df[feature].max(), 50)
            pdp_values = []
            
            X_test = X.copy()
            for val in x_range:
                X_test.iloc[:, feature_idx] = val
                pdp_values.append(model.predict(X_test).mean())
            
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.plot(x_range, pdp_values, linewidth=2, color='#667eea')
            ax.fill_between(x_range, pdp_values, alpha=0.3, color='#667eea')
            ax.set_xlabel(feature)
            ax.set_ylabel('Predicted Value')
            ax.set_title(f'Partial Dependence Plot: {feature}')
            plt.tight_layout()
            st.pyplot(fig)
            
        except Exception as e:
            st.error(f"Error: {str(e)}")

def model_explainability_ui(df: pd.DataFrame):
    """Main model explainability UI"""
    st.markdown("## 🔍 Model Explainability")
    
    explainability_type = st.radio(
        "Select explainability method",
        ["Feature Importance", "Permutation Importance", "Partial Dependence"],
        horizontal=True
    )
    
    if explainability_type == "Feature Importance":
        feature_importance_analysis(df)
    elif explainability_type == "Permutation Importance":
        permutation_importance(df)
    elif explainability_type == "Partial Dependence":
        pdp_analysis(df)
