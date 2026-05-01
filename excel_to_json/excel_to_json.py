# convert excel file to json
import pandas as pd
import json


def excel_to_json(excel_file, sheet_name=None):
    """
    Convert an Excel file to JSON format.

    :param excel_file: Path to the Excel file.
    :param sheet_name: Name of the sheet to convert. If None, converts all sheets.
    :return: JSON representation of the Excel data.
    """
    try:
        # Read the Excel file
        if sheet_name:
            df = pd.read_excel(excel_file, sheet_name=sheet_name)
        else:
            df = pd.read_excel(excel_file, sheet_name=None)  # Read all sheets

        # Convert DataFrame(s) to JSON
        if isinstance(df, dict):  # If multiple sheets are read
            json_data = {sheet: df[sheet].to_dict(orient='records') for sheet in df}
        else:
            json_data = df.to_dict(orient='records')

        output_json = json.dumps(json_data, indent=4)
        with open("fetch_tickers.json", "w") as json_file:
            json_file.write(output_json)
        return output_json

    except Exception as e:
        print(f"Error converting Excel to JSON: {e}")
        return None


def excel_to_csv(excel_file, sheet_name=None):
    """
    Convert an Excel file to CSV format.

    :param excel_file: Path to the Excel file.
    :param sheet_name: Name of the sheet to convert. If None, converts all sheets.
    :return: None
    """
    try:
        # Read the Excel file
        if sheet_name:
            df = pd.read_excel(excel_file, sheet_name=sheet_name)
            csv_file = f"{sheet_name}.csv"
            df.to_csv(csv_file, index=False, header=True)
            print(f"Sheet '{sheet_name}' converted to '{csv_file}'")
        else:
            xls = pd.ExcelFile(excel_file)
            for sheet in xls.sheet_names:
                df = pd.read_excel(excel_file, sheet_name=sheet)
                csv_file = f"{sheet}.csv"
                df.to_csv(csv_file, index=False)
                print(f"Sheet '{sheet}' converted to '{csv_file}'")

    except Exception as e:
        print(f"Error converting Excel to CSV: {e}")
        return None


# converted_json = excel_to_json("Full REIT List 8.18.25.xlsx", "REITs")
# print(converted_json)

excel_to_csv("Full REIT List 8.18.25.xlsx", "REITs")
