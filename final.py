#!/usr/bin/env python3


import json
import numpy as np
import numpy as np
import time
import os
import sys
import re
from pyvis.network import Network
import networkx as nx
import pprint
import pynetbox
import re
import variablesGvB as variables

# Define the base URL and your API token
base_url = variables.netbox_url
api_token = variables.netbox_token

# Initialize the pynetbox API client
nb = pynetbox.api(base_url, token=api_token)


### To debug only 1 site, Remove this PART LATER
# Query all locations
locations = list(nb.dcim.sites.all())

# Show all locations with numbers
print("Locations:")
for i, location in enumerate(locations, start=1):
    print(f"{i}. {location.name}")

# Ask the user to choose a location
selected_location_index = int(input("Enter the number of the location: ")) - 1
if selected_location_index < 0 or selected_location_index >= len(locations):
    print("Invalid location number")
    exit(1)


# Retrieve the selected location's slug
selected_location_slug = locations[selected_location_index].slug

# Create a dictionary to store the information
devices = {}

# Print the selected location slug for debugging
print("Selected location slug:", selected_location_slug)

# Filter cables based on the selected site
cables = nb.dcim.cables.filter(site=selected_location_slug)

for cable in cables:
    print(vars(cable))

