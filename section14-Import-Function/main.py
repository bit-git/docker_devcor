from util import read_devices_info
from util import print_device_info

#====================================================================
# Main program: connect to device, show interface, display

devices_list = read_devices_info('sbx')

for device in devices_list:

    print('==== Device =============================================================')

    device.connect()
    device.get_interfaces()
    print_device_info(device)