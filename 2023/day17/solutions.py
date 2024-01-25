from city import City

city = City(open('input.txt'))
print(f"Shortest path: {city.dijkstra()[-1, -1]}")
