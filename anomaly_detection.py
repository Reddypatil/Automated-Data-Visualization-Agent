from scipy import stats
import numpy as np

def detect_anomalies(df): return {c:int((abs(stats.zscore(df[c].dropna()))>3).sum()) for c in df.select_dtypes(include='number').columns}
