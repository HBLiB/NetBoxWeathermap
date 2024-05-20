#!/usr/bin/python3

import pprint
import pynetbox

# Assume variables.netbox_url and variables.netbox_token are defined
import variablesGvB

# Define the base URL and your API token
base_url = variablesGvB.netbox_url
api_token = variablesGvB.netbox_token

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

# Filter cables based on the selected site
cables = nb.dcim.cables.filter(site=selected_location_slug )


# Create a dictionary to store the information
devices = {}




# Print the selected location slug for debugging
print("Selected location slug:", selected_location_slug)

# Filter cables based on the selected site
cables = nb.dcim.cables.filter(site=selected_location_slug)

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

for x in devices:
    print(f'Device: {x}')
    for y in devices[x]:
        print(f'Interface: {y}')
        for z in devices[x][y]:
            print(f'Connected to: {z} Interface: {devices[x][y][z]}')


devicesDUP = {}
cables = nb.dcim.cables.filter(site=selected_location_slug)

# Iterate over the cables
for cable in cables:
    if cable.a_terminations and cable.b_terminations:
        termination_a = cable.a_terminations[0]
        termination_b = cable.b_terminations[0]
        if hasattr(termination_a, 'device') and hasattr(termination_b, 'device'):
            devicesDUP.setdefault(termination_a.device.name, {})
            devicesDUP[termination_a.device.name].setdefault(termination_a.name, {})
            devicesDUP[termination_a.device.name][termination_a.name].setdefault(termination_b.device.name, {})
            devicesDUP[termination_a.device.name][termination_a.name][termination_b.device.name] = termination_b.name
            devicesDUP.setdefault(termination_b.device.name, {})
            devicesDUP[termination_b.device.name].setdefault(termination_b.name, {})
            devicesDUP[termination_b.device.name][termination_b.name].setdefault(termination_a.device.name, {})
            devicesDUP[termination_b.device.name][termination_b.name][termination_a.device.name] = termination_a.name


# Pretty print the devices dictionary
pp = pprint.PrettyPrinter(indent=4)
pp.pprint(devices)

print("===")
pp = pprint.PrettyPrinter(indent=4)
pp.pprint(devicesDUP)


print(devices['gvb-clt-backfw1'])


for device in devicesDUP:
    for iface in devicesDUP[device]:
        for neighbor in devicesDUP[device][iface]:
            neighborIface = devicesDUP[device][iface][neighbor]
            print(f"Device: {device}, Interface: {iface}, Neighbor: {neighbor}, Neighbor Interface: {neighborIface}")

