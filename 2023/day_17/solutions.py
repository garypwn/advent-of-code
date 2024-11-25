from city import City

city = City(open('input.txt'))
print(f"Shortest path: {city.dijkstra()[-1, -1]}")
print(f"Shortest path for the ultra crucible: {city.dijkstra(min_len=4, max_len=10)[-1, -1]}")
