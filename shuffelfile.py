import random
with open('spn/keys.txt', 'r') as f:
    data = f.read().splitlines()
    random.shuffle(data)
    f.close
with open('spn/keys.txt', 'w') as f:
    for i in data:
        f.write(i + '\n')
    f.close()
