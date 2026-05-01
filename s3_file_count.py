import boto3

s3 = boto3.client('s3')

# s3_bucket = 'trepp-developmentservices-lake-rawdata'
# s3_file = 'attom/parcel_boundary/loadtype=delta/date=2024-06-03/'
s3_bucket = 'trepp-productionservices-rawdata'
s3_file = 'attom/parcel_boundary/loadtype=delta/date=2024-06-04/'

paginator = s3.get_paginator('list_objects_v2')
pages = paginator.paginate(Bucket=s3_bucket, Prefix=s3_file)

date_time_list = []
count = 0
for page in pages:
    for obj in page['Contents']:
        if obj['Size'] > 0:
            date_time_list.append(obj['LastModified'])
            count += 1

print(f'Total files loaded - {count}')
# print(f'remaining : {3193 - count}')  # for 48 GB file
print(f'remaining : {3228 - count}')  # for 36 GB file

start_date_time = min(date_time_list)
end_date_time = max(date_time_list)
# print(f"Start Time {start_date_time.strftime('%Y-%m-%d    %H:%M:%S')}")
# print(f"End Time {end_date_time.strftime('%Y-%m-%d    %H:%M:%S')}")
print(f"Total time - {end_date_time - start_date_time}"
      )

# 3193
# start time - 16:33:45
# obj['LastModified'].strftime('%Y-%m-%d    %H:%M:%S')
