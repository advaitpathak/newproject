import boto3, json
client = boto3.client('datazone', region_name='us-east-1')
domain_id = 'dzd_6l7t90mge4intz'
try:
    resp = client.search(
        domainIdentifier=domain_id,
        searchScope='ASSET',
        searchText='cmbsrptsnapshot_parquet',
        maxResults=5
    )
    print(json.dumps(resp.get('items', []), indent=2, default=str))
except Exception as e:
    print('Error:', e)
