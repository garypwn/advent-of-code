from walk import Hiking

m = Hiking(open("input.txt"))
longest_paths = m.longest_path(m.start)
print(f"Longest path from start to end is {longest_paths[m.end]} steps.")
