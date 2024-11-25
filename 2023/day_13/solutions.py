from mirrors import *

mirrors = parse(open('input.txt'))
print(f'Summary of mirrors: {sum(summarize(m) for m in mirrors)}')

mirrors = parse(open('input.txt'))
print(f'Summary of de-smudged mirrors: {sum(de_smudge(m) for m in mirrors)}')