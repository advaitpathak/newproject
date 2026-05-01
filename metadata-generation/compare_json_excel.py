# import pandas as pd
# from typing import Dict
#
#
# def compare_excel_with_json(
#     excel_path: str,
#     sheet_name: str,
#     json_mapping: Dict[str, str],
# ) -> pd.DataFrame:
#     """
#     Strict word-to-word comparison between an Excel data dictionary sheet
#     and a JSON field->description mapping.
#
#     Parameters
#     ----------
#     excel_path : str
#         Path to the Excel dictionary file
#     sheet_name : str
#         Sheet name to read (e.g. 'cmbs_deal')
#     json_mapping : Dict[str, str]
#         JSON mapping: { field_name: description }
#
#     Returns
#     -------
#     pd.DataFrame
#         Diff table with strict comparison results
#     """
#
#     # Read Excel
#     df = pd.read_excel(excel_path, sheet_name=sheet_name)
#
#     # Validate expected columns
#     required_columns = {"Data Field Name", "Description"}
#     missing_cols = required_columns - set(df.columns)
#     if missing_cols:
#         raise ValueError(f"Missing required columns in Excel sheet: {missing_cols}")
#
#     # Build Excel mapping
#     excel_map = (
#         df[["Data Field Name", "Description"]]
#         .dropna(subset=["Data Field Name"])
#         .assign(
#             field=lambda d: d["Data Field Name"].astype(str).str.strip(),
#             excel_description=lambda d: d["Description"].astype(str).str.strip(),
#         )
#         .set_index("field")["excel_description"]
#         .to_dict()
#     )
#
#     results = []
#
#     all_fields = sorted(set(excel_map.keys()) | set(json_mapping.keys()))
#
#     for field in all_fields:
#         excel_desc = excel_map.get(field)
#         json_desc = json_mapping.get(field)
#
#         if excel_desc is None:
#             status = "EXTRA_IN_JSON"
#             exact_match = False
#         elif json_desc is None:
#             status = "MISSING_IN_JSON"
#             exact_match = False
#         else:
#             exact_match = excel_desc == json_desc
#             status = "MATCH" if exact_match else "DESCRIPTION_MISMATCH"
#
#         results.append({
#             "field": field,
#             "excel_description": excel_desc,
#             "json_description": json_desc,
#             "exact_match": exact_match,
#             "status": status,
#         })
#
#     return pd.DataFrame(results).sort_values("field").reset_index(drop=True)

import pandas as pd
import re
import unicodedata
from typing import Dict


def normalize_description(text: str) -> str:
    """
    Normalize text for meaning-preserving comparison:
    - Normalize Unicode (NFKD)
    - Convert smart quotes to ASCII
    - Collapse multiple spaces
    - Trim leading/trailing whitespace
    """
    if text is None:
        return None

    text = unicodedata.normalize("NFKD", text)

    # Normalize smart quotes
    text = (
        text.replace("’", "'")
            .replace("‘", "'")
            .replace("“", '"')
            .replace("”", '"')
    )

    # Normalize whitespace
    text = re.sub(r"\s+", " ", text)

    return text.strip()


def compare_excel_with_json(
    excel_path: str,
    sheet_name: str,
    json_mapping: Dict[str, str],
) -> pd.DataFrame:
    """
    Compare Excel data dictionary with JSON mapping.
    Typography-only differences (quotes, spacing) are treated as MATCH.
    """

    df = pd.read_excel(excel_path, sheet_name=sheet_name)

    required_columns = {"HEADER FIELD", "DESCRIPTION"}
    missing_cols = required_columns - set(df.columns)
    if missing_cols:
        raise ValueError(f"Missing required columns in Excel sheet: {missing_cols}")

    excel_map = (
        df[["HEADER FIELD", "DESCRIPTION"]]
        .dropna(subset=["HEADER FIELD"])
        .assign(
            field=lambda d: d["HEADER FIELD"].astype(str).str.strip(),
            excel_description=lambda d: d["DESCRIPTION"].astype(str).str.strip(),
        )
        .set_index("field")["excel_description"]
        .to_dict()
    )

    results = []
    all_fields = sorted(set(excel_map) | set(json_mapping))

    for field in all_fields:
        excel_desc = excel_map.get(field)
        json_desc = json_mapping.get(field)

        if excel_desc is None:
            status = "EXTRA_IN_JSON"
            exact_match = False
            normalized_match = False

        elif json_desc is None:
            status = "MISSING_IN_JSON"
            exact_match = False
            normalized_match = False

        else:
            exact_match = excel_desc == json_desc
            normalized_match = (
                normalize_description(excel_desc)
                == normalize_description(json_desc)
            )

            if exact_match or normalized_match:
                status = "MATCH"
            else:
                status = "DESCRIPTION_MISMATCH"

        results.append({
            "field": field,
            "excel_description": excel_desc,
            "json_description": json_desc,
            "exact_match": exact_match,
            "normalized_match": normalized_match,
            "status": status,
        })

    return (
        pd.DataFrame(results)
        .sort_values("field")
        .reset_index(drop=True)
    )



EXCEL_PATH = "Data Feed Documentation.xlsx"
SHEET_NAME = "Normalized Tenant"

json_mapping = {
    "dosname": "Trepp internal deal name",
    "distdate": "Date on which funds are distributed to certificateholders for a particular period as defined in the servicing agreement. (YYYYMMDD)",
    "propname": "Name of loan as it appears in Annex A; where Annex A is silent (i.e., multi-property loans, Trepp assigns name)",
    "masterloanidtrepp": "Trepp Master Loan ID (Key Field)",
    "masterpropidtrepp": "Trepp Master Property ID (Key Field)",
    "normLessee1": "Name of largest tenant as of securitization (normalized)",
    "normLessee2": "Name of second largest tenant as of securitization (normalized)",
    "normLessee3": "Name of third largest tenant as of securitization (normalized)",
    "normLessee4": "Name of fourth largest tenant as of securitization (normalized)",
    "normLessee5": "Name of fifth largest tenant as of securitization (normalized)",
    "curNormLessee1": "Name of current largest tenant based on CREFC Property Periodic (normalized)",
    "curNormLessee2": "Name of current second largest tenant based on CREFC Property Periodic (normalized)",
    "curNormLessee3": "Name of current third largest tenant based on CREFC Property Periodic (normalized)",
    "curNormLessee4": "Name of current fourth largest tenant based on CREFC Property Periodic (normalized)",
    "curNormLessee5": "Name of current fifth largest tenant based on CREFC Property Periodic (normalized)"
}

diff_df = compare_excel_with_json(
    excel_path=EXCEL_PATH,
    sheet_name=SHEET_NAME,
    json_mapping=json_mapping,
)

# Show mismatches only
mismatch_df = diff_df[diff_df["status"] != "MATCH"]
print(mismatch_df)

# Optional: export to CSV
if not mismatch_df.empty:
    mismatch_df.to_csv(f"{SHEET_NAME}_excel_vs_json_diff.csv", index=False)
