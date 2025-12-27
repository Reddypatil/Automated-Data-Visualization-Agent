from scipy import stats

def detect_anomalies(df): return {c:int((abs(stats.zscore(df[c]))>3).sum()) for c in df.select_dtypes(include='number').columns}
