import pandas as pd

# Define sample data
data = {
    "id": [1, 2, 3, 4, 5],
    "order_id": [1001, 1002, 1003, 1004, 1005],
    "item_id": [501, 502, 503, 504, 505],
    "customer_name": ["John Doe", "Jane Smith", "Mark Lee", "Susan Kim", "Tom Hardy"],
    "amount": [250.75, 120.00, 89.99, 300.50, 150.00],
    "status": ["Shipped", "Pending", "Delivered", "Processing", "Shipped"],
    "date": ["2024-02-11", "2024-02-11", "2024-02-11", "2024-02-11", "2024-02-11"],
    "op": ["I", "I", "D", "D", "D"]
}

# Create DataFrame
df = pd.DataFrame(data)

# Save as Parquet
df.to_parquet("test.parquet", engine="pyarrow", index=False)

print("Parquet file created: test.parquet")
