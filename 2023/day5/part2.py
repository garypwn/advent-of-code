from seedmap import *

seeds, mappings = read_input(open("input.txt"), seed_ranges=True)

locations = []
for seed in seeds:
    for mapping in mappings:
        seed = mapping[seed]

    locations.append(seed)

print(f"Lowest location: {min([location[0] for location in locations])}")
