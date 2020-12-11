import re

routes_list = [] # Create the list of routes

# #-----------------------------------------------------------
# # The following code connects to a device and dumps all
# # routing information

# print '--- connecting telnet 10.30.30.1 with cisco/cisco'

# session = pexpect.spawn('telnet 10.30.30.1', timeout=20)
# result = session.expect(['Username:', pexpect.TIMEOUT])

# # Check for failure
# if result != 0:
#     print 'Timout or unexpected reply from device'
#     exit()

# # Successfully got password prompt, logging in with username
# session.sendline('cisco')
# result = session.expect('Password:')

# # Successfully got password prompt, logging in with username
# session.sendline('cisco')
# result = session.expect('>')

# # Must set terminal length to zero for long replies
# print '--- setting terminal length to 0'
# session.sendline('terminal length 0')
# result = session.expect('>')

# # Execute the 'show ip route' command to get routing info
# print '--- executing: show ip route'
# session.sendline('show ip route')
# result = session.expect('>')

# # Get output from ip route command
# print '--- getting ip route command output'
# show_ip_route_output = session.before

show_ip_route_output = '''
show ip route
Codes: L - local, C - connected, S - static, R - RIP, M - mobile, B - BGP
       D - EIGRP, EX - EIGRP external, O - OSPF, IA - OSPF inter area
       N1 - OSPF NSSA external type 1, N2 - OSPF NSSA external type 2
       E1 - OSPF external type 1, E2 - OSPF external type 2
       i - IS-IS, su - IS-IS summary, L1 - IS-IS level-1, L2 - IS-IS level-2, 
       ia - IS-IS inter area, * - candidate default, U - per-user static root
       o - ODR, P - periodic downloaded static route, H - NHRP, l - LISP
       a - application route
       + - replicated root, % - next hop override

Gateway of last resort not set

      10.0.0.0/8 is variably subnetted, 11 subnets, 3 masks
C        10.1.1.0/24 is directly connected, GigabitEthernet0/1
L        10.1.1.1/32 is directly connected, GigabitEthernet0/1
C        10.1.2.0/30 is directly connected, GigabitEthernet0/2
L        10.1.2.1/32 is directly connected, GigabitEthernet0/2
C        10.1.3.0/30 is directly connected, GigabitEthernet0/3
L        10.1.3.1/32 is directly connected, GigabitEthernet0/3
O        10.2.3.0/30 [110/2] via 10.1.3.2, 00:04:14, GigabitEthernet0/3
                     [110/2] via 10.1.2.2, 00:04:14, GigabitEthernet0/2
O E2      10.11.12.0/24 [110/20] via 10.1.3.2, 00:04:14, GigabitEthernet0/3
                     [110/20] via 10.1.2.2, 00:04:24, GigabitEthernet0/2
C        10.30.30.1/32 is directly connected, Loopback0
O E2      10.30.30.2/32 [110/20] via 10.1.2.2, 00:04:24, GigabitEthernet0/2
O E2      10.30.30.3/32 [110/20] via 10.1.3.2, 00:04:14, GigabitEthernet0/3
'''

print()
print('IP route output')
print('----------------------------------------------------')
print(show_ip_route_output)
print('----------------------------------------------------')
print()

# Get routing information into list
routes_list = show_ip_route_output.splitlines()

while True: # Loop forever, until user terminates program

    # Request user to input the IP destination route prefix we will search for
    try:
        ip_address = input('Enter IP destination address to find (Ctrl-C to exit):')
    except KeyboardInterrupt:
        break

    # Set the pattern for matching OSPF routes
    route_pattern = re.compile(r'^O.{8}([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3})')

    # Loop through our devices looking for a match on IP address
    for route in routes_list:

        # Search for our route string, and continue to next iteration if not found
        route_match = route_pattern.search(route)
        if not route_match: continue

        # Found our IP address, print out route information
        if route_match.group(1) == ip_address:
            route_info = route.split(',')
            print('  ---- Route:     ', route_info[0][5:].strip())
            print('  ---- Time:      ', route_info[1].strip())
            print('  ---- Interface: ', route_info[2].strip())
            print()
            break

    else:  # We get here if we exhausted the device list, IP not found
        print('--- Given route prefix not found ---')

print()
print('Route search terminated.\n')

# session.sendline('quit')
# session.kill(0)    