def generate_insights(df): return [f'{c} mean {df[c].mean():.2f}' for c in df.select_dtypes(include='number').columns]
