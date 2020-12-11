#!/usr/bin/python

import re
import pexpect
import os

#-----------------------------------------------------------------------
def get_devices_list(filename):

    devices_list = []
    file = open(filename, 'r')

    for line in file:
        devices_list.append( line.rstrip() )

    file.close()

    print('devices list:', devices_list)
    return devices_list

#-----------------------------------------------------------------------
def connect(ip_address, username, password):

    print('Establishing ssh session:', ip_address)
    ssh_command = 'ssh ' + username + '@' + ip_address + ' -p 8181'
    print(ssh_command)
    # Connect via ssh to device
    session = pexpect.spawn(ssh_command, timeout=30)
    result = session.expect(['Password:', pexpect.TIMEOUT])

    # Check for error, if so then print error and exit
    if result != 0:
        print('!!! SSH failed creating session for: ', ip_address)
        exit()

    # Enter the username, expect password prompt afterwards
    # session.sendline(username)
    # result = session.expect(['Password:', pexpect.TIMEOUT])

    # # Check for error, if so then print error and exit
    # if result != 0:
    #     print '!!! Username failed: ', username
    #     exit()

    session.sendline(password)
    result = session.expect(['#', pexpect.TIMEOUT])

    # Check for error, if so then print error and exit
    if result != 0:
        print('!!! Password failed: ', password)
        exit()

    print('--- Connected to: ', ip_address)
    return session

#-----------------------------------------------------------------------
def get_version_info(session):

    print('--- Getting version information')

    session.sendline('show version | include Version')
    result = session.expect(['#', pexpect.TIMEOUT])
    # Check for error, if so then print error and exit
    if result != 0:
        print('--- Failure! getting the show version output')
        exit()
    # Extract the 'version' part of the output
    version_output_lines = session.before.splitlines()
    #print(version_output_lines)

    version_output_parts = version_output_lines[1].decode().split(',')

    version = version_output_parts[1].split(' ')
    version = version[2].strip()

    print('--- Got version: ', version)
    return version

#-----------------------------------------------------------------------

filename = os.environ['FILE']
ip_address = os.environ['DEVICE_IP']
username = os.environ['DEVICE_USER']
password = os.environ['DEVICE_PASSWORD']
password_enable = os.environ['DEVICE_PASSWORD']


devices_list = get_devices_list(filename)    # Get list of devices

version_file_out = open('version-info-out', 'w')



# Loop through all the devices in the devices list
for ip_address in devices_list:

    # Connect to the device via CLI and get version information
    session = connect(ip_address, username, password)
    device_version = get_version_info(session)

    session.close()  # Close the session

    version_file_out.write('IP: ' + ip_address + '  Version: ' + device_version + '\n')

# Done with all devices and writing the file, so close
version_file_out.close()