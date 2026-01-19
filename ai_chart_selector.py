import pandas as pd

def ai_chart_selection(df):
    num = df.select_dtypes(include='number').columns
    cat = df.select_dtypes(exclude='number').columns
    charts = []
    
    # 1. Comparison: Bar Chart
    if len(cat) and len(num):
        # Pick category with reasonable cardinality
        best_cat = None
        for c in cat:
            if 1 < df[c].nunique() <= 15:
                best_cat = c
                break
        x_col = best_cat if best_cat else cat[0]
        y_col = num[0]
        explanation = f"📊 Bar Chart: Compare average **{y_col}** across **{x_col}**. This helps identify which categories perform best or show significant differences."
        charts.append({'type':'bar','x':x_col,'y':y_col,'reason':explanation})
    
    # 2. Distribution: Histograms
    for i, n in enumerate(num):
        if i < 2: # Top 2 numeric
            explanation = f"📈 Histogram: Shows the frequency distribution of **{n}**. Essential for understanding data spread, skewness, and identifying potential outliers."
            charts.append({'type':'hist','x':n,'y':None,'reason':explanation})
    
    # 3. Correlation: Scatter Plot
    if len(num) >= 2:
        explanation = f"🔗 Scatter Plot: Relationship between **{num[0]}** and **{num[1]}**. Visualizes correlation patterns and helps detect linear or non-linear trends."
        charts.append({'type':'scatter','x':num[0],'y':num[1],'reason':explanation})
    
    # 4. Composition: Pie Chart
    if len(cat):
        best_cat = None
        for c in cat:
            if 1 < df[c].nunique() <= 8:
                best_cat = c
                break
        if best_cat:
            explanation = f"🍰 Pie Chart: Proportion of **{best_cat}**. Best for visualizing part-to-whole relationships in your categorical data."
            charts.append({'type':'pie', 'x':best_cat, 'y':None, 'reason':explanation})

    # 5. Variation: Box Plot
    if len(cat) and len(num):
        explanation = f"📦 Box Plot: Statistical spread of **{num[0]}** across **{cat[0]}**. Shows the median, range, and specific outlier points for each group."
        charts.append({'type':'box','x':cat[0],'y':num[0],'reason':explanation})
    
    return charts
