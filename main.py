import time
import googlemaps
from datetime import datetime
import itertools
import webbrowser

# Enter your API key here
key = input("Enter your Google Maps API Key here: ")
gmaps = googlemaps.Client(key=key)

# Starting location
start = input("Enter the address of your starting location: ")

numAddresses = int(input("Enter the number of addresses you want to visit: "))
# List of addresses to visit
addresses = []
for i in range(numAddresses):
    addresses.append(input("Enter the address you want to add: "))
    # Find the shortest duration between all the addresses in addresses starting from start
    # Create a list of all possible permutations of the addresses
permutations = list(itertools.permutations(addresses))
print("\nCalculating the shortest route...  Please be patient.\n")
# Create a list of all possible routes
routes = []
for permutation in permutations:
    routes.append([start] + list(permutation))
# Find the shortest route
shortestRoute = routes[0]
shortestDuration = 0
for route in routes:
    # Find the duration of the route
    duration = 0
    for i in range(len(route) - 1):
        # Find the duration between each address
        directions_result = gmaps.directions(route[i], route[i + 1], mode="driving", departure_time=datetime.now())
        duration += directions_result[0]['legs'][0]['duration']['value']
    # Check if the duration is shorter than the shortest duration
    if shortestDuration == 0 or duration < shortestDuration:
        shortestDuration = duration
        shortestRoute = route

# Print the shortest route with line breaks between each address and the total distance
print("The shortest route is:")
for i in range(len(shortestRoute)):
    print(shortestRoute[i])
    if i != len(shortestRoute) - 1:
        print("to")
# Round the duration to the nearest minute
print("\nThe total duration is " + str(round(shortestDuration/60)) + " minutes.\n")

# Print the link to the Google Maps directions
print("Opening the link to the Google Maps directions...")
# Timeout for 1 second
time.sleep(1.25)
# Create a Google Maps URL for the shortest route in the shortestRoute list. The start address is the variable start,
# and the destination address is the last address in the shortestRoute list
gmapsUrl = "https://www.google.com/maps/dir/?api=1&origin=" + start + "&destination=" + shortestRoute[-1] + "&travelmode=driving" + "&waypoints=" + "|".join(shortestRoute[1:-1])
webbrowser.open(gmapsUrl)




