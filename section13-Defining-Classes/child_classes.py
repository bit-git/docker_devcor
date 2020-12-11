import pexpect

#---- Class to hold information about a generic network device --------
class NetworkDevice():

    def __init__(self, name, ip, user='cisco', pw='cisco'):
        self.name = name
        self.ip_address = ip
        self.username = user
        self.password = pw

        self.interfaces = ''

    def connect(self):
        self.session = None

    def get_interfaces(self):
        self.interfaces = '--- Base Device, does not know how to get interfaces ---'

#---- Class to hold information about an IOS-XE network device --------
class NetworkDeviceIOS(NetworkDevice):

    #---- Initialize --------------------------------------------------
    def __init__(self, name, ip, user='cisco', pw='cisco'):
        NetworkDevice.__init__(self, name, ip, user, pw)

    #---- Connect to device -------------------------------------------
    def connect(self):

        print('--- connecting IOS: telnet '+self.ip_address)

        self.session = pexpect.spawn('telnet '+self.ip_address, timeout=20)
        result = self.session.expect(['Username:', pexpect.TIMEOUT])

        # Check for failure
        if result != 0:
            print('--- Timeout or unexpected reply from device')
            return None

        result = self.session.expect(['Password:', pexpect.TIMEOUT])
        # Check for failure
        if result != 0:
            print('--- Timeout or unexpected reply from device')
            return None

        # Successfully got password prompt, logging in with password
        self.session.sendline(self.password)
        self.session.expect('>')

    #---- Get interfaces from device ----------------------------------
    def get_interfaces(self):

        self.session.sendline('show interfaces summary')
        result = self.session.expect('#')

        self.interfaces = self.session.before

#---- Class to hold information about an IOS-XE network device --------
class NetworkDeviceXE(NetworkDevice):

    #---- Initialize --------------------------------------------------
    def __init__(self, name, ip, user='cisco', pw='cisco'):
        NetworkDevice.__init__(self, name, ip, user, pw)

    #---- Connect to device -------------------------------------------
    def connect(self):

        print('--- connecting XE: ssh '+self.username+'@'+self.ip_address+' -p 8181')

        self.session = pexpect.spawn('ssh '+self.username+'@'+self.ip_address+' -p 8181', timeout=20)
        # result = self.session.expect(['Username:', pexpect.TIMEOUT])

        # # Check for failure
        # if result != 0:
        #     print('--- Timeout or unexpected reply from device')
        #     return None

        result = self.session.expect(['Password:', pexpect.TIMEOUT])
        # Check for failure
        if result != 0:
            print('--- Timeout or unexpected reply from device')
            return None

        # Successfully got password prompt, logging in with password
        self.session.sendline(self.password)
        self.session.expect('#')

    #---- Get interfaces from device ----------------------------------
    def get_interfaces(self):

        #self.interfaces = '--- XE Device interface info ---'
        self.session.sendline('show interfaces summary')
        result = self.session.expect('#')
        # use decode for formating
        self.interfaces = self.session.before.decode()

#======================================================================
def read_devices_info(devices_file):

    devices_list = []

    file = open(devices_file,'r')
    for line in file:

        device_info = line.strip().split(',')

        # Create a device object with this data
        if device_info[1] == 'ios':

            device = NetworkDeviceIOS(device_info[0],device_info[2],
                                      device_info[3],device_info[4])

        elif device_info[1] == 'ios-xe':

            device = NetworkDeviceXE(device_info[0],device_info[2],
                                     device_info[3],device_info[4])

        else:
            device = NetworkDevice(device_info[0],device_info[2],
                                   device_info[3],device_info[4])

        devices_list.append(device)

    return devices_list

#====================================================================
def print_device_info(device):

    print('-------------------------------------------------------')
    print('    Device Name:      ',device.name)
    print('    Device IP:        ',device.ip_address)
    print('    Device username:  ',device.username)
    print('    Device password:  ',device.password)

    print()
    print('    Interfaces')
    print()

    print(device.interfaces)
    print('-------------------------------------------------------\n\n')

#====================================================================
# Main program: connect to device, show interface, display

devices_list = read_devices_info('sbx')

for device in devices_list:

    print('==== Device =============================================================')

    session =  device.connect()     # Connect to device

    device.get_interfaces()         # Get interface info for this device
    print_device_info(device)       # Print interface info for this device
