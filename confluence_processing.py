import os
import urllib
import json
import re
from atlassian import Confluence
import configparser
import urllib3

# Disable SSL certificate verification and suppress warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Read the configuration values from confluence.config
config = configparser.ConfigParser()
config.read("confluence.config")

confluence_url = config.get("Confluence", "url")
confluence_username = config.get("Confluence", "username")
confluence_password = config.get("Confluence", "password")
spaces_to_search = config.get("Search", "spaces").split(",")
local_dir = config.get("Local", "directory")

# Set up the Confluence instance with SSL certificate validation disabled
confluence = Confluence(
    url=confluence_url,
    username=confluence_username,
    password=confluence_password,
    verify_ssl=False
)

# Define the REST API endpoint for finding pages with Draw.io diagrams
url = "/rest/api/content/search"

# Define the query parameters for the search
params = {
    "cql": f'type=page and text ~ "drawio" and space in ({",".join(spaces_to_search).upper()})',
    "expand": "body.storage,version",
    "limit": 1000,
    "start": 0
}

# Retrieve the search results using pagination
all_pages_with_drawio = []
while True:
    response = confluence.get(url, params=params)
    data = response
    all_pages_with_drawio.extend(data["results"])
    if data.get("_links") and data["_links"].get("next"):
        url = data["_links"]["next"]
    else:
        break

    params["start"] = data["start"] + data["size"]

# Loop through the pages that have Draw.io diagrams
for page in all_pages_with_drawio:
    # Get the Confluence space, page name, and attachment file name
    space_key = page["space"]["key"]
    page_title = page["title"]

    # Get the body storage and version information for the page
    body_storage = page["body"]["storage"]["value"]
    version = page["version"]["number"]

    # Find all instances of the <ac:structured-macro> tag with ac:name="drawio"
    pattern = r'<ac:structured-macro.*ac:name="drawio".*>'
    matches = re.findall(pattern, body_storage)
    for match in matches:
        # Extract the attachment ID from the macro tag
        attachment_id = re.search(r'name="(.*?)"', match).group(1)

        # Extract the name of the attachment from the parameters in the macro tag
        attachment_name_match = re.search(r'<ac:parameter ac:name="diagramName">(.*?)</ac:parameter>', match)
        if attachment_name_match:
            attachment_name = attachment_name_match.group(1) + ".drawio"
        else:
            attachment_name = f"{page_title}.drawio"

        # Download the Draw.io attachment file to the local directory
        attachment_url = f"{confluence_url}/download/attachments/{page['id']}/{attachment_id}?version={version}"
        local_path = os.path.join(local_dir, attachment_name)
        urllib.request.urlretrieve(attachment_url, local_path)

        # Print the Confluence space, page name, and attachment name
        print(f"Space: {space_key}, Page: {page_title}, Attachment: {attachment_name}")
