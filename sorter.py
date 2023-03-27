import googlemaps
import numpy as np
from sklearn.cluster import KMeans
import warnings

def sort_addresses(key):
    gmaps = googlemaps.Client(key=key)

    # Read in the addresses from the text file

    warnings.filterwarnings("ignore")
    with open('addresses.txt') as f:
        addresses = [line.strip() for line in f]

    # Get the latitude and longitude for each address
    locations = []
    for address in addresses:
        result = gmaps.geocode(address)
        if result:
            location = result[0]['geometry']['location']
            locations.append((location['lat'], location['lng']))

    # Ask the user for the number of groups to create
    num_groups = int(input("Enter the number of groups to create: "))
    kmeans = KMeans(n_clusters=num_groups, random_state=0).fit(np.array(locations))

    # Print out the groups to a text file
    with open('groups.txt', 'w') as f:
        for i in range(num_groups):
            f.write("Group " + str(i + 1) + "\n")
            for j in range(len(kmeans.labels_)):
                if kmeans.labels_[j] == i:
                    f.write(addresses[j] + "\n")
            f.write("\n")

