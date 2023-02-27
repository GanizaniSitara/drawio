import configparser
import datetime
import io
import requests
import matplotlib.pyplot as plt
from atlassian import Confluence

# Read the configuration details from the confluence.config file
config = configparser.ConfigParser()
config.read('confluence.config')

config = configparser.ConfigParser()
config.read("confluence.config")
confluence_url = config.get("Confluence","url")
confluence_username = config.get("Confluence", "username")
confluence_password = config.get("Confluence", "password")
publish_space = config.get("Confluence","publish_space")

# Create a Confluence object with the specified URL, username, and password
confluence = Confluence(url=confluence_url, username=confluence_username, password=confluence_password)

# Set the parent page ID for the new page to be created
parent_id = "12345"  # replace with the actual parent page ID

# Set the keys for the spaces to retrieve page updates from
space_keys = ["space1", "space2", "space3"]  # replace with the actual space keys

# Define an empty list to store the generated graphs
graphs = []

# Generate a frequency graph for each space
for space_key in space_keys:
    # Retrieve all pages from the specified space using the Confluence API
    pages = confluence.get_all_pages_from_space(space_key)

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
    ax.set_xlabel("Update Date")

    # Set the y-axis label to "Number of Page Updates"
    ax.set_ylabel("Number of Page Updates")

    # Set the title of the graph to "Page Update Frequency"
    ax.set_title(f"{space_key.capitalize()} - Page Update Frequency")

    # Rotate the x-axis labels for better readability
    plt.xticks(rotation=45)

    # Adjust the layout of the graph to fit the specified size
    plt.tight_layout()
    plt.subplots_adjust(bottom=0.25)

    # Save the graph to a binary buffer
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png', dpi=100, bbox_inches='tight')
    buffer.seek(0)

    # Append the binary buffer to the list of graphs
    graphs.append((space_key, buffer))

# Create a new Confluence page with a list of the spaces and the corresponding frequency graphs
html = "<h1>Page Update Frequency</h1>"
html += "<ul>"

for space_key, graph in graphs:
    # Upload the graph as an attachment to the Confluence server
    attachment_url = confluence.attach_file(graph, space_key=space_key, filename="page_update_frequency.png")

    # Create a hyperlink to the space with the corresponding URL and key
    space_url = f"{confluence_url}/spaces/{space_key}"
    space_link = f"<a href=\"{space_url}\">{space_key.capitalize()}</a>"

    # Add the space and graph to the HTML content
    html += f"<li><h2>{space_link}</h2>"
    html += f"<img src=\"{attachment_url}\" alt=\"{space_key} - Page Update Frequency\"></li>"

html += "</ul>"

#Define the title and content for the new Confluence page
title = "Page Update Frequency"
content = html

# Create the new Confluence page with the specified title and content
page_data = {
    "type": "page",
    "title": title,
    "space": {"key": publish_space},
    "body": {"storage": {"value": content, "representation": "storage"}},
}
confluence.create_page(page_data)

