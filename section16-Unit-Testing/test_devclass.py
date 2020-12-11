import unittest
from pprint import pprint

from devclass import NetworkDeviceIOS

# Device information for the actual device we will be testing against
device_name = 'test-device'
device_ip   = '10.30.30.1'
device_user = 'cisco'
device_pw   = 'cisco'

class TestDevice(unittest.TestCase):


    def setUp(self):

        # Create device for testing login, connectivity, etc.
        self.device = NetworkDeviceIOS(device_name,device_ip,device_user,device_pw)

    def test_attributes(self):

        print('\n**** Testing device object creation and values ****')

        # Test to make sure that the device object has correct values as set up
        self.assertEqual(self.device.name, device_name, "Incorrect device name")
        self.assertEqual(self.device.ip_address, device_ip, "Incorrect IP address")
        self.assertEqual(self.device.username, device_user, "Incorrect username")
        self.assertEqual(self.device.password, device_pw, "Incorrect password")

    def test_connect(self):

        print('\n**** Testing device object connectivity to real device ****')

        # Test that we can connect to the device (login)
        session = self.device.connect()
        self.assertNotEqual(session, 0, "Failed connection to device")

        self.device.disconnect()  # Clean up the session


    def test_show_interfaces(self):

        print('\n**** Testing device show interfaces command ****')

        # First must connect to the device
        session = self.device.connect()
        self.assertNotEqual(session, 0, "Failed connection to device")

        # Set terminal length to 0 for long replies
        self.assertTrue(self.device.set_terminal_length())

        # Run show interfaces command
        intf_output = self.device.get_interfaces()

        # Test the command ran successfully
        self.assertNotEqual(intf_output, 0, "Failed show interfaces command")

        # Test the data returned from the command
        # Note we test for 'Loopback', which will be present always
        self.assertNotEqual(len(intf_output), 0, "Show interfaces: no data")
        self.assertNotEqual(intf_output.find('Loopback'), -1, 
                                               "Show interfaces: incorrect data")

        self.device.disconnect()  # Clean up the session

    def test_show_routes(self):

        print('\n**** Testing device show routes command ****')

        # First must connect to the device
        session = self.device.connect()
        self.assertNotEqual(session, 0, "Failed connection to device")

        # Set terminal length to 0 for long replies
        self.assertTrue(self.device.set_terminal_length())

        # Run show ip route command
        routes_output = self.device.get_routes()

        # Test the command ran successfully
        self.assertNotEqual(routes_output, 0, "Failed show ip route command")

        # Test the data returned from the command
        # Note we test for 'OSPF' just part of the legend for the command output
        self.assertNotEqual(len(routes_output), 0, "Show ip routes: no data")
        self.assertNotEqual(routes_output.find('OSPF'), -1, 
                                                   "Show ip routes: incorrect data")

        self.device.disconnect()  # Clean up the session

    def tearDown(self):

        pass

if __name__ == '__main__':
    unittest.main()