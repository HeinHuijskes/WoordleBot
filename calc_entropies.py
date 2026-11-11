from solver import *


if __name__ == "__main__":
    NAME = 'NL'

    entropies = {}
    for word in WORDS:
        entropy = word_entropy(word, WORDS)
        entropies[word] = entropy
        print(word, entropy)

    to_save = list(sorted(entropies.items(), key=lambda x: x[1], reverse=True))
    with open('./data/'+LOCATION+'/entropies.txt', 'w') as f:
        f.write('\n'.join([f'{x}: {y}' for x, y in to_save]))
