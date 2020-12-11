from util.readdevs import read_devices_info
from util.printdev import print_device_info

#====================================================================
# Main program: connect to device, show interface, display

devices_list = read_devices_info('devices')

for device in devices_list:

    print('==== Device =============================================================')

    device.connect()
    device.get_interfaces()
    print_device_info(device)