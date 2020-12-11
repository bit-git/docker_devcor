from pprint import pprint

device_info = {} # Create my device_info dictionary
devices = []  
# Open the file and read in the line
file = open('devices', 'r')
for line in file:
    # Here is the main part: use the string 'split' to create a list
    # of items that are separated by commas
    device_info_list = line.strip().split(',')
    #print('read line: ', line) # Print out the line I just read

    # Now put those items from the list into our dictionary
    device_info['name'] = device_info_list[0]
    device_info['os-type'] = device_info_list[1]
    device_info['ip'] = device_info_list[2]
    device_info['username'] = device_info_list[3]
    device_info['password'] = device_info_list[4]
    
    # Print out what we have read and built so far
    print('device_info: ', device_info)
    #pprint(device_info) # Print the dictionary with nice formatting
    
    # Now append our device and its info onto our 'devices' list
    devices.append(device_info)

pprint(devices)
file.close() # Close the file since we are done with it