import pexpect

#-----------------------------------------------------------
# The following code connects to a device

def connect(dev_ip,username,password):
    """
    Connects to device using pexpect

    :dev_ip: The IP address of the device we are connectin to
    :username: The username that we should use when logging in
    :password: The password that we should use when logging in

    =return: pexpect session object if succssful, 0 otherwise

    """

    print('--- attempting to: ssh ' + dev_ip)

    session = pexpect.spawn('ssh ' + username + '@' + dev_ip + ' -p 8181', timeout=20)

    # result = session.expect(['Username:', pexpect.TIMEOUT])
    # # Check for failure
    # if result != 0:
    #     print('--- Timeout or unexpected reply from device')
    #     return 0

    # print('--- attempting to: username: ' + username)

    # # Successfully got username prompt, logging with username
    # session.sendline(username)

    result = session.expect(['Password:', pexpect.TIMEOUT])
    # Check for failure
    if result != 0:
        print('--- Timeout or unexpected reply from device')
        return 0

    print('--- attempting to: password: ' + password)

    # Successfully got password prompt, logging in with password
    session.sendline(password)
    session.expect('#')

    return session  # return pexpect session object to caller

#-----------------------------------------------------------
# The following function gets and returns interface information

def show_int_summary(session):
    """
    Runs 'show int summary' command on device and returns 
    output from device in a string

    :session: The pexpect session for communication with device

    =return: string of output from device
    """

    print('--- show interface summary command')
    session.sendline('show interface summary')
    result = session.expect('#')

    print('--- getting interface command output')
    show_int_brief_output = session.before

    return show_int_brief_output

#-----------------------------------------------------------
def read_devices_info(filename):

    devices_list = []

    file = open(filename,'r')
    for line in file:

        device_info_list = line.strip().split(',')

        device_info = {}
        device_info['name'] = device_info_list[0]
        device_info['ip'] = device_info_list[1]
        device_info['username'] = device_info_list[2]
        device_info['password'] = device_info_list[3]

        devices_list.append(device_info)

    return devices_list


def print_device_info(device_info,show_int_output):

    print('-------------------------------------------------------')
    print('    Device Name:      ',device_info['name'])
    print('    Device IP:        ',device_info['ip'])
    print('    Device username:  ',device_info['username'],)
    print('    Device password:  ',device_info['password'])

    print()
    print('    Show Interface Output')
    print()

    print(show_int_output.decode())
    print('-------------------------------------------------------')


# Main program: connect to device, show interface, display

if __name__ == '__main__':

    devices_list = read_devices_info('sbx')

    for device_info in devices_list:

        session = connect(device_info['ip'],
                          device_info['username'],
                          device_info['password'])
        if session == 0:
            print ('--- Session attempt unsuccessful ---')
            continue

        show_int_output = show_int_summary(session)

        print_device_info(device_info,show_int_output)

        session.sendline('exit')
        session.kill(0)

        