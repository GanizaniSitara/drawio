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

import requests

import requests


def download_drawio_attachments(page, attachments):
    # Get the Confluence space and page name
    space_key = page.get("space", {}).get("key")
    if not space_key:
        # If the page does not have a space property, extract the space key from the container link
        container_link = page["_expandable"]["container"]
        space_key = container_link.split("/")[-1]

    page_title = page["title"]

    # Get the body storage and version information for the page
    body_storage = page["body"]["storage"]["value"]
    version = page["version"]["number"]

    # Loop through the attachments and download Draw.io files
    for attachment in attachments:
        attachment_name = attachment["title"]

        # Check if the attachment is a Draw.io file by searching for the <ac:structured-macro> pattern
        pattern = r'<ac:structured-macro.*ac:name="drawio".*>'
        if re.search(pattern, body_storage):
            attachment_id = attachment["id"]
            download_link = attachment["_links"]["download"]

            # Download the Draw.io attachment file to the local directory
            attachment_url = f"{confluence_url}{download_link}?version={version}"
            local_path = os.path.join(local_dir, attachment_name)
            with requests.get(attachment_url, auth=(confluence_username, confluence_password), stream=True,
                              verify=False) as response:
                response.raise_for_status()
                with open(local_path, "wb") as f:
                    for chunk in response.iter_content(chunk_size=1024):
                        f.write(chunk)

            # Print the Confluence space, page name, and attachment name
            print(f"Space: {space_key}, Page: {page_title}, Attachment: {attachment_name}")


# Retrieve all pages in the specified spaces
all_pages = []
for space in spaces_to_search:
    response = confluence.get(
        f"/rest/api/content?spaceKey={space}&limit=1000&expand=body.storage,version,attachments,ancestors.space")
    all_pages.extend(response["results"])
    while "next" in response["_links"]:
        response = confluence.get(response["_links"]["next"])
        all_pages.extend(response["results"])

# Loop through the pages and check them for attachments
# Loop through the pages and check them for attachments
for page in all_pages:
    # Get the page attachments
    response = confluence.get(f"/rest/api/content/{page['id']}/child/attachment")
    attachments = response["results"]

    # Download Draw.io files for the page
    download_drawio_attachments(page, attachments)



