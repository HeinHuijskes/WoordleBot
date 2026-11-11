from solver import *


results = {x: 0 for x in range(1,8)}
word_results = {}


for word in WORDS:
    words = WORDS.copy()
    guesses = 0
    entropies = ENTROPIES.copy()
    guess = 'salet'
    track = WordTracker()

    while True:
        guesses += 1

        colours = compare_to_answer(guess, word)
        track.restrict_guess(guess, colours)
        words = track.words()

        if len(words) == 1 or guesses == 7:
            break

        highest = 0
        guess = ''
        for w in WORDS:
            entropy = word_entropy(w, words)
            if entropy > highest:
                guess, highest = w, entropy

    results[guesses] += 1
    word_results[word] = guesses
    print(word, guesses, results)


with open('./data/'+LOCATION+'/entropy_results.txt', 'w') as f:
    f.write('\n'.join([f'{x}: {y}' for x,y in results.items()]))


with open('./data/'+LOCATION+'/word_guesses.txt', 'w') as f:
    word_results = sorted(word_results.items(), key=lambda x: str(x[1])+x[0])
    f.write('\n'.join([f'{x}: {y}' for x,y in word_results]))