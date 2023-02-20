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


def download_drawio_attachments(page):
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

    # Find all instances of the <ac:structured-macro> tag with ac:name="drawio"
    pattern = r'<ac:structured-macro.*ac:name="drawio".*>'
    matches = re.findall(pattern, body_storage)

    # Loop through the matching <ac:structured-macro> tags
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
for page in all_pages:
    # Get the page attachments
    response = confluence.get(f"/rest/api/content/{page['id']}/child/attachment")
    attachments = response["results"]

    # Loop through the attachments and download Draw.io files
    for attachment in attachments:
        if attachment["contentType"] == "application/vnd.jgraph.mxfile":
            download_drawio_attachments(page)
            break

