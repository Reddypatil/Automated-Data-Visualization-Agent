import matplotlib.pyplot as plt
import streamlit as st
import seaborn as sns
import pandas as pd

def generate_chart(df, c):
    fig = plt.figure(figsize=(10, 5))
    try:
        # Pre-process data: Ensure numeric columns are actually numeric
        if 'y' in c and c['y'] in df.columns:
            df[c['y']] = pd.to_numeric(df[c['y']], errors='coerce')
        
        if c['type'] == 'bar':
            # Drop NAs and ensure we have numeric data for mean
            plot_df = df.dropna(subset=[c['x'], c['y']])
            if not plot_df.empty:
                plot_df.groupby(c['x'])[c['y']].mean().sort_values(ascending=False).head(10).plot(kind='bar', color='#667eea')
                plt.title(f'Average {c["y"]} by {c["x"]} (Top 10)')
            else:
                st.warning(f"No valid numeric data to plot for {c['y']}")
                return

        elif c['type'] == 'hist':
            plt.hist(df[c['x']].dropna(), bins=20, color='#764ba2', edgecolor='white', alpha=0.8)
            plt.title(f'Distribution of {c["x"]}')
            plt.xlabel(c['x'])

        elif c['type'] == 'pie':
            counts = df[c['x']].value_counts().head(8)
            if not counts.empty:
                counts.plot(kind='pie', autopct='%1.1f%%', cmap='viridis')
                plt.title(f'Proportion of {c["x"]} (Top 8)')
                plt.ylabel('')
            else:
                st.warning(f"No data to plot for {c['x']}")
                return

        elif c['type'] == 'scatter':
            plot_df = df.dropna(subset=[c['x'], c['y']])
            if not plot_df.empty:
                plt.scatter(plot_df[c['x']], plot_df[c['y']], alpha=0.5, color='#667eea', s=40)
                try:
                    sns.regplot(data=plot_df, x=c['x'], y=c['y'], scatter=False, color='#ef4444')
                except:
                    pass # Skip trendline if it fails
                plt.title(f'{c["y"]} vs {c["x"]} with Trendline')
                plt.xlabel(c['x'])
                plt.ylabel(c['y'])
            else:
                st.warning("Insufficient data for scatter plot")
                return

        elif c['type'] == 'box':
            plot_df = df.dropna(subset=[c['x'], c['y']])
            if not plot_df.empty:
                sns.boxplot(data=plot_df, x=c['x'], y=c['y'], palette='Set3')
                plt.title(f'{c["y"]} Distribution by {c["x"]}')
                plt.xticks(rotation=45)
            else:
                st.warning("Insufficient data for box plot")
                return

        elif c['type'] == 'line':
            plot_df = df.dropna(subset=[c['x'], c['y']]).sort_values(c['x'])
            if not plot_df.empty:
                plot_df.plot(x=c['x'], y=c['y'], marker='o', color='#667eea')
                plt.title(f'{c["y"]} Trend by {c["x"]}')
            else:
                st.warning("Insufficient data for line chart")
                return

        plt.tight_layout()
        st.pyplot(fig)
    except Exception as e:
        st.error(f"Error generating {c['type']} chart: {str(e)}")
    finally:
        plt.close(fig)

def plot_correlation_heatmap(corr_matrix):
    if corr_matrix is None or corr_matrix.empty:
        st.warning("Correlation matrix is empty.")
        return
        
    fig = plt.figure(figsize=(10, 8))
    try:
        sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0, fmt='.2f')
        plt.title('Correlation Matrix Heatmap')
        plt.tight_layout()
        st.pyplot(fig)
    except Exception as e:
        st.error(f"Error generating heatmap: {str(e)}")
    finally:
        plt.close(fig)

def plot_time_series(df_ts, date_col, value_col):
    if df_ts is None or df_ts.empty:
        st.warning("Time series data is empty.")
        return
        
    fig = plt.figure(figsize=(12, 5))
    try:
        plt.plot(df_ts[date_col], df_ts[value_col], linewidth=2, marker='o')
        plt.title(f'{value_col} Over Time')
        plt.xlabel('Date')
        plt.ylabel(value_col)
        plt.xticks(rotation=45)
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        st.pyplot(fig)
    except Exception as e:
        st.error(f"Error generating time series: {str(e)}")
    finally:
        plt.close(fig)
