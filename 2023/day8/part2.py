from desert import *

path, network = read_lines(open('input.txt'))
print(f"Path length is: {ghost_path_length(path, network)}")
