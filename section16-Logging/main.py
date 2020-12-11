import logging

from util import read_devices_info
from devclass import NetworkDeviceIOS

#====================================================================
devices_filename = 'csv-devices'

logging.basicConfig(filename='prne.log',
                    format='%(asctime)s %(message)s',
                    level=logging.INFO)

devices_list_in = read_devices_info(devices_filename)  # read CSV info for devices

logging.info('main: read %s devices from %s', len(devices_list_in), devices_filename)

# Iterate through all devices from the file, creating device objects for each
devices_list = []
for device_in in devices_list_in:

    device = NetworkDeviceIOS(device_in[0],  # Device name
                              device_in[2],  # Device IP address
                              device_in[3],  # Device username
                              device_in[4])  # Device password
    
    logging.info('main: created device: %s IP: %s', 
                                               device.name, device.ip_address)
    print ('----- device: name: ',device.name,' IP: ',device.ip_address)

    devices_list.append(device)

# Iterate through all devices, connecting and getting interface and routing info
for device in devices_list:

    session = device.connect()
    if session == 0:
        logging.error('main: unable to connect: %s, %s', 
                                               device.name, device.ip_address)
        continue

    device.set_terminal_length()
    interfaces = device.get_interfaces()
    if interfaces == 0 or len(interfaces) == 0:
        logging.error('main: get interfaces failed')
        continue

    print('--------------- device: name: ',device.name,' IP: ',device.ip_address)
    print('interfaces:', interfaces)

    logging.info('main: got interfaces data for: %s', device.name)

    routes = device.get_routes()
    if routes == 0 or len(routes) == 0:
        logging.error('main: get routes failed')
        continue

    print('--------------- device: name: ',device.name,' IP: ',device.ip_address)
    print('routes:', routes)

    logging.info('main: got routes data for: %s', device.name)