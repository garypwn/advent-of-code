from pipes import Pipes

pipes = Pipes(open('input.txt'))
loop = pipes.loop()
print(f"Loop length: {len(loop)}")
print(f"Farthest point: {len(loop) // 2}")