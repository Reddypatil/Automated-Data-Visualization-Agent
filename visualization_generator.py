import matplotlib.pyplot as plt,streamlit as st

def generate_chart(df,c):
 plt.figure()
 if c['type']=='bar': df.groupby(c['x'])[c['y']].mean().plot(kind='bar')
 else: plt.hist(df[c['x']],bins=10)
 st.pyplot(plt); plt.clf()
