import matplotlib.pyplot as plt
import streamlit as st

def generate_chart(df,c):
 fig = plt.figure()
 if c['type']=='bar': df.groupby(c['x'])[c['y']].mean().plot(kind='bar')
 else: plt.hist(df[c['x']],bins=10)
 st.pyplot(fig); plt.clf()
