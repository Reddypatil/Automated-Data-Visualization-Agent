import pandas as pd

def load_data(f):
 if f.name.endswith('csv'):
  return pd.read_csv(f)
 elif f.name.endswith('json'):
  return pd.read_json(f)
 else:
  return pd.read_excel(f)
