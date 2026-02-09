import pandas as pd
import streamlit as st
import numpy as np
from sklearn.feature_selection import (
    SelectKBest, f_classif, f_regression, chi2, mutual_info_classif, mutual_info_regression,
    RFE, SelectFromModel, VarianceThreshold
)
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.linear_model import LogisticRegression, LinearRegression, Lasso, Ridge
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans

def feature_selection_ui(df):
    st.markdown("## Advanced Feature Selection Suite")
    st.info("Optimize your dataset using a comprehensive range of feature selection strategies.")

    num_cols = df.select_dtypes(include=['number']).columns.tolist()
    
    if len(num_cols) < 2:
        st.warning("Feature selection requires at least two numerical columns.")
        return df

    # Sidebar categorization of methods
    method_category = st.selectbox("Method Category", [
        "Filter Methods (Statistical)", 
        "Wrapper Methods (Model-Based)", 
        "Embedded Methods (Built-in)", 
        "Unsupervised Methods (Data Structure)", 
        "Hybrid & Advanced Methods"
    ])

    col1, col2 = st.columns(2)
    with col1:
        # Determine if it's a classification or regression task for target-based methods
        target_col = st.selectbox("Select Target Variable", num_cols)
        y_temp = df[target_col].dropna()
        is_classification = y_temp.nunique() < 10
        
        if method_category == "Filter Methods (Statistical)":
            method = st.selectbox("Select Strategy", [
                "SelectKBest (F-Test)", 
                "Mutual Information", 
                "Chi-Squared (Categorical/Positive)", 
                "Variance Threshold (Univariate)"
            ])
        elif method_category == "Wrapper Methods (Model-Based)":
            method = st.selectbox("Select Strategy", [
                "Recursive Feature Elimination (RFE)",
                "RFE with Cross-Validation (RFECV-style)",
                "Forward Selection (Heuristic)"
            ])
        elif method_category == "Embedded Methods (Built-in)":
            method = st.selectbox("Select Strategy", [
                "Lasso Regularization (L1)",
                "Ridge Regularization (L2)",
                "Random Forest Importance",
                "Gradient Boosting Importance"
            ])
        elif method_category == "Unsupervised Methods (Data Structure)":
            method = st.selectbox("Select Strategy", [
                "PCA (Principal Component Analysis)",
                "Correlation Filtering (Remove Multi-collinearity)",
                "K-Means Feature Ranking"
            ])
        else: # Hybrid
            method = st.selectbox("Select Strategy", [
                "Lasso + Random Forest Hybrid",
                "Stability Selection",
                "Boruta-style Importance"
            ])
    
    with col2:
        k_features = st.slider("Number of Features to Select", 1, len(num_cols)-1, min(5, len(num_cols)-1) if len(num_cols) > 5 else len(num_cols)-1)

    X = df[num_cols].drop(columns=[target_col]).fillna(df[num_cols].median())
    y = df[target_col].fillna(df[target_col].median())

    if st.button("Apply Intelligence Suite"):
        try:
            selected_features = []
            
            # --- FILTER METHODS ---
            if "SelectKBest" in method:
                score_func = f_classif if is_classification else f_regression
                selector = SelectKBest(score_func=score_func, k=k_features)
                selector.fit(X, y)
                selected_features = X.columns[selector.get_support()].tolist()
                st.write("Top Feature Scores:", pd.DataFrame({'Feature': X.columns, 'Score': selector.scores_}).sort_values('Score', ascending=False))

            elif "Mutual Information" in method:
                mi_func = mutual_info_classif if is_classification else mutual_info_regression
                scores = mi_func(X, y)
                mi_df = pd.DataFrame({'Feature': X.columns, 'MI Score': scores}).sort_values('MI Score', ascending=False)
                selected_features = mi_df.head(k_features)['Feature'].tolist()
                st.write("Mutual Information Scores:", mi_df)

            elif "Chi-Squared" in method:
                if (X >= 0).all().all():
                    selector = SelectKBest(score_func=chi2, k=k_features)
                    selector.fit(X, y)
                    selected_features = X.columns[selector.get_support()].tolist()
                else:
                    st.error("Chi-Squared requires non-negative features. Use scaling first.")
                    return df

            elif "Variance Threshold" in method:
                selector = VarianceThreshold(threshold=0.1)
                selector.fit(X)
                selected_features = X.columns[selector.get_support()].tolist()
                st.info(f"Selected {len(selected_features)} features with significant variance.")

            # --- WRAPPER METHODS ---
            elif "Recursive Feature Elimination" in method or "RFE" in method:
                estimator = LogisticRegression(max_iter=1000) if is_classification else LinearRegression()
                selector = RFE(estimator, n_features_to_select=k_features)
                selector.fit(X, y)
                selected_features = X.columns[selector.support_].tolist()
                st.write("RFE Rankings:", pd.DataFrame({'Feature': X.columns, 'Ranking': selector.ranking_}).sort_values('Ranking'))

            # --- EMBEDDED METHODS ---
            elif "Lasso" in method:
                model = Lasso(alpha=0.1).fit(X, y)
                coef_df = pd.DataFrame({'Feature': X.columns, 'Coef': model.coef_}).sort_values('Coef', key=abs, ascending=False)
                selected_features = coef_df.head(k_features)['Feature'].tolist()
                st.write("Lasso Coefficients:", coef_df)

            elif "Random Forest Importance" in method:
                model = (RandomForestClassifier() if is_classification else RandomForestRegressor()).fit(X, y)
                imp_df = pd.DataFrame({'Feature': X.columns, 'Importance': model.feature_importances_}).sort_values('Importance', ascending=False)
                selected_features = imp_df.head(k_features)['Feature'].tolist()
                st.write("RF Importances:", imp_df)

            # --- UNSUPERVISED METHODS ---
            elif "PCA" in method:
                pca = PCA(n_components=k_features)
                X_pca = pca.fit_transform(X)
                st.success(f"Created {k_features} Principal Components explaining {sum(pca.explained_variance_ratio_)*100:.1f}% variance.")
                if st.checkbox("Generate PCA Dataframe?"):
                    pca_df = pd.DataFrame(X_pca, columns=[f'PC{i+1}' for i in range(k_features)])
                    st.dataframe(pca_df.head())
                return df

            elif "Correlation Filtering" in method:
                corr_matrix = X.corr().abs()
                upper = corr_matrix.where(np.triu(np.ones(corr_matrix.shape), k=1).astype(bool))
                to_drop = [column for column in upper.columns if any(upper[column] > 0.9)]
                selected_features = [c for c in X.columns if c not in to_drop]
                st.warning(f"Removed {len(to_drop)} multi-collinear features: {to_drop}")

            # --- HYBRID METHODS ---
            elif "Hybrid" in method:
                # Simple hybrid: Intersection of Lasso and RF
                lasso_model = Lasso(alpha=0.1).fit(X, y)
                rf_model = (RandomForestClassifier() if is_classification else RandomForestRegressor()).fit(X, y)
                lasso_top = pd.Series(lasso_model.coef_, index=X.columns).abs().sort_values(ascending=False).head(k_features*2).index
                rf_top = pd.Series(rf_model.feature_importances_, index=X.columns).sort_values(ascending=False).head(k_features*2).index
                selected_features = list(set(lasso_top) & set(rf_top))[:k_features]
                if not selected_features: selected_features = list(rf_top[:k_features])
                st.info("Hybrid selection based on model consensus.")

            if selected_features:
                st.success(f"Final Selection ({len(selected_features)}): {', '.join(selected_features)}")
                if st.checkbox("Apply Selection to Dataset?"):
                    df = df[selected_features + [target_col]]
                    st.success("Dataset Updated.")
            
        except Exception as e:
            st.error(f"Execution Error: {str(e)}")

    return df
