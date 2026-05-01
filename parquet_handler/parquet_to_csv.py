import pandas as pd


def convert_parquet_to_csv(input_file, output_file):
    # Read the Parquet file
    df = pd.read_parquet(input_file)
    # df = df.tail(5)

    # Display the DataFrame
    print("DataFrame:")
    print(df)

    # Save the DataFrame to a CSV file
    df.to_csv(output_file, index=False)
    print(f"\nDataFrame saved to {output_file}")

def convert_parquet_to_parquet(input_file, output_file):
    # Read the Parquet file
    df = pd.read_parquet(input_file)

    #  Drop a column
    # df = df.drop(columns=['bloombergname', 'dealname'], errors='ignore')
    # df = df.drop([2, 3, 4, 6])
    df = df.drop(df.index)

    df.loc[len(df)] = ["D", 5697, "2025-08-15", "BANK 2021-BN32", ""]
    df.loc[len(df)] = ["D", 6047, "2025-08-25", "FNA 2021-M19", ""]
    df.loc[len(df)] = ["D", 6581, "2025-08-16", "ONYP 2020-1NYP", "gnr14040"]
    df.loc[len(df)] = ["D", 6827, "2025-08-25", "FREMF 2023-K507", ""]
    df.loc[len(df)] = ["D", 7047, "2025-08-26", "FNA 2021-M19", "ubs18c9"]
    df.loc[len(df)] = ["D", 7388, "2025-08-15", "HHT 2025-MAUI", ""]
    df.loc[len(df)] = ["D", 7827, "2025-08-26", "FREMF 2023-K507", "nc19mile"]
    df.loc[len(df)] = ["D", 8388, "2025-08-16", "HHT 2025-MAUI", "ms21bn32"]
    df.loc[len(df)] = ["I", 98765, "2025-08-16", "HHT 2025-MAUI", "ms21bn32"]
    df.loc[len(df)] = ["U", 5581, "2025-08-15", "ONYP 2020-1NYP", "newdealname"]

    print("DataFrame:")
    print(df)

    # Save the DataFrame to a new Parquet file
    df.to_parquet(output_file, engine="pyarrow", index=False)
    print(f"\nDataFrame saved to {output_file}")


# Example usage
input_parquet_file = 'C:\\datalake-pipeline-commons\\src\\test\\resources\\pipeline\\commons\\dataframe\\icebergdataframe\\input\\dealrpt\\appendcolumnadd\\append_column_added.parquet'

# output_csv_file = 'append_new_columns.csv'
# convert_parquet_to_csv(input_parquet_file, output_csv_file)
output_parquet_file = 'hard_delete_upsert.parquet'
convert_parquet_to_parquet(input_parquet_file, output_parquet_file)