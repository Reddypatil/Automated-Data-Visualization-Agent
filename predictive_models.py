import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import r2_score, accuracy_score, mean_squared_error

def simple_regression(df, target_col):
 try:
  num_cols = df.select_dtypes(include='number').columns.tolist()
  if target_col in num_cols:
   num_cols.remove(target_col)
  
  if len(num_cols) == 0:
   return None
  
  X = df[num_cols].dropna()
  y = df.loc[X.index, target_col]
  
  X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
  
  model = LinearRegression()
  model.fit(X_train, y_train)
  
  y_pred = model.predict(X_test)
  r2 = r2_score(y_test, y_pred)
  rmse = np.sqrt(mean_squared_error(y_test, y_pred))
  
  return {
   'model_type': 'Linear Regression',
   'r2_score': round(r2, 3),
   'rmse': round(rmse, 3),
   'features_used': num_cols,
   'coefficients': {col: round(float(coef), 3) for col, coef in zip(num_cols, model.coef_)},
   'intercept': round(float(model.intercept_), 3)
  }
 except:
  return None

def classification_model(df, target_col):
 try:
  num_cols = df.select_dtypes(include='number').columns.tolist()
  if target_col in num_cols:
   num_cols.remove(target_col)
  
  if len(num_cols) == 0:
   return None
  
  X = df[num_cols].dropna()
  y = df.loc[X.index, target_col]
  
  scaler = StandardScaler()
  X_scaled = scaler.fit_transform(X)
  
  X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)
  
  model = LogisticRegression(max_iter=1000)
  model.fit(X_train, y_train)
  
  y_pred = model.predict(X_test)
  accuracy = accuracy_score(y_test, y_pred)
  
  return {
   'model_type': 'Logistic Regression',
   'accuracy': round(accuracy, 3),
   'features_used': num_cols,
   'classes': list(model.classes_),
   'intercept': round(float(model.intercept_[0]), 3)
  }
 except:
  return None
