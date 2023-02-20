import os
import urllib
from atlassian import Confluence
import json
import configparser
import ssl

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
    password=confluence_password
)

# Disable SSL certificate verification for urllib
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE
urllib.request.urlopen = urllib.request.URLopener().open

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
    data = json.loads(response)
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
    attachment_filename = f"{page_title}.drawio"

    # Get the body storage and version information for the page
    body_storage = page["body"]["storage"]["value"]
    version = page["version"]["number"]

    # Find the Draw.io attachment ID in the body storage
    start_tag = '<ac:structured-macro ac:name="drawio">'
    end_tag = '</ac:structured-macro>'
    start_index = body_storage.find(start_tag)
    end_index = body_storage.find(end_tag, start_index)
    drawio_macro = body_storage[start_index:end_index]
    attachment_id = drawio_macro.split("name=|")[1].split("|")[0]

    # Download the Draw.io attachment file to the local directory
    attachment_url = f"{confluence_url}/download/attachments/{page['id']}/{attachment_id}?version={version}"
    local_path = os.path.join(local_dir, attachment_filename)
    urllib.request.urlretrieve(attachment_url, local_path)

    # Print the Confluence space, page name, and attachment file name
    print(f"Space: {space_key}, Page: {page_title}, Attachment: {attachment_filename}")
