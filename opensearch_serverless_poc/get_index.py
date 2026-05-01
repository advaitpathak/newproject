search_url = f"{host}/{index_name}/_search"

query = {
    "query": {
        "match_all": {}
    }
}

response = requests.get(
    search_url,
    auth=awsauth,
    headers={"Content-Type": "application/json"},
    data=json.dumps(query)
)

print(response.status_code)
print(json.dumps(response.json(), indent=2))