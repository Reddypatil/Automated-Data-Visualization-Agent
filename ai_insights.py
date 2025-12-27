import os
import json

def generate_ai_insights(df, eda_results, anomalies, correlations):
 try:
  from openai import OpenAI
  
  api_key = os.getenv('AI_INTEGRATIONS_OPENAI_API_KEY')
  if not api_key:
   return "AI insights unavailable - API key not configured"
  
  client = OpenAI(api_key=api_key)
  
  data_summary = f"""
  Dataset Summary:
  - Rows: {len(df)}, Columns: {len(df.columns)}
  - Numeric columns: {len(df.select_dtypes(include='number').columns)}
  - EDA: {json.dumps(eda_results, default=str)}
  - Anomalies detected: {anomalies}
  - Strong correlations: {correlations}
  """
  
  response = client.chat.completions.create(
   model="gpt-4o-mini",
   messages=[
    {
     "role": "system",
     "content": "You are a data analyst expert. Provide concise, actionable insights about a dataset in 2-3 sentences."
    },
    {
     "role": "user",
     "content": f"Analyze this dataset and provide key insights:\n{data_summary}"
    }
   ],
   max_tokens=300
  )
  
  return response.choices[0].message.content
 except Exception as e:
  return f"AI insights error: {str(e)}"
