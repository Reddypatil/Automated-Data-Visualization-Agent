import pandas as pd

def load_data(f):
 return pd.read_csv(f) if f.name.endswith('csv') else pd.read_excel(f)
