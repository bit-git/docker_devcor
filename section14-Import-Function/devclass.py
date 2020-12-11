import pexpect

#---- Class to hold information about a generic network device --------
class NetworkDevice():

    def __init__(self, name, ip, user='cisco', pw='cisco'):
        self.name = name
        self.ip_address = ip
        self.username = user
        self.password = pw

    def connect(self):
        self.session = None

    def get_interfaces(self):
        self.interfaces = '--- Base Device, does not know how to get interfaces ---'

#---- Class to hold information about an IOS network device --------
class NetworkDeviceIOS(NetworkDevice):

    def __init__(self, name, ip, user='cisco', pw='cisco'):
        NetworkDevice.__init__(self, name, ip, user, pw)

    def connect(self):
        print('--- connecting IOS: ssh '+self.ip_address)
        
        self.session = pexpect.spawn('ssh '+self.username+'@'+self.ip_address+' -p 8181', timeout=20)
        # result = self.session.expect(['Username:', pexpect.TIMEOUT])
        
        # # Successfully got username prompt
        # print '--- username:',self.username
        # self.session.sendline(self.username)
        result = self.session.expect('Password:')

        # Successfully got password prompt, logging in with password
        print('--- password:',self.password)
        self.session.sendline(self.password)
        result = self.session.expect('#')
        
        # check for failure
        if result != 0:
            print('--- Timeout or unexpected reply from device')
            return 0
        
    #---- Get interfaces from device ----------------------------------
    def get_interfaces(self):

        self.session.sendline('show ip interface brief')
        result = self.session.expect('#')

        self.interfaces = self.session.before.decode()

