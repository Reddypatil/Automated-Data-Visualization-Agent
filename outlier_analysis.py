import pandas as pd
import numpy as np
from scipy import stats

def detailed_outliers(df):
 num_cols = df.select_dtypes(include='number').columns
 results = {}
 
 for col in num_cols:
  z_scores = np.abs(stats.zscore(df[col].dropna()))
  outlier_indices = np.where(z_scores > 3)[0]
  
  if len(outlier_indices) > 0:
   outlier_values = df[col].iloc[outlier_indices].values
   results[col] = {
    'count': len(outlier_indices),
    'percentage': round((len(outlier_indices) / len(df[col].dropna())) * 100, 2),
    'threshold': round(3 * df[col].std(), 2),
    'mean': round(df[col].mean(), 2),
    'std': round(df[col].std(), 2),
    'outlier_values': [round(float(v), 2) for v in sorted(outlier_values)[:5]],
    'indices': [int(i) for i in outlier_indices[:5]]
   }
 
 return results

def remove_outliers(df, threshold=3):
 df_clean = df.copy()
 num_cols = df.select_dtypes(include='number').columns
 
 for col in num_cols:
  z_scores = np.abs(stats.zscore(df_clean[col].dropna()))
  mask = z_scores <= threshold
  df_clean = df_clean[mask]
 
 return df_clean
