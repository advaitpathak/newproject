import yaml

with open('D:\\workspace\\newproject\\sftp\\serverless.yaml', 'r', encoding='utf-8') as query_file:
    query_config = yaml.load(query_file, Loader=yaml.FullLoader)
print()


import os
t = os.environ.get('list1')