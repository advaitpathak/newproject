import pandas as pd
from datetime import datetime, timedelta
import random

input_file = "iceberg_inputsource.parquet"
output_file = "iceberg_inputsource_updated.parquet"

# Read existing parquet
df = pd.read_parquet(input_file, engine="pyarrow")

# Detect timestamp string format from sample row
timestamp_format = "%Y-%m-%d %H:%M:%S.%f"

# Base template from existing columns
base_record = {col: None for col in df.columns}

# Generate 5 unique rows
new_records = []
start_fips = random.randint(1000000000, 9999999999)
start_date = datetime(2024, 8, 1)

for i in range(5):
    record = base_record.copy()
    record.update({
        "DL_TIMESTAMP": datetime.now().strftime(timestamp_format),
        "report_date": str((start_date + timedelta(days=i)).strftime("%Y%m%d")),  # keep as string
        "fips_assessors_parcel_number": str(start_fips + i),
        "site_street_address": "123 MAIN ST",
        "site_city": "AUSTIN",
        "site_state": "TX",
        "site_zip": "73301",
        "site_county": "Travis County, TX",
        "owner_name": f"JOHN DOE {i+1}",
        "owner_street_address": "456 MARKET ST",
        "owner_city": "AUSTIN",
        "owner_state": "TX",
        "owner_zip": "73301",
        "flag_owner_occupancy": "y",
        "last_purchase_price": "500000.00",
        "adjusted_assessor_property_value": "500000.00",
        "recent_annual_property_taxes": "10000.00",
        "bldg_square_footage_assessor": "2500",
        "number_buildings_on_this_parcel": "1",
        "year_built": "2010",
        "lot_size_type": "S",
        "lot_size": "0.25",
        "estimated_pct_property_value_change_under_current_owner": "5",
        "property_use_derived_from_assessor": "Residential",
        "property_use_derived_from_owner_name_or_tenant_biz": "Residential",
        "property_use_general_category": "Single Family",
        "property_use_overall_category": "Residential",
        "multiple_source_property_use_reliability_score": "1",
        "current_mtg_loan_amount": "300000",
        "current_mtg_origination_date": "20200101",
        "current_mtg_lender_name": "ABC Bank",
        "default_history_textual_comment": "NO DEFAULTS IN AVAILABLE RECORDS",
        "existing_mtg_risk_score": "21",
        "new_applicant_underwriting_score": "B",
        "default_risk_based_on_property_use": "21",
        "flag_multi_parcel_property": "N",
        "legal_description": "LOT 1 BLK 1 SAMPLE SUBDIVISION",
        "fips": "12345",
        "apn": "67890",
        "loaddt": datetime.now().strftime(timestamp_format)
    })
    new_records.append(record)

# Create DataFrame with same column order
df_new = pd.DataFrame(new_records)[df.columns]

# Force column dtypes to match original df
for col in df.columns:
    df_new[col] = df_new[col].astype(df[col].dtype)

# Append and save
df_updated = pd.concat([df, df_new], ignore_index=True)
df_updated.to_parquet(output_file, engine="pyarrow", index=False)

print(f"✅ Added 5 unique records with matching dtypes. Saved to {output_file}")
