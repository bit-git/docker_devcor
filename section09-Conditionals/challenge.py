import pexpect
from pprint import pprint
import re

# Print heading
print()
print('Interfaces, routes list, routes details')
print('---------------------------------------')

# Create regular expressions to match interfaces and OSPF
OSPF_pattern = re.compile('^O')
intf_pattern = re.compile(r'(GigabitEthernet)([0-9]\/[0-9])')

# Create regular expressions to match prefix and routes
prefix_pattern = re.compile(r'^O.{8}([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\/[0-9]{1,2})')
route_pattern = re.compile(r'via ([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3})')

# Connect to device and run 'show ip route' command
# print('--- connecting ssh 10.30.30.1 with cisco/cisco')

# session = pexpect.spawn('ssh 10.30.30.1', timeout=20)
# result = session.expect(['Username:', pexpect.TIMEOUT])

# # Check for failure
# if result != 0:
#     print('Timeout or unexpected reply from device')
#     exit()

# # Successfully got username prompt, enter username
# session.sendline('cisco')
# result = session.expect('Password:')

# # Enter password
# session.sendline('cisco')
# result = session.expect('>')

# # Must set terminal length to zero for long replies
# print('--- setting terminal length to 0')
# session.sendline('terminal length 0')
# result = session.expect('>')

# # Run the 'show ip route' commanmd on device
# print('--- successfully logged into device, performing show ip route command')
# session.sendline('show ip route')
# result = session.expect('>')

# # Print out the output of the command, for comparison
# print('--- show ip route output:')
# show_ip_route_output = session.before

######################
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
######################
print('--- show ip route output:')
#print(show_ip_route_output)

# Get the output from the command into a list of lines from the output
routes_list = show_ip_route_output.splitlines()

intf_routes= {} # Create dictionary to hold number of routes per interface

# Go through the list of routes to get routes per interface
for route in routes_list:
    OSPF_match = OSPF_pattern.search(route)
    if OSPF_match:
        intf_match = intf_pattern.search(route) # Match for Gigabit Ethernet
        #print(intf_match.group())
        # Check to see if we matched the Gig Ethernet string
        if intf_match:
            intf = intf_match.group(2) # get the interface from the match
            #print(intf)
            if intf not in intf_routes: # If route list not yet created, do so now
                intf_routes[intf] = []
            #pprint(intf_routes)
            # Extract the prefix (destination IP address/subnet)
            prefix_match = prefix_pattern.search(route)
            if prefix_match:
                prefix = prefix_match.group(1)

            # Extract the route
            route_match = route_pattern.search(route)
            next_hop = route_match.group(1)

            # Create dictionary for this route, and add it to the list
            route = {'prefix':prefix,'next-hop':next_hop}
            intf_routes[intf].append(route)

pprint(intf_routes)
print() # Print final blank line            