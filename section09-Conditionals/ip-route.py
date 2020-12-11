from pprint import pprint
import re

# Create regular expression to match Gigabit interface names
gig_pattern = re.compile(r'(GigabitEthernet)([0-9]\/[0-9]\/[0-9]\/[0-9])')

routes = {}

# Read all lines of IP routing information
with open('ip-routes','r') as file:
    for line in file:
        match = gig_pattern.search(line) # Match for Gigabit Ethernet

        # Check to see if we matched the Gig Ethernet string
        if match:
            #print(match.group())
            intf = match.group(2) # get the interface from the match
            
            pprint(routes)
            # populate the routes dict, increment the route count if intf is already in routes dict
            # else add intf with count 1. KeyError: '0/0/0/0' if intf not in routes
            routes[intf] = routes[intf] + 1 if intf in routes else 1
            
print() # Print blank line
print('Number of routes per interface')
print('------------------------------')
pprint(routes)
print() # Print final blank line