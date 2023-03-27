import time
import googlemaps
from datetime import datetime
import webbrowser
import sorter

# Enter your API key here
key = input("Enter your Google Maps API Key here: ")
gmaps = googlemaps.Client(key=key)
sorter.sort_addresses(key)
# Starting location
start = input("Enter the address of your starting location: ")

# Read the groups from the text file
with open("groups.txt", "r") as f:
    groups = f.read().split("\n\n")


# Helper function to find the nearest neighbor
def find_nearest_neighbor(curr, unvisited):
    # Find the nearest unvisited neighbor
    nearest_neighbor = None
    nearest_duration = None
    for neighbor in unvisited:
        directions_result = gmaps.directions(curr, neighbor, mode="driving", departure_time=datetime.now())
        duration = directions_result[0]['legs'][0]['duration']['value']
        if nearest_duration is None or duration < nearest_duration:
            nearest_duration = duration
            nearest_neighbor = neighbor
    return nearest_neighbor, nearest_duration


# Iterate over each group
for i in range(len(groups)):
    # Split the group into a list of addresses
    if not groups[i].strip():
        continue
    group = groups[i]
    addresses = group.strip().split("\n")[1:]

    # Find the shortest route between all the addresses in 'addresses' starting from 'start'
    unvisited = set(addresses)
    curr = start
    shortestRoute = [start]
    shortestDuration = 0

    while unvisited:
        # Find the nearest unvisited neighbor
        nearest_neighbor, duration = find_nearest_neighbor(curr, unvisited)

        # Update the shortest duration and route
        shortestDuration += duration
        shortestRoute.append(nearest_neighbor)

        # Move to the nearest neighbor
        curr = nearest_neighbor
        unvisited.remove(nearest_neighbor)

    # Print the shortest route with line breaks between each address and the total distance
    print(f"\nThe shortest route for {group.splitlines()[0]} is:\n")
    with open("routes.txt", "a") as f:
        f.write(f"\nThe shortest route for {group.splitlines()[0]} is:\n")
        for i, address in enumerate(shortestRoute):
            print(address)
            f.write(f"{address}\n")
            if i != len(shortestRoute) - 1:
                print("to")
                f.write("to\n")
        # Round the duration to the nearest minute
        print(f"\nThe total duration is {round(shortestDuration / 60)} minutes.\n")
        f.write(f"\nThe total duration is {round(shortestDuration / 60)} minutes.\n\n")

        # Print the link to the Google Maps directions
        print(f"Opening the link to the Google Maps directions for {group.splitlines()[0]}...\n")
        f.write(f"Link to the Google Maps directions for {group.splitlines()[0]}:\n")
        time.sleep(1.25)
        gmapsUrl = "https://www.google.com/maps/dir/?api=1&origin=" + start + "&destination=" + shortestRoute[
            -2] + "&travelmode=driving" + "&waypoints=" + "|".join(shortestRoute[1:-2])
        webbrowser.open(gmapsUrl)
        f.write(f"{gmapsUrl}\n\n")
