import pandas as pd
import numpy as np

def quality_report(df):
 report = {
  'total_rows': len(df),
  'total_columns': len(df.columns),
  'columns': {}
 }
 
 for col in df.columns:
  missing = df[col].isnull().sum()
  missing_pct = (missing / len(df)) * 100
  
  report['columns'][col] = {
   'dtype': str(df[col].dtype),
   'missing_count': int(missing),
   'missing_percentage': round(missing_pct, 2),
   'unique_values': df[col].nunique()
  }
 
 duplicates = df.duplicated().sum()
 report['duplicates'] = {
  'count': int(duplicates),
  'percentage': round((duplicates / len(df)) * 100, 2)
 }
 
 report['memory_usage_mb'] = round(df.memory_usage(deep=True).sum() / 1024**2, 2)
 
 return report

def data_quality_summary(df):
 quality = quality_report(df)
 summary = f"Dataset Quality Report:\n"
 summary += f"- Total Rows: {quality['total_rows']}\n"
 summary += f"- Total Columns: {quality['total_columns']}\n"
 summary += f"- Duplicates: {quality['duplicates']['count']} ({quality['duplicates']['percentage']}%)\n"
 summary += f"- Memory Usage: {quality['memory_usage_mb']} MB\n"
 summary += f"- Columns with missing data:\n"
 
 for col, info in quality['columns'].items():
  if info['missing_percentage'] > 0:
   summary += f"  • {col}: {info['missing_percentage']}% missing\n"
 
 return summary
