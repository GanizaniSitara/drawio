import configparser
import json
import os
import re
import requests
import sys
import html
#import timeit

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

from atlassian import Confluence

config = configparser.ConfigParser()
config.read("confluence.config")
confluence_url = config.get("Confluence","url")
confluence_username = config.get("Confluence", "username")
confluence_password = config.get("Confluence", "password")
local_dir = config.get("Local","directory")
local_dir_diagrams = config.get("Local","diagrams")
local_dir_images = config.get("Local","images")
local_dir_metadata = config.get("Local","metadata")
spaces_to_search = config.get("Search","spaces").split(",")
publish_space = config.get("Confluence","publish_space")


def download_drawio_attachments(confluence, page, attachments, local_dir):
    # Get the Confluence space and page name
    space_key = page.get("space", {}).get("key")
    if not space_key:
        # If the page does not have a space property, extract the space key from the container link
        container_link = page["_expandable"]["container"]
        space_key = container_link.split("/")[-1]

    # Create a folder for the space key if it does not exist
    space_dir = os.path.join(local_dir, space_key)
    if not os.path.exists(space_dir):
        os.mkdir(space_dir)

    for attachment in attachments:
        if attachment["metadata"]["mediaType"] == "application/vnd.jgraph.mxfile":
            # Download the draw.io attachment
            attachment_url = attachment["_links"]["download"]
            response = confluence.get(attachment_url, not_json_response=True, stream=True)

            # Get the name of the draw.io diagram
            page_body = page["body"]["storage"]["value"]
            start_tag = '<ac:structured-macro.*ac:name="drawio".*>'
            end_tag = "</ac:structured-macro>"
            matches = re.findall(f"{start_tag}.*?{end_tag}", page_body, re.DOTALL)

            for match in matches:
                drawio_name_match = re.search('<ac:parameter ac:name="diagramName">(.*?)</ac:parameter>', match)
                if drawio_name_match:
                    drawio_name = drawio_name_match.group(1)
                    filename = f"{drawio_name}.drawio"

                    # Save the draw.io attachment to the local directory
                    with open(os.path.join(space_dir, filename), "wb") as f:
                        for chunk in response.iter_content(chunk_size=1024):
                            f.write(chunk)


def main():

    # Create a Confluence instance
    confluence = Confluence(
        url=confluence_url,
        username=confluence_username,
        password=confluence_password,
        verify_ssl=False
    )

    # Get all pages in the specified spaces

    for space_key in spaces_to_search:
        all_pages = []
        start = 0
        limit = 1000

        while True:
            response = confluence.get_all_pages_from_space(space_key, start=start, limit=limit, expand="body.storage")

            if not response.get("results"):
                break

            all_pages.extend(response["results"])
            start += limit

        # Download draw.io attachments from the pages
        for page in all_pages:
            attachments_url = page["_links"]["attachments"]
            attachments_response = confluence.get(attachments_url)

            # Check if the page has any attachments and download draw.io attachments
            attachments = attachments_response.get("results", [])
            if attachments:
                download_drawio_attachments(confluence, page, attachments, local_dir)
                print(f"Downloaded draw.io attachments from '{page['title']}' in '{page['space']['name']}' space")


if __name__ == "__main__":
    main()
