from atlassian import Confluence

# Load configuration from external file
with open("confluence.config", "r") as f:
    config = eval(f.read())

confluence_url = config["confluence_url"]
confluence_username = config["confluence_username"]
confluence_password = config["confluence_password"]


def get_all_spaces():
    # Create a Confluence instance
    confluence = Confluence(
        url=confluence_url,
        username=confluence_username,
        password=confluence_password,
        verify_ssl=False,
    )

    # Construct the API endpoint URL for retrieving all spaces
    url = f"{confluence_url}/rest/api/space"

    # Send a GET request to the API endpoint and retrieve the response
    response = confluence.get(url)

    # If the response is successful, extract the space keys from the JSON data
    if response.ok:
        data = response.json()
        space_keys = [space["key"] for space in data["results"]]
        return space_keys
    else:
        response.raise_for_status()
