import pandas as pd

def preprocess_data(df):
    """Preprocess data with robust error handling for unhashable types (dicts/lists)"""
    try:
        # Check if any columns contain dicts or lists which make them unhashable for drop_duplicates
        for col in df.columns:
            if df[col].apply(lambda x: isinstance(x, (dict, list))).any():
                # Convert complex types to strings for hashing/deduplication
                df[col] = df[col].apply(lambda x: str(x) if isinstance(x, (dict, list)) else x)
        
        # Now safe to drop duplicates
        df = df.drop_duplicates()
        
        # Handle missing values robustly
        return df.ffill().bfill() # Forward fill then backward fill to catch all NAs
    except Exception as e:
        # Fallback if preprocessing fails
        return df
