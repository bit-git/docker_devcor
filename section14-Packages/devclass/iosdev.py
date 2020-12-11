#======================================================================
import pexpect
from devclass.basedev import NetworkDevice

#---- Class to hold information about an IOS network device --------
class NetworkDeviceIOS(NetworkDevice):

    #---- Initialize --------------------------------------------
    def __init__(self, name, ip, user='cisco', pw='cisco'):
        NetworkDevice.__init__(self, name, ip, user, pw)

    #---- Connect to device  ------------------------------------
    def connect(self):
        print('--- connecting IOS: telnet '+self.ip_address)
        
        self.session = pexpect.spawn('telnet '+self.ip_address, timeout=20)
        # result = self.session.expect(['Username:', pexpect.TIMEOUT])
        
        # # Successfully got username prompt
        # print('--- username:',self.username)
        # self.session.sendline(self.username)
        result = self.session.expect('Password:')

        # Successfully got password prompt, logging in with password
        print('--- password:',self.password)
        self.session.sendline(self.password)
        result = self.session.expect('>')
        
        # check for failure
        if result != 0:
            print('--- Timeout or unexpected reply from device')
            return 0
 
    #---- Get interfaces from device -----------------------------
    def get_interfaces(self):
        
        self.session.sendline('show interfaces summary')
        result = self.session.expect('>')

        self.interfaces = self.session.before