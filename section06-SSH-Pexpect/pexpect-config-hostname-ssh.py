import pexpect
import os


ip_address = os.environ['DEVICE_IP']
username = os.environ['DEVICE_USER']
password = os.environ['DEVICE_PASSWORD']
password_enable = os.environ['DEVICE_PASSWORD']

#create the pexpect session
ssh_command = 'ssh ' + username + '@' + ip_address + ' -p 8181'
print(ssh_command)
session = pexpect.spawn(ssh_command, timeout=20)
result = session.expect(['Password:', pexpect.TIMEOUT])

# Check for error, if so then print error and exit
if result != 0:
    print('--- FAILURE! creating session for: ', ip_address)
    exit()

# Session expecting password, enter it here
session.sendline(password)

######## Section for priv mode and enable passwprd
# result = session.expect(['>', pexpect.TIMEOUT])

# # Check for error, if so then print error and exit
# if result != 0:
#     print('--- FAILURE! entering password: ', password)
#     exit()

# # Enter enable mode
# session.sendline('enable')
# result = session.expect(['Password:', pexpect.TIMEOUT])

# # Check for error, if so then print error and exit
# if result != 0:
#     print('--- Failure! entering enable mode')
#     exit()

# # Send enable password
# session.sendline(password_enable)
########

result = session.expect(['#', pexpect.TIMEOUT])

# Check for error, if so then print error and exit
if result != 0:
    print('--- Failure! entering enable mode after sending password')
    exit()

# Check for hostname in running config
session.sendline('show runn | i hostname')
result = session.expect(['#', pexpect.TIMEOUT])
old_hostname = session.before.splitlines()

# Issue config t command.  
session.sendline('config t')
result = session.expect([r'\(config\)#', pexpect.TIMEOUT])

# Check for error, if so then print error and exit
if result != 0:
    print('--- Failure! entering config mode')
    exit()

# Change the hostname to R1
session.sendline('hostname csr1000v-1')
result = session.expect([r'csr1000v-1\(config\)#', pexpect.TIMEOUT])

# Check for error, do not exit - exit config mode first
if result != 0:
    print('--- Failure! setting hostname')

# Exit config mode
session.sendline('exit')
result = session.expect(['#', pexpect.TIMEOUT])

# Check for hostname in running config
session.sendline('show runn | i hostname')
result = session.expect(['#', pexpect.TIMEOUT])
new_hostname = session.before.splitlines()

# Exit config mode and exit enable mode
session.sendline('exit')
session.sendline('exit')

print('--- Success! connecting to: ', ip_address)
print('---               Username: ', username)
print('---               Password: ', password)
print('---      Previous Hostname: ', old_hostname[2].decode())
print('---           New Hostname: ', new_hostname[2].decode())
print('------------------------------------------------------\n')

# End session
session.close()