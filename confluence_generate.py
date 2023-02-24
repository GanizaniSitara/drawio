import os
import json
import shutil
import datetime
from atlassian import Confluence
import base64

metadata_dir = 'metadata'

data = []

# Iterate over all subfolders of metadata directory
for subdir, _, files in os.walk(metadata_dir):
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

# Generate HTML table
table_html = '<table><tr>'

for i, item in enumerate(data_sorted):
    # Add a new row after every second item
    if i > 0 and i % 2 == 0:
        table_html += '</tr><tr>'

    # Add cell for current item
    table_html += f'<td style="text-align: center;"><p>{item["edit date"]}</p><p>{item["author"]}</p><img src="data:image/png;base64,{base64.b64encode(open(item["path"], "rb").read()).decode()}" /></td>'

# Close table tag
table_html += '</tr></table>'

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
    confluence.update_page(
        page_id=existing_page_id,
        title=page_title,
        body=table_html)
else:
    confluence.create_page(
        space_key=space_key,
        title=page_title,
        body=table_html)
