class NetworkDevice():

    def set_info(self, name, os, ip, user='cisco', pw='cisco'):
        self.name = name
        self.ip_address = ip
        self.os_type    = os
        self.username = user
        self.password = pw


#---- Function to go through devices printing them to table -----------
def print_device_info(devices_list):

    print()
    print('Name        OS-type  IP address   Username  Password')
    print('---------   -------  ----------   --------  --------')

    # Go through the list of devices, printing out values in nice format
    for device in devices_list:

        print('{0:11} {1:8} {2:12} {3:9} {4:9}'.format(device.name,
                                                       device.os_type,
                                                       device.ip_address,
                                                       device.username,
                                                       device.password))

    print()

#---- Main: read device info, then print ------------------------------

dev1 = NetworkDevice()
dev1.set_info('dev1','IOS-NX','9.9.9.9')

dev2 = NetworkDevice()
dev2.set_info('dev2','IOS-XE','8.8.8.8','chuck','secret')

print_device_info([dev1,dev2])
