import matplotlib.pyplot as plt
import streamlit as st
import seaborn as sns

def generate_chart(df, c):
 fig = plt.figure(figsize=(10, 5))
    try:
        if c['type'] == 'bar':
            df.groupby(c['x'])[c['y']].mean().sort_values(ascending=False).head(10).plot(kind='bar', color='#667eea')
            plt.title(f'Average {c["y"]} by {c["x"]} (Top 10)')
        elif c['type'] == 'hist':
            plt.hist(df[c['x']].dropna(), bins=20, color='#764ba2', edgecolor='white', alpha=0.8)
            plt.title(f'Distribution of {c["x"]}')
            plt.xlabel(c['x'])
        elif c['type'] == 'pie':
            df[c['x']].value_counts().head(8).plot(kind='pie', autopct='%1.1f%%', cmap='viridis')
            plt.title(f'Proportion of {c["x"]} (Top 8)')
            plt.ylabel('')
        elif c['type'] == 'scatter':
            plt.scatter(df[c['x']], df[c['y']], alpha=0.5, color='#667eea', s=40)
            sns.regplot(data=df, x=c['x'], y=c['y'], scatter=False, color='#ef4444')
            plt.title(f'{c["y"]} vs {c["x"]} with Trendline')
            plt.xlabel(c['x'])
            plt.ylabel(c['y'])
        elif c['type'] == 'box':
            sns.boxplot(data=df, x=c['x'], y=c['y'], palette='Set3')
            plt.title(f'{c["y"]} Distribution by {c["x"]}')
            plt.xticks(rotation=45)
        elif c['type'] == 'line':
            df.sort_values(c['x']).plot(x=c['x'], y=c['y'], marker='o', color='#667eea')
            plt.title(f'{c["y"]} Trend by {c["x"]}')
        plt.tight_layout()
        st.pyplot(fig)
    except Exception as e:
        st.error(f"Error generating {c['type']} chart: {str(e)}")
    finally:
        plt.close(fig)

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
