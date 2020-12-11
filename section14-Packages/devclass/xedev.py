#======================================================================
import pexpect
from devclass.basedev import NetworkDevice

#---- Class to hold information about an IOS-XE network device --------
class NetworkDeviceXE(NetworkDevice):

    #---- Initialize --------------------------------------------------
    def __init__(self, name, ip, user='cisco', pw='cisco'):
        NetworkDevice.__init__(self, name, ip, user, pw)

    #---- Connect to device -------------------------------------------
    def connect(self):

        print('--- connecting: ssh '+self.username+'@'+self.ip_address)

        self.session = pexpect.spawn('ssh '+self.username+
                                     '@'+self.ip_address+' -p 8181', timeout=20)
        result = self.session.expect(['Password:', pexpect.TIMEOUT])

        # Check for failure
        if result != 0:
            print('--- Timeout or unexpected reply from device')
            return 0

        # Successfully got password prompt, logging in with password
        print('--- password:',self.password)
        self.session.sendline(self.password)
        self.session.expect('#')

    #---- Get interfaces from device ----------------------------------
    def get_interfaces(self):

        self.session.sendline('show ip interface brief')
        result = self.session.expect('#')

        self.interfaces = self.session.before.decode()
