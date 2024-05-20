#!/usr/bin/python3

import requests
import variablesGvB
import logging
import pynetbox
import pprint


logging.basicConfig(level=logging.DEBUG)

NETBOX_URL = variablesGvB.netbox_url
NETBOX_TOKEN = variablesGvB.netbox_token

nb = pynetbox.api(url=NETBOX_URL, token=NETBOX_TOKEN)

# Query all tenants
tenants = nb.tenancy.tenants.all()

# Print the list of tenants
for tenant in tenants:
    print(f"ID: {tenant.id}, Name: {tenant.name}, Slug: {tenant.slug}")

# Define the location and roles
location_name = "Arlandaweg (ALW)"
roles = ["Access Switch", "Distribution Dwitch"]

# Get the site that matches the location name
site = nb.dcim.sites.get(name=location_name)
if not site:
    print(f"No site found with name {location_name}")
    exit(1)


# Get the devices that match the roles and are in the site
devices = nb.dcim.devices.filter(site_id=site.id, role__in=roles)

# Print the list of devices
#for device in devices:
#    print(f"ID: {device.id}, Name: {device.name}, Role: {device.device_role.name}, Site: {device.site.name}")



device_name = "qalw1b2-1 Arlandaweg"
# Get the device by name
device = nb.dcim.devices.get(name=device_name)
if not device:
    print(f"No device found with name {device_name}")
    exit(1)


# Get the interfaces of the device
interfaces = nb.dcim.interfaces.filter(device_id=device.id)

# Filter interfaces that have a connection
connected_interfaces = [interface for interface in interfaces if interface.cable]

# Pretty printer for better readability of the output
pp = pprint.PrettyPrinter(indent=4)

# Function to get device and interface details from a termination
def get_termination_details(termination):
    if not termination:
        return None, None
    if termination.device:
        device = nb.dcim.devices.get(termination.device.id)
        return device.name, termination.name
    return None, None

# Initialize the devices_index dictionary
devices_index = {}

# Populate the devices_index dictionary with cable details
for interface in connected_interfaces:
    cable = nb.dcim.cables.get(interface.cable)
    
    # Get terminations details
    termination_a = cable.a_terminations[0] if cable.a_terminations else None
    termination_b = cable.b_terminations[0] if cable.b_terminations else None
    
    device_a_name, interface_a_name = get_termination_details(termination_a)
    device_b_name, interface_b_name = get_termination_details(termination_b)
    
    if device_a_name and interface_a_name and device_b_name and interface_b_name:
        if device_a_name not in devices_index:
            devices_index[device_a_name] = {}
        if interface_a_name not in devices_index[device_a_name]:
            devices_index[device_a_name][interface_a_name] = {}
        devices_index[device_a_name][interface_a_name][device_b_name] = interface_b_name

# Print the devices_index dictionary
pp.pprint(devices_index)