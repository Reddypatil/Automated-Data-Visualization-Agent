def ai_chart_selection(df):
 num = df.select_dtypes(include='number').columns
 cat = df.select_dtypes(include='object').columns
 charts = []
 
 if len(cat) and len(num):
  x_col, y_col = cat[0], num[0]
  unique_x = df[x_col].nunique()
  explanation = f"📊 Bar Chart: Compare {y_col} across {unique_x} categories in {x_col}. Shows how the numeric values vary by category, making it easy to identify which categories have higher or lower values."
  charts.append({'type':'bar','x':x_col,'y':y_col,'reason':explanation})
 
 for i, n in enumerate(num):
  if i < 3:
   mean_val = df[n].mean()
   std_val = df[n].std()
   min_val = df[n].min()
   max_val = df[n].max()
   explanation = f"📈 Histogram: Distribution of {n}. Shows frequency patterns - Min: {min_val:.2f}, Max: {max_val:.2f}, Mean: {mean_val:.2f}, Std Dev: {std_val:.2f}. Helps identify outliers and data concentration."
   charts.append({'type':'hist','x':n,'y':None,'reason':explanation})
 
 if len(num) >= 2:
  explanation = f"🔗 Scatter Plot: Relationship between {num[0]} and {num[1]}. Shows if variables are correlated."
  charts.append({'type':'scatter','x':num[0],'y':num[1],'reason':explanation})
 
 if len(cat) and len(num):
  explanation = f"📦 Box Plot: Distribution of {num[0]} by {cat[0]}. Shows median, quartiles, and outliers for each category."
  charts.append({'type':'box','x':cat[0],'y':num[0],'reason':explanation})
 
 return charts
