from aoc_lube import fetch

s = fetch(2019, 8)

# The image you received is 25 pixels wide and 6 pixels tall.

layers_row = [s[i:i+25*6] for i in range(0, len(s), 25*6)]
layers = [[layers_row[i][j:j+25] for j in range(0, len(layers_row[i]), 25)] for i in range(len(layers_row))]

min_layer = min(layers, key=lambda x: sum(i.count('0') for i in x))
print(sum(i.count('1') for i in min_layer) * sum(i.count('2') for i in min_layer))


for i in range(6):
    for j in range(25):
        for layer in layers:
            if layer[i][j] == '0':
                print(' ', end='')
                break
            if layer[i][j] == '1':
                print('X', end='')
                break
    print()
