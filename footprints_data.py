"""
This snippet demonstrates how to access and convert the buildings
data from .csv.gz to geojson for use in common GIS tools. You will
need to install pandas, geopandas, and shapely.
"""

import pandas as pd
import geopandas as gpd
from shapely.geometry import shape

import boto3
from datetime import datetime


def check_file_exists(s3_client, s3_bucket, key):
    try:
        s3_client.head_object(Bucket=s3_bucket, Key=key)
        return True
    except:
        return False


def main():
    location = 'UnitedStates'

    dataset_links = pd.read_csv("https://minedbuildings.blob.core.windows.net/global-buildings/dataset-links.csv")
    usa_links = dataset_links[dataset_links.Location == location]

    # Set S3 bucket and file location
    s3_client = boto3.client('s3')
    # current_date = datetime.today().strftime('%Y-%m-%d')
    current_date = '2023-07-10'
    s3_bucket = 'trepp-developmentservices-lake-rawdata'
    s3_file = f'microsoft/building/{current_date}/'

    # Set counter to 0
    count = 0

    for _, row in usa_links.iterrows():
        file_name = f'{row.QuadKey}.geojson'
        if check_file_exists(s3_client, s3_bucket, s3_file + file_name):
            print(f'File already exists in S3 - {file_name}')
            pass
        else:
            df = pd.read_json(row.Url, lines=True)
            df['geometry'] = df['geometry'].apply(shape)
            gdf = gpd.GeoDataFrame(df, crs=4326)

            # Download the file in local
            temp_file = f'./geojson_files/{file_name}'
            gdf.to_file(temp_file, driver='GeoJSON')
            count += 1
            print(f'Downloaded file in local {file_name} ---- TOTAL FILES DOWNLOADED : {count}')

            # Upload the file to S3
            s3_client.upload_file(temp_file, s3_bucket, s3_file + file_name)
            print(f'Uploaded the file to S3 {file_name} ---- TOTAL FILES UPLOADED : {count}')

    print(f'Data load for {location} completed.')


if __name__ == "__main__":
    main()
