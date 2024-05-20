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

# Assume variables.netbox_url and variables.netbox_token are defined
import variables

# Define the base URL and your API token
base_url = variables.netbox_url
api_token = variables.netbox_token

# Initialize the pynetbox API client
nb = pynetbox.api(base_url, token=api_token)

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
#cables = nb.dcim.cables.all()
# Iterate over the cables


for cable in cables:
    if cable.a_terminations and cable.b_terminations:
        termination_a = cable.a_terminations[0]
        termination_b = cable.b_terminations[0]
        if hasattr(termination_a, 'device') and hasattr(termination_b, 'device'):
            devices.setdefault(termination_a.device.name, {})
            devices[termination_a.device.name].setdefault(termination_a.name, {})
            devices[termination_a.device.name][termination_a.name].setdefault(termination_b.device.name, {})
            devices[termination_a.device.name][termination_a.name][termination_b.device.name] = termination_b.name

print("received cables")
#net = Network(height="100%", width="100%",bgcolor="#222222", font_color="white",directed=True,heading=f"GvB {selected_location_slug} Weathermap")
#net = Network(height="100%", width="100%",bgcolor="#222222", font_color="white",directed=True,heading="NeP CP NL WeatherMap")
net = Network(height="100%", width="100%",bgcolor="#222222", font_color="white",directed=True,heading=f"GvB {selected_location_slug} Weathermap")

print("itirating devices")

#net = Network()
for x in devices:
    if x is not None:
        try:
            # Query a device by its name
            device_name = x
            device = nb.dcim.devices.get(name=device_name)
            site = device.site
            grouP = site.name
            # Get the device role tag if the device is found
            print(x)
            print(device.device_role.slug)
            if device:
                device_role_tag = device.device_role.slug
                if device_role_tag == "distribution-switch":
                    color2 = "blue"
                    massV = 10
                    group=grouP
                elif device_role_tag == "access-switch":
                    color2 = "green"
                    massV = 1
                    group=grouP
                elif device_role_tag == "patchpaneel":
                    color2 = "red"
                    massV = 1
                    group=grouP
                elif device_role_tag == "firewall":
                    color2 = "red"
                    massV = 1
                    group=grouP
                elif device_role_tag == "router":
                    color2 = "blue"
                    massV = 1
                    group=grouP
                elif device_role_tag == "wdm-mux":
                    color2 = "black"
                    massV = 1
                    group=grouP
                elif device_role_tag == "wdm-olt":
                    color2 = "orange"
                    massV = 1
                    group=grouP
                elif device_role_tag == "core-switch":
                    color2 = "navy"
                    massV = 1
                    group=grouP
                elif device_role_tag == "cpe":
                    color2 = "brown"
                    massV = 1
                    group=grouP
                elif device_role_tag == "access-point":
                    color2 = "cyan"
                    massV = 1
                    group=grouP
                elif device_role_tag == "odf":
                    color2 = "magenta"
                    massV = 1
                    group=grouP
                elif device_role_tag == "oob":
                    color2 = "yellow"
                    massV = 1
                    group=grouP
                else:
                    massV = 1
                    color2 = "green"
                    print(device_role_tag)
                net.add_node(x, label=x,shape= "box", color=color2,group=grouP, borderWidth=5,mass=1,x=-1600,y=-600)
            else:
                print(f"Device named '{device_name}' not found.")
        except Exception as e:
            print(f"Error: {e}")


print("itirating keys")

for x in devices.keys():
    print(x)
    try:
        if x != None:
            for iface in devices[x]:
                for neighbor in devices[x][iface]:
                    if neighbor != None:
                        neighborIface = devices[x][iface][neighbor]
                        if neighbor not in devices.keys():
                            net.add_node(neighbor, label=neighbor,shape= "box", color="red",borderWidth=5,mass=1,x=-1600,y=-600)
                            utilLabel =  "A:" + x + ":" + iface +"\n""Z:" + neighbor + ":" + neighborIface +"\n"
                            net.add_edge(x, str(neighbor), size=1, title=utilLabel, color="red", font='5px arial black',arrows='None')
                        else:                
                            utilLabel =  "A:" + x + ":" + iface +"\n""Z:" + neighbor + ":" + neighborIface +"\n"
                            net.add_edge(x, str(neighbor), size=1, title=utilLabel, color="red", font='5px arial black',arrows='None')
    except Exception as e:
        print(f"Error: {e}")



net.toggle_physics(True)

net.set_edge_smooth('dynamic')

net.show_buttons(filter_=['physics'])
net.force_atlas_2based()

net.show('nx.html',notebook=False)


