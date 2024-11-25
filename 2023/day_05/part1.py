from seedmap import *

seeds, mappings = read_input(open("input.txt"))

locations = []
for seed in seeds:
    for mapping in mappings:
        seed = mapping[seed]

    locations.append(seed)

print(f"Locations: {locations}\n")
print(f"Lowest location: {min(locations)}")
