import pandas as pd


# Function to read a Parquet file, delete records, and save it back
def modify_parquet(input_file, output_file, condition_column, condition_value):
    # Read the Parquet file
    df = pd.read_parquet(input_file)

    # Display the original DataFrame
    print("Original DataFrame:")
    print(df)

    # Delete records based on the condition
    modified_df = df.iloc[3:]

    # Display the modified DataFrame
    print("\nModified DataFrame (after deleting records):")
    print(modified_df)

    # Save the modified DataFrame back to a Parquet file
    modified_df.to_parquet(output_file)
    print(f"\nModified DataFrame saved to {output_file}")


# Example usage
input_parquet_file = 'D:\\workspace\\trepp\\datalake-pipeline-commons\\src\\test\\resources\\pipeline\\commons\\demo\\demo8\\input\\parquet\\demo8_inputsource.parquet'
output_parquet_file = 'output.parquet'
column_to_check = 'op'  # Column to check the condition
value_to_delete = 'D'  # Value that needs to be deleted

# Call the function
modify_parquet(input_parquet_file, output_parquet_file, column_to_check, value_to_delete)
