def ai_chart_selection(df):
 num=df.select_dtypes(include='number').columns
 cat=df.select_dtypes(include='object').columns
 charts=[]
 if len(cat) and len(num): charts.append({'type':'bar','x':cat[0],'y':num[0],'reason':'AI categorical vs numeric'})
 for n in num: charts.append({'type':'hist','x':n,'y':None,'reason':'Distribution'})
 return charts
