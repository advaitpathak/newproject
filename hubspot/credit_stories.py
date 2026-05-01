import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs
from datetime import datetime


offset = 0
limit = 100
total = 7201

uri = 'https://api.hubapi.com/marketing-emails/v1/emails?campaign=507fae8c-4f13-4bfd-bddb-7d6238307dbd&orderBy=-created&offset={offset}&limit={limit}'
header = {'Authorization': F'Bearer {BEARER}', 'Content-Type': 'application/json'}
method = 'GET'

session = requests.Session()

while offset < total:
    print(f'offset: {offset}')
    uri = uri.format(offset=offset, limit=limit)
    response = session.request(method=method, url=uri, json=None, headers=header, verify=True)
    query_output = response.json()

    objects = query_output['objects']
    all_data = []

    for obj in objects:
        hs_email_body = obj.get('hsEmailBody')
        if hs_email_body:
            soup = BeautifulSoup(hs_email_body, 'html.parser')
            div = soup.find('div', {'id': 'hs_cos_wrapper_hs_email_body_old12'})
            if div:
                print(f'found at offset : {offset}')
    offset += limit

# print(result_dict)


# for obj in objects:
#     name = obj.get('name')
#     print("Object with name %s and published value %s", name, obj.get('isPublished'))
#     if (obj.get('isPublished') and name.startswith('US TreppWire') and name.find('_') == -1
#             and name.find('(') == -1 and name.find(')') == -1):
#         # HTML content
#         hs_email_body = obj.get('hsEmailBody')
#         if hs_email_body:
#             print("Found email body for url %s", obj.get('publishedUrl'))
#             soup = BeautifulSoup(hs_email_body, 'html.parser')
#             can_break = False
#             for credit_stories_section in soup.find_all('div', {'id': 'content'}):
#                 a_tags = credit_stories_section.select('a[href^="https://apps.trepp.com"]')  # Find all <a> tags
#                 if not can_break and len(a_tags) > 0:
#                     # LoanID's and DealID's
#                     loan_ids = []
#                     deal_names = []
#                     urls = [a['href'] for a in a_tags]  # Extract href attributes from <a> tags
#                     for url in urls:
#                         parsed_url = urlparse(url)
#                         query_params = parse_qs(parsed_url.query)
#                         if query_params.get('dealname'):
#                             deal_name = query_params.get('dealname', [])[0]
#                             deal_names.append(deal_name)
#                         if query_params.get('loanID'):
#                             loan_id = query_params.get('loanID', [])[0]
#                             loan_ids.append(loan_id)
#
#                     # Author
#                     author_email = obj.get('author')
#                     author_name = obj.get('authorName')
#
#                     # Publish date
#                     publish_epoch_time = obj.get('publishDate') / 1000  # Convert ms epoch time to sec
#                     datetime_object = datetime.fromtimestamp(publish_epoch_time)
#                     publish_date = datetime_object.strftime('%Y-%m-%d %H:%M:%S')
#                     result = {
#                         "content_source": obj['fromName'],
#                         "content_type": "article",
#                         "publish_date": publish_date,
#                         "author_name": author_name,
#                         "author_email": author_email,
#                         "html_content": str(credit_stories_section),
#                         "campaign_id": obj['campaign'],
#                         "deal_names": deal_names,
#                         "loan_ids": loan_ids
#                     }
#
#                     result_dict["data"].append(result)
#                     print("appending to dictionary deals with names %s", deal_names)
#                     can_break = True
