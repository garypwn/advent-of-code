from cubes import create_games

games = create_games(open('input.txt'))

total = 0
for game in games:
    total += game.min_power()

print(f"The sum min powers is {total}")
