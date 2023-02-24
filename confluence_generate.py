import configparser
import os
import json
import shutil
import datetime
from atlassian import Confluence
import base64

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

config = configparser.ConfigParser()
config.read("confluence.config")

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
            image_path = os.path.join(subdir, f'{name}.png')
            if os.path.exists(image_path):
                dest_dir = os.path.abspath(os.path.join(subdir, os.pardir))
                dest_path = os.path.join(dest_dir, f'{name}.png')
                shutil.copyfile(image_path, dest_path)

            # Add data to list
            data.append({'name': name, 'path': dest_path, 'author': author, 'edit date': date})

# Sort data by edit date
data_sorted = sorted(data, key=lambda x: datetime.datetime.strptime(x['edit date'], '%Y-%m-%d'), reverse=True)

# Create Confluence page
confluence = Confluence(
    url='https://your-confluence-site.com',
    username='your-username',
    password='your-password')

page_title = 'Overview'
space_key = 'SpaceKey'

# Check if page already exists
existing_page_id = confluence.get_page_id(space_key, title=page_title)

# If page exists, update it; otherwise, create a new page
if existing_page_id:
    page_id = existing_page_id
else:
    page = confluence.create_page(
        space_key=space_key,
        title=page_title,
        body='')

    page_id = page['id']

# Upload images and attach them to page
for item in data_sorted:
    image_path = item['path']

    with open(image_path, 'rb') as f:
        image_data = f.read()

    attachment_id = confluence.attach_file(
        filename=os.path.basename(image_path),
        file=image_data,
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
    table_html += f'<td style="text-align: center;"><p>{item["edit date"]}</p><p>{item["author"]}</p><ac:image ac:thumbnail="true"><ri:attachment ri:filename="{os.path.basename(item["path"])}" ri:version-at-save="1" ri:content-type="image/png" /><ac:plain-text-body><![CDATA[]]></ac:plain-text-body></ac:image></td>'

# Close table tag
table_html += '</tr></table>'

# Update or create page with new content
confluence.update_page(
    page_id=page_id,
    title=page_title,
    body=table_html)

