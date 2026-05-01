from query_output_new import query_output_new
from datetime import datetime
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs

# TODO : total credit stories 475 in the whole response
#  total credit stories 157 in the hs_email_body
#  total commentary_div_54277 186 in the whole response
#  do we need to include the credit stories which are not in the hs_email_body??

objects = query_output_new['objects']
hs_email = []
for obj in objects:
    # HTML content
    hs_email_body = obj.get('hsEmailBody')

    # LoanID's and DealID's
    loan_ids = []
    deal_names = []
    if hs_email_body:
        soup = BeautifulSoup(hs_email_body, 'html.parser')
        hs_email.append(soup)
print
        # keyword = "credit stories"
        # credit_stories_section = None
        #
        # # Find the section based on the keyword
        # sections = soup.find_all('div')  # You might need to adjust the class name
        # for section in sections:
        #     if keyword in section.get_text().lower():
        #         credit_stories_section = section
        #         break
        #
        # if credit_stories_section:
        #     credit_stories = credit_stories_section.find_all('p')
        #
        #     if credit_stories:
        #         for story in credit_stories:
        #             print(story.get_text())
        #     else:
        #         print("No credit stories found in the section.")
        # else:
        #     print("Credit Stories section not found.")