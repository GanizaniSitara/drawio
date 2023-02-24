import configparser
import os
import json
import shutil
from datetime import datetime
from atlassian import Confluence
import base64

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

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

data = []

# Iterate over all subfolders of metadata directory
for subdir, _, files in os.walk(local_dir_metadata):
    for file in files:
        if file.endswith('.json'):
            # Read JSON file and extract data
            json_path = os.path.join(subdir, file)
            with open(json_path, 'r') as f:
                json_data = json.load(f)
                name = json_data['title']
                date = json_data['version']['when']
                author = json_data['version']['by']['displayName']

            # Concatenate images to parent of metadata directory
            image_path = os.path.join(local_dir_images,json_data["space"]["key"], f'{name}.png')

            # Add data to list
            data.append({'name': name, 'path': image_path, 'author': author, 'date': date})

# Sort data by edit date
data_sorted = sorted(data, key=lambda x: datetime.strptime(x['date'], '%Y-%m-%dT%H:%M:%S.%f%z'), reverse=True)

# Create Confluence page
confluence = Confluence(
    url=confluence_url,
    username=confluence_username,
    password=confluence_password,
    verify_ssl=False)


page_title = 'Overview'

# Check if page already exists
existing_page_id = confluence.get_page_id(space=publish_space, title=page_title)

# If page exists, update it; otherwise, create a new page
if existing_page_id:
    page_id = existing_page_id
    page_version = confluence.get_page_by_id(page_id, expand='version')['version']['number']
else:
    page = confluence.create_page(
        space=publish_space,
        title=page_title,
        body='')

    page_id = page['id']

# Upload images and attach them to page
for item in data_sorted:
    attachment_id = confluence.attach_file(
        filename=item["path"],
        name=item["name"],
        content_type='image/png',
        page_id=page_id)

    item['attachment_id'] = attachment_id

# Generate HTML table
table_html = '<table><tr>'

for i, item in enumerate(data_sorted):
    # Add a new row after every second item
    if i > 0 and i % 2 == 0:
        table_html += '</tr><tr>'

    # Add cell for current item
    table_html += f'<td style="text-align: center;"><p>{item["date"]}</p><p>{item["author"]}</p><ac:image ac:thumbnail="true"><ri:attachment ri:filename="{os.path.basename(item["path"])}" ri:version-at-save="1" ri:content-type="image/png" /><ac:plain-text-body><![CDATA[]]></ac:plain-text-body></ac:image></td>'

# Close table tag
table_html += '</tr></table>'



# Update or create page with new content
confluence.update_page(
    page_id=page_id,
    title=page_title,
    body=table_html,
    version={'number':page_version + 1},
    minor_edit=True,
    space=publish_space)

