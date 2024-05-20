#!/usr/bin/python3

import pynetbox
import pprint
import json

# Assume variables.netbox_url and variables.netbox_token are defined
import variablesGvB

# Define the base URL and your API token
base_url = variablesGvB.netbox_url
api_token = variablesGvB.netbox_token

# Initialize the pynetbox API client
nb = pynetbox.api(base_url, token=api_token)

# Define the location name and roles
location_name = "Arlandaweg (ALW)"
roles = ["Access Switch", "Distribution Switch"]

# Get the site that matches the location name
site = nb.dcim.sites.get(name=location_name)
if not site:
    print(f"No site found with name {location_name}")
    exit(1)

# Query devices in the specified site
devices = nb.dcim.devices.filter(site_id=site.id)

# Initialize the devices_index dictionary
devices_index = {}

# Function to get device and interface details from a termination
def get_termination_details(termination):
    if not termination:
        return None, None
    if termination.device:
        device = nb.dcim.devices.get(termination.device.id)
        return device.name, termination.name
    return None, None

# Limit to 5 devices
device_limit = 10
device_count = 0

# Process each device to populate the devices_index dictionary
for device in devices:
    if device_count >= device_limit:
        break

    # Check if the device role matches the specified roles
    if device.device_role.name not in roles:
        continue

    print(f"Processing device: {device.name}")  # Debugging line

    # Get the interfaces of the device
    interfaces = nb.dcim.interfaces.filter(device_id=device.id)
    print(f"Interfaces for device {device.name}: {[interface.name for interface in interfaces]}")  # Debugging line
    for record in interfaces:
        print(record)
    # Filter interfaces that have a connection
    connected_interfaces = []
    for interface in interfaces:
        print(interface)
        print(f"Checking interface {interface.name}, Cable ID: {interface.cable}")  # Debugging line
        print(f"Interface details: {interface}")  # Debugging line
        if interface.cable:
            connected_interfaces.append(interface)

    print(f"Connected interfaces for device {device.name}: {[interface.name for interface in connected_interfaces]}")  # Debugging line

    for interface in connected_interfaces:
        cable = nb.dcim.cables.get(interface.cable)

        if cable:
            termination_a = cable.a_terminations[0] if cable.a_terminations else None
            termination_b = cable.b_terminations[0] if cable.b_terminations else None

            device_a_name, interface_a_name = get_termination_details(termination_a)
            device_b_name, interface_b_name = get_termination_details(termination_b)

            print(f"Device A: {device_a_name}, Interface A: {interface_a_name}, Device B: {device_b_name}, Interface B: {interface_b_name}")  # Debugging line

            if device_a_name and interface_a_name and device_b_name and interface_b_name:
                if device_a_name not in devices_index:
                    devices_index[device_a_name] = {}
                if interface_a_name not in devices_index[device_a_name]:
                    devices_index[device_a_name][interface_a_name] = {}
                devices_index[device_a_name][interface_a_name][device_b_name] = interface_b_name

    device_count += 1

# Pretty printer for better readability of the output
pp = pprint.PrettyPrinter(indent=4)

# Print the devices_index dictionary
pp.pprint(devices_index)

# Save the devices_index dictionary to a JSON file
with open('devices_index.json', 'w') as json_file:
    json.dump(devices_index, json_file, indent=4)
