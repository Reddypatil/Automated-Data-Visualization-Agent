import matplotlib.pyplot as plt
import streamlit as st
import seaborn as sns

def generate_chart(df, c):
 fig = plt.figure(figsize=(10, 5))
 try:
  if c['type'] == 'bar':
   df.groupby(c['x'])[c['y']].mean().plot(kind='bar')
   plt.title(f'{c["y"]} by {c["x"]}')
  elif c['type'] == 'hist':
   plt.hist(df[c['x']], bins=15, edgecolor='black', alpha=0.7)
   plt.title(f'Distribution of {c["x"]}')
   plt.xlabel(c['x'])
  elif c['type'] == 'scatter':
   plt.scatter(df[c['x']], df[c['y']], alpha=0.6)
   plt.title(f'{c["y"]} vs {c["x"]}')
   plt.xlabel(c['x'])
   plt.ylabel(c['y'])
  elif c['type'] == 'box':
   df.boxplot(column=c['y'], by=c['x'], figsize=(10, 5))
   plt.title(f'{c["y"]} by {c["x"]}')
  plt.tight_layout()
  st.pyplot(fig)
 except:
  pass
 plt.clf()

def plot_correlation_heatmap(corr_matrix):
 fig = plt.figure(figsize=(10, 8))
 sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0, fmt='.2f')
 plt.title('Correlation Matrix Heatmap')
 plt.tight_layout()
 st.pyplot(fig)
 plt.clf()

def plot_time_series(df_ts, date_col, value_col):
 fig = plt.figure(figsize=(12, 5))
 plt.plot(df_ts[date_col], df_ts[value_col], linewidth=2, marker='o')
 plt.title(f'{value_col} Over Time')
 plt.xlabel('Date')
 plt.ylabel(value_col)
 plt.xticks(rotation=45)
 plt.grid(True, alpha=0.3)
 plt.tight_layout()
 st.pyplot(fig)
 plt.clf()
