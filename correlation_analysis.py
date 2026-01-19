import pandas as pd
import numpy as np
from scipy.stats import pearsonr, spearmanr

def calculate_correlations(df):
    num_cols = df.select_dtypes(include='number').columns
    if len(num_cols) < 2:
        return None
    corr_matrix = df[num_cols].corr()
    return corr_matrix

def get_significant_correlations(df, threshold=0.7):
    corr = calculate_correlations(df)
    if corr is None:
        return []
    significant = []
    for i in range(len(corr.columns)):
        for j in range(i+1, len(corr.columns)):
            val = corr.iloc[i, j]
            if abs(val) > threshold:
                significant.append({
                    'var1': corr.columns[i],
                    'var2': corr.columns[j],
                    'correlation': round(val, 3),
                    'interpretation': 'Strong positive' if val > 0 else 'Strong negative'
                })
    return significant

def statistical_tests(df):
    num_cols = df.select_dtypes(include='number').columns
    results = []
    for i in range(len(num_cols)):
        for j in range(i+1, len(num_cols)):
            col1, col2 = num_cols[i], num_cols[j]
            # Use only rows that have non-null values in both columns
            valid_df = df[[col1, col2]].dropna()
            
            if len(valid_df) > 1:
                try:
                    # Pearson
                    pearson_r, pearson_p = pearsonr(valid_df[col1], valid_df[col2])
                    # Spearman
                    spearman_r, spearman_p = spearmanr(valid_df[col1], valid_df[col2])
                    results.append({
                        'variables': f'{col1} vs {col2}',
                        'pearson_r': round(pearson_r, 3),
                        'pearson_p': round(pearson_p, 4),
                        'spearman_r': round(spearman_r, 3),
                        'spearman_p': round(spearman_p, 4),
                        'significant': 'Yes' if min(pearson_p, spearman_p) < 0.05 else 'No'
                    })
                except:
                    continue
    return results
