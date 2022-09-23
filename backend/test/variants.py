import itertools

option_groups = [
    ['a1', 'a2'],
    ['b1', 'b2', 'b3', 'b4'],
    ['c1', 'c2', 'c3']
]

options = list(itertools.product(*option_groups))

for o in options:
    print(o)


