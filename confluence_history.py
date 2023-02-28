import configparser
import datetime
import io
import requests
import matplotlib.pyplot as plt
from atlassian import Confluence

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Read the configuration details from the confluence.config file
config = configparser.ConfigParser()
config.read('confluence.config')

config = configparser.ConfigParser()
config.read("confluence.config")
confluence_url = config.get("Confluence","url")
confluence_username = config.get("Confluence", "username")
confluence_password = config.get("Confluence", "password")
spaces_to_search = config.get("Search","spaces").split(",")
publish_space = config.get("Confluence","publish_space")

# Create a Confluence object with the specified URL, username, and password
confluence = Confluence(url=confluence_url,
                        username=confluence_username,
                        password=confluence_password,
                        verify_ssl=False)

# Define an empty list to store the generated graphs
graphs = []
page_counts = {}

# Generate a frequency graph for each space
for space_key in spaces_to_search:
    # Retrieve all pages from the specified space using the Confluence API
    pages = confluence.get_all_pages_from_space(space_key, expand='version,history')

    # Extract the update dates for each page and count the number of pages updated on each day
    update_dates = [datetime.datetime.strptime(page['version']['when'][:10], '%Y-%m-%d').date() for page in pages]
    update_counts = {}
    for update_date in update_dates:
        if update_date in update_counts:
            update_counts[update_date] += 1
        else:
            update_counts[update_date] = 1

    # Create a frequency graph of the page updates using Matplotlib
    fig, ax = plt.subplots(figsize=(10, 1.2))

    x_values = list(update_counts.keys())
    y_values = list(update_counts.values())

    ax.bar(x_values, y_values)

    # Set the x-axis label to "Update Date"
    # ax.set_xlabel("Update Date")

    # Set the y-axis label to "Number of Page Updates"
    ax.set_ylabel("# Updates")

    # Set the title of the graph to "Page Update Frequency"
    ax.set_title(f"{space_key} - Current Version Latest Updates")

    # Rotate the x-axis labels for better readability
    plt.xticks(rotation=45)

    # Adjust the layout of the graph to fit the specified size
    plt.tight_layout()
    plt.subplots_adjust(bottom=0.25)

    # Save the graph to a binary buffer
    plt.savefig(f"PageUpdateFrequency{space_key}.png", format='png', dpi=100, bbox_inches='tight')

    graphs.append((space_key, f"PageUpdateFrequency{space_key}.png"))

    # Count the number of pages in the space
    page_counts[space_key] = len(pages)

page_title="Update History"

# Check if page already exists
existing_page_id = confluence.get_page_id(space=publish_space, title=page_title)

# If page exists, update it; otherwise, create a new page
if existing_page_id:
    page_id = existing_page_id
    # page_version = confluence.get_page_by_id(page_id, expand='version')['version']['number']
    confluence.remove_page(page_id)

page = confluence.create_page(
    space=publish_space,
    title=page_title,
    body='')

page_id = page['id']



# Generate the HTML content for the new Confluence page
html = "<h1>Page Update Frequency</h1>"
html += "<ul>"

for space_key, graph in graphs:
    # Upload the graph as an attachment to the Confluence server
    attachment_url = confluence.attach_file(graph, page_id=page_id)

    # Calculate the percentage of pages updated within the last year
    one_year_ago = datetime.datetime.now() - datetime.timedelta(days=365)
    updated_pages = [page for page in pages if datetime.datetime.strptime(page['version']['when'][:10], '%Y-%m-%d').date() >= one_year_ago.date()]
    if len(pages) > 0:
        percentage_updated = len(updated_pages) / len(pages) * 100
    else:
        percentage_updated = 0

    # Create a hyperlink to the space with the corresponding URL and key
    space_url = f"{confluence_url}/spaces/{space_key}"
    space_link = f"<a href=\"{space_url}\">{space_key}</a>"

    # Add the space, page count, and graph to the HTML content
    html += f"<li><h2>{space_link}</h2>"
    html += f"<p>Total number of pages: {page_counts[space_key]}</p>"
    html += f"<p>Percentage of pages updated within the last year: {percentage_updated:.2f}%</p>"
    html += f"<ac:image><ri:attachment ri:filename='PageUpdateFrequency{space_key}.png' ri:version-at-save='1' ri:content-type='image/png' /></ac:image></li>"

html += "</ul>"

# Create a new Confluence page with the list of spaces and frequency graphs
title = "Page Update Frequency"
confluence.update_page(
    title=page_title,
    page_id=page_id,
    body=html,
    parent_id=None,
    type='page',
    representation='storage',
    minor_edit=True
)