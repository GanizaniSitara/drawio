import os
import re
import requests

from atlassian import Confluence


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
