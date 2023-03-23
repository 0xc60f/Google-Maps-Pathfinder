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
print("The total duration is " + str(int(shortestDuration/60)) + " minutes.")

# Print the link to the Google Maps directions
print("Opening the link to the Google Maps directions...")
gmapsUrl = "https://www.google.com/maps/dir/?api=1&origin=" + start + "&destination=" + start + "&travelmode=driving&waypoints=" + "|".join(addresses)
webbrowser.open(gmapsUrl)




