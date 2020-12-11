print() # Print heading
print('Devices with bad software versions')
print('==================================')

# Set Variable for current version comparison used in Step 4

current_version = 'Version 5.3.1'

# Read all lines of device information from file
file = open('devices','r')
for line in file:

    device_info_list = line.strip().split(',') # Get device info into list
    
    # Put device information into dictionary for this one device
    device_info = {} # Create the inner dictionary of device info
    device_info['name'] = device_info_list[0]
    device_info['ip'] = device_info_list[1]
    device_info['version'] = device_info_list[2]

    # Print out what we have read and built so far
    #print('device_info: ', device_info)

    # If the version doesn't match our 'current version', print out warning
    if device_info['version'] != current_version:
        print('      Device:', device_info['name'], '   Version:', device_info['version'])

print() # Print final blank line

file.close() # Close the file since we are done with it