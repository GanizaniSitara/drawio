import base64
import requests
import configparser
import tiktoken
from bs4 import BeautifulSoup
import boto3
import json


# Bedrock configuration
default = boto3.session.Session()
bedrock = default.client(
    service_name="bedrock-runtime",
    region_name="us-east-1",
    endpoint_url="https://bedrock-runtime.us-east-1.amazonaws.com",
)

modelId = 'anthropic.claude-v2'
accept = 'application/json'
contentType = 'application/json'


# Load configuration settings
config = configparser.ConfigParser()
config.read('C:\\Solutions\\Python\\LifeRunner\\config.ini')  # Replace with your actual config file path

# Setup Confluence authentication
confluence_email = config.get('Confluence', 'email')
confluence_api_token = config.get('Confluence', 'api_token')
auth_string = f"{confluence_email}:{confluence_api_token}"
encoded_auth_string = base64.b64encode(auth_string.encode("utf-8")).decode("utf-8")

headers = {
    "Authorization": f"Basic {encoded_auth_string}",
    "Content-Type": "application/json"
}

# Setup Confluence API URL
base_url_content = config.get('Confluence', 'base_url_content')
space_key = "NOT"

# Initialize the tokenizer
tokenizer = tiktoken.encoding_for_model("gpt-4")

def clean_html_and_extract_text(page_content):
    # Use BeautifulSoup to parse HTML content and extract text
    soup = BeautifulSoup(page_content, "html.parser")
    text = soup.get_text(separator=' ')  # Use a space as a separator for inline tags
    return text


# Function to fetch and tokenize all pages in the Confluence space
def fetch_and_tokenize_all_pages(base_url_content, space_key, headers, tokenizer):
    token_count = 0
    start_at = 0
    limit = 500
    is_last = False

    while not is_last:
        content_url = f"{base_url_content}/wiki/rest/api/content?limit={limit}&spaceKey={space_key}&start={start_at}"
        response = requests.get(content_url, headers=headers).json()

        # Tokenize the content of each page
        for page in response.get('results', []):
            page_id = page['id']
            page_content_url = f"{base_url_content}/wiki/rest/api/content/{page_id}?expand=body.storage,ancestors"
            page_response = requests.get(page_content_url, headers=headers).json()
            if page['title'] in ['Finance']:
                continue
            page_content = page_response.get('body', {}).get('storage', {}).get('value', '')
            page_content = clean_html_and_extract_text(page_content)
            tokens = tokenizer.encode(page_content)
            token_count += len(tokens)

            ancestor = page_response["ancestors"][-1]
            ancestor_title = ancestor["title"] if ancestor else ""
            print(f'Processed:"{page_response["title"]}" Parent:"{ancestor_title}"')
            continue

            body = json.dumps({
                "prompt": f"Human:{page_content} \\n\\n###\\n\\n The above is content of a webpage. Please summarize in one short sentence what the page is about."
                          f" Don't repeat any introductory phrases such as 'This page is about'. Only give the content. It can be a stub not a full sentence. \\n\\n Assistant:",
                #"prompt": "Human: This is a test \\n\\nAssistant:",
                "max_tokens_to_sample": 8149,
                "temperature": 0.1,
                "top_p": 0.9,
            })

            response = bedrock.invoke_model(body=body, modelId=modelId, accept=accept, contentType=contentType)
            response_body = json.loads(response.get('body').read())

            print(f'TokensIn:{len(tokens)} TotalIn:{token_count} Processed:"{page_response["title"]}" Summary:{response_body.get("completion")}')
        # Prepare for next iteration if there are more pages
        start_at += limit
        is_last = not response.get('_links', {}).get('next', None)

    return token_count

# Count the tokens in all pages of the Confluence space
total_token_count = fetch_and_tokenize_all_pages(base_url_content, space_key, headers, tokenizer)
print(f"Total token count: {total_token_count}")