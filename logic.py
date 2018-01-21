import random

alphabets = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U',
             'V', 'W', 'X', 'Y', 'Z']


def biased_random(p, pool_a, pool_b):
    for x in pool_b:
        if x in pool_a:
            pool_a.remove(x)
    if random.random() < p:
        x = random.randint(0, len(pool_b) - 1)
        print pool_b[x]
    else:
        x = random.randint(0, len(pool_a) - 1)
        print pool_a[x]


left_alphabets = ['C', 'O', 'M', 'P', 'U', 'T', 'E', 'R']
biased_random(0.5, alphabets, left_alphabets)

# 0 probability will never let player to win
# 1 probability will make player to win every time

