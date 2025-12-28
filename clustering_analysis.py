import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans, DBSCAN, AgglomerativeClustering
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score, davies_bouldin_score
import seaborn as sns

def kmeans_clustering(df: pd.DataFrame):
    """K-means clustering analysis"""
    st.markdown("### K-Means Clustering")
    
    numeric_df = df.select_dtypes(include=['number'])
    if numeric_df.empty:
        st.warning("No numeric columns for clustering")
        return
    
    n_clusters = st.slider("Number of clusters", 2, 10, 3)
    
    if st.button("Run K-Means"):
        try:
            scaler = StandardScaler()
            scaled_data = scaler.fit_transform(numeric_df)
            
            kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
            clusters = kmeans.fit_predict(scaled_data)
            
            silhouette = silhouette_score(scaled_data, clusters)
            davies_bouldin = davies_bouldin_score(scaled_data, clusters)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Silhouette Score", f"{silhouette:.3f}")
            with col2:
                st.metric("Davies-Bouldin Index", f"{davies_bouldin:.3f}")
            with col3:
                st.metric("Inertia", f"{kmeans.inertia_:.2f}")
            
            df['Cluster'] = clusters
            
            if numeric_df.shape[1] >= 2:
                fig, ax = plt.subplots(figsize=(10, 6))
                scatter = ax.scatter(numeric_df.iloc[:, 0], numeric_df.iloc[:, 1], 
                                   c=clusters, cmap='viridis', alpha=0.6, s=50)
                ax.scatter(kmeans.cluster_centers_[:, 0], kmeans.cluster_centers_[:, 1],
                          c='red', marker='X', s=200, edgecolors='black', linewidth=2)
                ax.set_xlabel(numeric_df.columns[0])
                ax.set_ylabel(numeric_df.columns[1])
                ax.set_title(f'K-Means Clustering (k={n_clusters})')
                plt.colorbar(scatter, ax=ax)
                st.pyplot(fig)
            
            st.success("✅ Clustering complete")
            return df
        except Exception as e:
            st.error(f"Error: {str(e)}")

def dbscan_clustering(df: pd.DataFrame):
    """DBSCAN clustering"""
    st.markdown("### DBSCAN Clustering")
    
    numeric_df = df.select_dtypes(include=['number'])
    if numeric_df.empty:
        st.warning("No numeric columns")
        return
    
    eps = st.slider("EPS (neighborhood distance)", 0.1, 2.0, 0.5)
    min_samples = st.slider("Minimum samples", 2, 10, 5)
    
    if st.button("Run DBSCAN"):
        try:
            scaler = StandardScaler()
            scaled_data = scaler.fit_transform(numeric_df)
            
            dbscan = DBSCAN(eps=eps, min_samples=min_samples)
            clusters = dbscan.fit_predict(scaled_data)
            
            n_clusters = len(set(clusters)) - (1 if -1 in clusters else 0)
            n_noise = list(clusters).count(-1)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Clusters Found", n_clusters)
            with col2:
                st.metric("Noise Points", n_noise)
            with col3:
                st.metric("Total Points", len(clusters))
            
            df['Cluster'] = clusters
            
            if numeric_df.shape[1] >= 2:
                fig, ax = plt.subplots(figsize=(10, 6))
                scatter = ax.scatter(numeric_df.iloc[:, 0], numeric_df.iloc[:, 1],
                                   c=clusters, cmap='plasma', alpha=0.6, s=50)
                ax.set_xlabel(numeric_df.columns[0])
                ax.set_ylabel(numeric_df.columns[1])
                ax.set_title('DBSCAN Clustering')
                plt.colorbar(scatter, ax=ax)
                st.pyplot(fig)
            
            st.success("✅ DBSCAN complete")
            return df
        except Exception as e:
            st.error(f"Error: {str(e)}")

def hierarchical_clustering(df: pd.DataFrame):
    """Hierarchical clustering"""
    st.markdown("### Hierarchical Clustering")
    
    numeric_df = df.select_dtypes(include=['number'])
    if numeric_df.empty:
        st.warning("No numeric columns")
        return
    
    n_clusters = st.slider("Number of clusters", 2, 10, 3)
    linkage = st.selectbox("Linkage method", ["ward", "complete", "average", "single"])
    
    if st.button("Run Hierarchical"):
        try:
            scaler = StandardScaler()
            scaled_data = scaler.fit_transform(numeric_df)
            
            hierarchical = AgglomerativeClustering(n_clusters=n_clusters, linkage=linkage)
            clusters = hierarchical.fit_predict(scaled_data)
            
            df['Cluster'] = clusters
            
            if numeric_df.shape[1] >= 2:
                fig, ax = plt.subplots(figsize=(10, 6))
                scatter = ax.scatter(numeric_df.iloc[:, 0], numeric_df.iloc[:, 1],
                                   c=clusters, cmap='coolwarm', alpha=0.6, s=50)
                ax.set_xlabel(numeric_df.columns[0])
                ax.set_ylabel(numeric_df.columns[1])
                ax.set_title(f'Hierarchical Clustering ({linkage})')
                plt.colorbar(scatter, ax=ax)
                st.pyplot(fig)
            
            st.success("✅ Hierarchical clustering complete")
            return df
        except Exception as e:
            st.error(f"Error: {str(e)}")

def clustering_ui(df: pd.DataFrame) -> pd.DataFrame:
    """Main clustering UI"""
    st.markdown("## 🎯 Clustering Analysis")
    
    method = st.radio(
        "Select clustering method",
        ["K-Means", "DBSCAN", "Hierarchical"],
        horizontal=True
    )
    
    if method == "K-Means":
        result = kmeans_clustering(df)
        if result is not None:
            df = result
    elif method == "DBSCAN":
        result = dbscan_clustering(df)
        if result is not None:
            df = result
    elif method == "Hierarchical":
        result = hierarchical_clustering(df)
        if result is not None:
            df = result
    
    if 'Cluster' in df.columns:
        st.markdown("### 📊 Cluster Distribution")
        cluster_dist = df['Cluster'].value_counts().sort_index()
        st.bar_chart(cluster_dist)
    
    return df
