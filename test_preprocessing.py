import pandas as pd
from data_preprocessing import preprocess_data

# Create a test DataFrame with unhashable types (dicts)
test_data = {
    'id': [1, 2, 3, 1],
    'name': ['Alice', 'Bob', 'Charlie', 'Alice'],
    'details': [
        {'age': 25, 'city': 'NYC'},
        {'age': 30, 'city': 'LA'},
        {'age': 35, 'city': 'Chicago'},
        {'age': 25, 'city': 'NYC'}  # duplicate
    ]
}

df = pd.DataFrame(test_data)
print("Original DataFrame:")
print(df)
print("\nData types:")
print(df.dtypes)

try:
    processed_df = preprocess_data(df)
    print("\nProcessed DataFrame:")
    print(processed_df)
    print("\nData types after processing:")
    print(processed_df.dtypes)
    print(f"\nOriginal rows: {len(df)}, Processed rows: {len(processed_df)}")
    print("✅ Preprocessing successful!")
except Exception as e:
    print(f"❌ Error during preprocessing: {e}")
