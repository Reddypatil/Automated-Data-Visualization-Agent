def preprocess_data(df):
 df=df.drop_duplicates()
 return df.ffill()
