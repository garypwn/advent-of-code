from cubes import create_games

games = create_games(open('input.txt'))

limits = {'red': 12, 'green': 13, 'blue': 14}

total = 0
for i, game in enumerate(games):
    i += 1  # Games are 1-indexed
    if game.check_limit(limits):
        total += i

print(f"The sum of game ids is {total}")