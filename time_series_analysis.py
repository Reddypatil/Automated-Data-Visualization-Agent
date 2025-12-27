import pandas as pd
import numpy as np

def detect_datetime_columns(df):
 datetime_cols = []
 for col in df.columns:
  try:
   if pd.api.types.is_datetime64_any_dtype(df[col]):
    datetime_cols.append(col)
   else:
    pd.to_datetime(df[col], errors='coerce')
    if df[col].dtype == 'object':
     test = pd.to_datetime(df[col], errors='coerce')
     if test.notna().sum() > len(df) * 0.9:
      datetime_cols.append(col)
  except:
   pass
 return datetime_cols

def time_series_analysis(df, date_col, value_col):
 try:
  df_ts = df[[date_col, value_col]].copy()
  df_ts[date_col] = pd.to_datetime(df_ts[date_col])
  df_ts = df_ts.dropna()
  df_ts = df_ts.sort_values(date_col)
  
  analysis = {
   'date_range': f"{df_ts[date_col].min().date()} to {df_ts[date_col].max().date()}",
   'total_days': (df_ts[date_col].max() - df_ts[date_col].min()).days,
   'data_points': len(df_ts),
   'value_min': round(float(df_ts[value_col].min()), 2),
   'value_max': round(float(df_ts[value_col].max()), 2),
   'value_mean': round(float(df_ts[value_col].mean()), 2),
   'trend': 'Increasing' if df_ts[value_col].iloc[-1] > df_ts[value_col].iloc[0] else 'Decreasing'
  }
  
  return analysis, df_ts
 except:
  return None, None
