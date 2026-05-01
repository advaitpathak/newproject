# TODO : Questions
## 1. should we look for implementing the variables as below for the graphql request pagination
##  2. should we look for implementing the offset limit pagination

import requests

session = requests.Session()
method = 'POST'
uri = 'https://graphql.cherre.com/graphql'
# body = {'query': 'query Usa_owner_unmask_v2 { usa_owner_unmask_v2( where: { tax_assessor_v2__tax_assessor_id: { zip: { _eq: "99999" } } } order_by: { cherre_usa_owner_unmask_pk: desc } limit: 100 ) { cherre_usa_owner_unmask_pk has_confidence last_seen_date occurrences_count owner_id owner_name owner_state owner_type tax_assessor_id } }'}

variables = {"zipcode": "80212", "previous_id": 3869848}
body = {
    'query': 'query AdditionalPages($zipcode: String!, $previous_id: numeric!) { tax_assessor_v2( where: { zip: { _eq: $zipcode } tax_assessor_id: { _gt: $previous_id } } order_by: { tax_assessor_id: asc } limit: 100 ) { tax_assessor_id bed_count bath_count gross_sq_ft } }',
    'variables': variables
}
headers = {'Authorization': 'Bearer YXBpLWNsaWVudC0zZTI3MjJmMC01YjBlLTQ4MjMtODgzYS00NTFkMTEyMDQ0YjhAY2hlcnJlLmNvbTpLR1A3T0toR090RFVYUmVvQTVhcTdvRkVhVWI0TjNFMlgzajJGRVhMT04ySWN5SGFPMndrMSNQaW02Q1BKIzFP', 'Content-Type': 'application/json'}

response = session.request(
    method=method,
    url=uri,
    json=body,
    headers=headers,
    verify=True,
    stream=False
)
print()