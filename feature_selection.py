import pandas as pd
import streamlit as st
from sklearn.feature_selection import SelectKBest, f_classif, f_regression, VarianceThreshold
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier

def feature_selection_ui(df):
    st.markdown("## Feature Selection")
    st.info("Identify the most important features in your dataset using statistical and model-based methods.")

    num_cols = df.select_dtypes(include=['number']).columns.tolist()
    
    if len(num_cols) < 2:
        st.warning("Feature selection requires at least two numerical columns.")
        return df

    col1, col2 = st.columns(2)
    with col1:
        target_col = st.selectbox("Select Target Variable", num_cols)
        method = st.selectbox("Selection Method", [
            "Statistical (SelectKBest)", 
            "Model-Based (Random Forest)", 
            "Variance Threshold",
            "Recursive Feature Elimination (RFE)",
            "Lasso Regularization (L1)"
        ])
    
    with col2:
        k_features = st.slider("Number of Features to Select", 1, len(num_cols)-1, min(5, len(num_cols)-1) if len(num_cols) > 5 else len(num_cols)-1)

    X = df[num_cols].drop(columns=[target_col]).fillna(df[num_cols].median())
    y = df[target_col].fillna(df[target_col].median())

    # Determine if it's a classification or regression task
    is_classification = y.nunique() < 10

    if st.button("Run Feature Selection"):
        try:
            selected_features = []
            if method == "Statistical (SelectKBest)":
                score_func = f_classif if is_classification else f_regression
                selector = SelectKBest(score_func=score_func, k=k_features)
                selector.fit(X, y)
                cols_idx = selector.get_support(indices=True)
                selected_features = X.columns[cols_idx].tolist()
                
                scores_df = pd.DataFrame({'Feature': X.columns, 'Score': selector.scores_}).sort_values(by='Score', ascending=False)
                st.write("Feature Scores:")
                st.dataframe(scores_df, use_container_width=True)

            elif method == "Model-Based (Random Forest)":
                model = RandomForestClassifier() if is_classification else RandomForestRegressor()
                model.fit(X, y)
                importances = model.feature_importances_
                feature_imp_df = pd.DataFrame({'Feature': X.columns, 'Importance': importances}).sort_values(by='Importance', ascending=False)
                selected_features = feature_imp_df.head(k_features)['Feature'].tolist()
                
                st.write("Feature Importances:")
                st.dataframe(feature_imp_df, use_container_width=True)

            elif method == "Variance Threshold":
                selector = VarianceThreshold(threshold=0.1)
                selector.fit(X)
                cols_idx = selector.get_support(indices=True)
                selected_features = X.columns[cols_idx].tolist()
                st.info(f"Selected {len(selected_features)} features based on variance.")

            elif method == "Recursive Feature Elimination (RFE)":
                from sklearn.feature_selection import RFE
                from sklearn.linear_model import LogisticRegression, LinearRegression
                estimator = LogisticRegression(max_iter=1000) if is_classification else LinearRegression()
                selector = RFE(estimator, n_features_to_select=k_features, step=1)
                selector = selector.fit(X, y)
                selected_features = X.columns[selector.support_].tolist()
                st.write("Feature Rankings (1 is selected):")
                ranking_df = pd.DataFrame({'Feature': X.columns, 'Ranking': selector.ranking_}).sort_values(by='Ranking')
                st.dataframe(ranking_df, use_container_width=True)

            elif method == "Lasso Regularization (L1)":
                from sklearn.linear_model import Lasso, LogisticRegression
                if is_classification:
                    model = LogisticRegression(penalty='l1', solver='liblinear', C=1.0)
                    model.fit(X, y)
                    coefs = model.coef_[0]
                else:
                    model = Lasso(alpha=0.1)
                    model.fit(X, y)
                    coefs = model.coef_
                
                coef_df = pd.DataFrame({'Feature': X.columns, 'Coefficient': coefs}).sort_values(by='Coefficient', key=abs, ascending=False)
                selected_features = coef_df.head(k_features)['Feature'].tolist()
                st.write("Lasso Coefficients:")
                st.dataframe(coef_df, use_container_width=True)

            st.success(f"Top {len(selected_features)} Features: {', '.join(selected_features)}")
            
            if st.checkbox("Keep only selected features in dataset?"):
                df = df[selected_features + [target_col]]
                st.success("Dataset updated with selected features.")
                
        except Exception as e:
            st.error(f"Error in feature selection: {str(e)}")

    return df
