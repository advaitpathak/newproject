import json, sys
with open('1776138988690.json') as f:
    data = json.load(f)
cl = data['outputs'][0]['facets']['columnLineage']
print('Keys:', list(cl.keys()))
print('_producer:', cl.get('_producer'))
print('Has dataset:', 'dataset' in cl)
print('Field count:', len(cl.get('fields', {})))
