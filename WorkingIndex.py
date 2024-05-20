#!/usr/bin/python3

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

# Query devices in the selected location
devices = list(nb.dcim.devices.filter(site=selected_location_slug))

# Show devices in the selected location with numbers
print(f"Devices in {locations[selected_location_index].name}:")
for i, device in enumerate(devices, start=1):
    print(f"{i}. {device}")

# Ask the user to choose a device
selected_device_index = int(input("Enter the number of the device: ")) - 1
if selected_device_index < 0 or selected_device_index >= len(devices):
    print("Invalid device number")
    exit(1)

# Retrieve the selected device
selected_device = devices[selected_device_index]

# Query interfaces of the selected device
interfaces = list(nb.dcim.interfaces.filter(device_id=selected_device.id))

# Show interfaces of the selected device with numbers
print(f"Interfaces of {selected_device}:")
for i, interface in enumerate(interfaces, start=1):
    print(f"{i}. {interface.name}")

# Ask the user to choose an interface
interface_selection = input("Enter the number or name of the interface: ")

# Retrieve the selected interface
selected_interface = None
try:
    interface_index = int(interface_selection) - 1
    if interface_index < 0 or interface_index >= len(interfaces):
        print("Invalid interface number")
        exit(1)
    selected_interface = interfaces[interface_index]
except ValueError:
    for interface in interfaces:
        if interface.name == interface_selection:
            selected_interface = interface
            break

if selected_interface is None:
    print("Invalid interface selection")
    exit(1)

# Print all information about the selected interface
print(f"Information for {selected_interface}:")
print(f"Name: {selected_interface.name}")
print(f"Type: {selected_interface.type}")
print(f"Description: {selected_interface.description}")
print(f"MAC Address: {selected_interface.mac_address}")
print(f"MTU: {selected_interface.mtu}")



# Filter cables based on the selected site
cables = nb.dcim.cables.filter(site=selected_location_slug )

'''
# Iterate over the cables and print their details
print(selected_device)
for cable in cables:
    if cable.a_terminations:
        termination_a = cable.a_terminations[0]
        if termination_a.device == selected_device:
            print(f"CableID: {cable.id}")
            print(f"Z-Side: {termination_b.device}")
            print(f"Z-Side: {termination_b.name}")
    if cable.b_terminations:
        termination_b = cable.b_terminations[0]
        if termination_b.device == selected_device:
            print(f"CableID: {cable.id}")
            print(f"Z-Side: {termination_a.device}")
            print(f"Z-Side: {termination_a.name}")

'''
print(" cables index")



# Create a dictionary to store the information
devices = {}




# Print the selected location slug for debugging
print("Selected location slug:", selected_location_slug)

# Filter cables based on the selected site
cables = nb.dcim.cables.filter(site=selected_location_slug)

# Iterate over the cables
'''
for cable in cables:
    print(cable.id)
    if cable.a_terminations:
        termination_a = cable.a_terminations[0]
        if termination_a and hasattr(termination_a, 'device'):
            devices.setdefault(termination_a.device, {})
            devices[termination_a.device].setdefault(termination_a.name, {})
        if cable.b_terminations:
            termination_b = cable.b_terminations[0]
            if termination_b and hasattr(termination_b, 'device'):
                devices.setdefault(termination_b.device, {})
                devices[termination_b.device].setdefault(termination_b.name, {})
        # Assign values
        devices[termination_a.device][termination_a.name][termination_b.device] = termination_b.name
        devices[termination_b.device][termination_b.name][termination_a.device] = termination_a.name
'''


print("-----")

for cable in cables:
    print(cable.id)
    if cable.a_terminations and cable.b_terminations:
        termination_a = cable.a_terminations[0]
        termination_b = cable.b_terminations[0]
        if hasattr(termination_a, 'device') and hasattr(termination_b, 'device'):
            devices.setdefault(termination_a.device.name, {})
            devices[termination_a.device.name].setdefault(termination_a.name, {})
            devices[termination_a.device.name][termination_a.name].setdefault(termination_b.device.name, {})
            devices[termination_a.device.name][termination_a.name][termination_b.device.name] = termination_b.name

for x in devices:
    print (devices(x))

