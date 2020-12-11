import logging
import logging.handlers

from util import read_devices_info
from devclass import NetworkDeviceIOS

#====================================================================
devices_filename = 'csv-devices'

#--- Set up logging --------------------
logger = logging.getLogger('main')
logger.setLevel(logging.INFO)

handler = logging.handlers.RotatingFileHandler('main.log',maxBytes=20000,backupCount=4)
handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))

logger.addHandler(handler)

#--- Read in devices from file ---------
devices_list_in = read_devices_info(devices_filename)  # read CSV info for all devices

logger.info('read %s devices from %s', len(devices_list_in), devices_filename)

# Iterate through all devices from the file, creating device objects for each
devices_list = []
for device_in in devices_list_in:

    device = NetworkDeviceIOS(device_in[0],  # Device name
                              device_in[2],  # Device IP address
                              device_in[3],  # Device username
                              device_in[4])  # Device password
    
    logger.info('created device: %s IP: %s', device.name, device.ip_address)

    devices_list.append(device)

# Iterate through all devices, connecting and getting interface and routing info
for device in devices_list:

    session = device.connect()
    if session == 0:
        logger.error('unable to connect: %s, %s', device.name, device.ip_address)
        continue

    device.set_terminal_length()
    interfaces = device.get_interfaces()
    if interfaces == 0 or len(interfaces) == 0:
        logger.error('get interfaces failed')
        continue
    
    print('--------------- device: name: ',device.name,' IP: ',device.ip_address)
    print('interfaces:', interfaces)

    logger.info('got interfaces data for: %s', device.name)

    routes = device.get_routes()
    if routes == 0 or len(routes) == 0:
        logger.error('get routes failed')
        continue

    print('--------------- device: name: ',device.name,' IP: ',device.ip_address)
    print('routes:', routes)


    logger.info('got routes data for: %s', device.name)