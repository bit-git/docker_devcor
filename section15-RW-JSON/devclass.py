import pexpect

#---- Class to hold information about a generic network device --------
class NetworkDevice():

    def __init__(self, name, ip, user='cisco', pw='cisco'):
        self.name = name
        self.ip_address = ip
        self.username = user
        self.password = pw
        self.os_type = None

    def connect(self):
        self.session = None

    def get_interfaces(self):
        self.interfaces = '--- Base Device, does not know how to get interfaces ---'

#---- Class to hold information about an IOS network device --------
class NetworkDeviceIOS(NetworkDevice):

    def __init__(self, name, ip, user='cisco', pw='cisco'):
        NetworkDevice.__init__(self, name, ip, user, pw)
        self.os_type = 'ios'

    def connect(self):
        print('--- connecting IOS: telnet '+self.ip_address)

        self.session = pexpect.spawn('telnet '+self.ip_address, timeout=20)
        result = self.session.expect(['Username:', pexpect.TIMEOUT])

        self.session.sendline(self.username)
        result = self.session.expect('Password:')

        # Successfully got password prompt, logging in with password
        self.session.sendline(self.password)
        self.session.expect('>')
 
    def get_interfaces(self):
        
        self.session.sendline('show interfaces summary')
        result = self.session.expect('>')

        self.interfaces = self.session.before


#---- Class to hold information about an IOS-XE network device --------
class NetworkDeviceXE(NetworkDevice):

    #---- Initialize --------------------------------------------------
    def __init__(self, name, ip, user='cisco', pw='cisco'):
        NetworkDevice.__init__(self, name, ip, user, pw)
        self.os_type = 'ios-xe'

    #---- Connect to device -------------------------------------------
    def connect(self):

        print('--- connecting XE: ssh '+self.username+'@'+self.ip_address)

        self.session = pexpect.spawn('ssh '+self.username+
                                     '@'+self.ip_address+' -p 8181', timeout=20)
        result = self.session.expect(['Password:', pexpect.TIMEOUT])

        # Check for failure
        if result != 0:
            print('--- Timout or unexpected reply from device')
            return 0

        # Successfully got password prompt, logging in with password
        print('--- password:',self.password)
        self.session.sendline(self.password)
        self.session.expect('#')

    #---- Get interfaces from device ----------------------------------
    def get_interfaces(self):

        self.session.sendline('show ip interface brief')
        result = self.session.expect('#')

        self.interfaces = self.session.before