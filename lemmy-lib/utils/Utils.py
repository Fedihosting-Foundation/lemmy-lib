import re

# Regex for the url https://example.com/u/username
regex = r"https:\/\/(.*)\/(u|c)\/(.*)"

def extract_username_from_actor_id(url):
    """Extracts the username from a url."""

    # Find matches
    matches = re.match(regex, url, re.MULTILINE)

    # Get the username
    username = matches.group(3)

    return username

def extract_domain_from_actor_id(url):
    """Extracts the domain from a url."""

    # Find matches
    matches = re.match(regex, url, re.MULTILINE)

    # Get the domain
    domain = matches.group(1)

    return domain
