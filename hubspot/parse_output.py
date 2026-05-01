from query_output import query_output
from datetime import datetime
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs


objects = query_output['objects']
for obj in objects:
    # HTML content
    hs_email_body = obj.get('hsEmailBody')

    # LoanID's and DealID's
    loan_ids = []
    deal_names = []
    if hs_email_body:
        soup = BeautifulSoup(hs_email_body, 'html.parser')

        credit_stories_section = soup.find('div', {'id': 'commentary_div_54277'})
        # credit_stories_section = soup.find(id="Credit Stories")
        # credit_stories_content = credit_stories_section.get_text()  # Extract all the content under the "Credit_Stories" section

        if credit_stories_section:
            a_tags = credit_stories_section.find_all('a')  # Find all <a> tags
            urls = [a['href'] for a in a_tags]  # Extract href attributes from <a> tags
            for url in urls:
                parsed_url = urlparse(url)
                query_params = parse_qs(parsed_url.query)
                if query_params.get('dealName'):
                    deal_name = query_params.get('dealName', [])[0]
                    deal_names.append(deal_name)
                if query_params.get('loanID'):
                    loan_id = query_params.get('loanID', [])[0]
                    loan_ids.append(loan_id)

    # Author
    author_email = obj.get('author')
    author_name = obj.get('authorName')

    # Publish date
    publish_epoch_time = obj.get('publishDate') / 1000  # Convert ms epoch time to sec
    datetime_object = datetime.fromtimestamp(publish_epoch_time)
    publish_date = datetime_object.strftime('%Y-%m-%d %H:%M:%S')

    print(
        {
            # "html_content": hs_email_body,
            "dean_names": deal_names,
            "loan_ids": loan_ids,
            # "author_email": author_email,
            # "author_name": author_name,
            # "publish_date": publish_date
        }
    )
