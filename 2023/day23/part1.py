from walk import Hiking

m = Hiking(open("input.txt"))
longest_path = m.longest_path(m.start, m.end)
print(f"Longest path from start to end is {longest_path} steps.")
