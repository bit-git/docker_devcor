#---- Class to hold information about a generic network device --------
class NetworkDevice():

    def __init__(self, name, ip, user='cisco', pw='cisco'):
        self.name = name
        self.ip_address = ip
        self.username = user
        self.password = pw
        self.os_type = 'unknown'

#---- Class to hold information about an IOS-XE network device --------
class NetworkDeviceIOS(NetworkDevice):

    def __init__(self, name, ip, user='cisco', pw='cisco'):
        NetworkDevice.__init__(self, name, ip, user, pw)
        self.os_type = 'ios'

#---- Class to hold information about an IOS-XR network device --------
class NetworkDeviceXR(NetworkDevice):

    def __init__(self, name, ip, user='cisco', pw='cisco'):
        NetworkDevice.__init__(self, name, ip, user, pw)
        self.os_type = 'ios-xr'

#---- Function to read device information from file -------------------
def read_device_info(devices_file):

    devices_list = []

    # Read in the devices from the file
    file = open(devices_file,'r')
    for line in file:

        device_info = line.strip().split(',') # Get device info into list

        # Create a device object with this data
        if device_info[1] == 'ios':

            device = NetworkDeviceIOS(device_info[0],device_info[2],
                                      device_info[3],device_info[4])

        elif device_info[1] == 'ios-xr':

            device = NetworkDeviceXR(device_info[0],device_info[2],
                                     device_info[3],device_info[4])

        else:
            continue  # go to the next device in the file

        devices_list.append(device) # add this device object to list

    file.close() # Close the file since we are done with it
    return devices_list

#---- Function to go through devices printing them to table -----------
def print_device_info(devices_list):

    print()
    print('Name     OS-type  IP address       Username  Password')
    print('------   -------  --------------   --------  --------')

    # Go through the list of devices, printing out values in nice format
    for device in devices_list:

        print('{0:8} {1:8} {2:16} {3:8} {4:8}'.format(device.name,
                                                      device.os_type,
                                                      device.ip_address,
                                                      device.username,
                                                      device.password))

    print()

#---- Main: read device info, then print ------------------------------

devices = read_device_info('devices')
print_device_info(devices)