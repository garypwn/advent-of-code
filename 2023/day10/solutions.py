from pipes import Pipes, area

pipes = Pipes(open('input.txt'))
loop = list(pipes.loop())
print(f"Loop length: {len(loop)}")
print(f"Farthest point: {len(loop) // 2}")
print(f"Area: {area(loop)}")
