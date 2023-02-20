import os
import re
import requests

from atlassian import Confluence

from download_drawio_attachments import download_drawio_attachments
from get_all_spaces import get_all_spaces


# Load configuration from external file
with open("confluence.config", "r") as f:
    config = eval(f.read())

confluence_url = config["confluence_url"]
confluence_username = config["confluence_username"]
confluence_password = config["confluence_password"]
local_dir = config["local_dir"]
spaces_to_search = config["spaces_to_search"]


def main():
    # Create a Confluence object to interact with the API
    confluence = Confluence(
        url=confluence_url, username=confluence_username, password=confluence_password, verify_ssl=False
    )

    # Get a list of all spaces
    spaces = get_all_spaces(confluence)

    # Filter the spaces we want to search
    filtered_spaces = [space for space in spaces if space["key"] in spaces_to_search]

    for space in filtered_spaces:
        # Get all the pages in the space
        all_pages = confluence.get_all_pages_from_space(space["key"])

        for page in all_pages:
            # Get all the attachments for the page
            attachments = confluence.get_attachments_from_content_id(page["id"])

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
                            with open(os.path.join(local_dir, filename), "wb") as f:
                                for chunk in response.iter_content(chunk_size=1024):
                                    f.write(chunk)


if __name__ == "__main__":
    main()
