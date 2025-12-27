def profile_data(df): return {c:{'mean':df[c].mean()} for c in df.select_dtypes(include='number').columns}
