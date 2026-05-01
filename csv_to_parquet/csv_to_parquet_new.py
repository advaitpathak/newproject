import pandas as pd

# Create DataFrame
df = pd.read_csv("D:\\workspace\\newproject\\parquet_handler\\append_new_columns.csv")

# Save as Parquet
df.to_parquet("append_new_columns.parquet", engine="pyarrow", index=False)

print("Parquet file created: test.parquet")
