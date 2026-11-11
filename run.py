from solver import *
import random


if __name__ == "__main__":
    answer = input("Set answer, use random, or enter manually? ")
    if answer == "random" or answer == "r":
        print('Guesses are in the form of:  "<word>", e.g.: "salet"')
        answer = random.choice(WORDS)
        use_answer = True
    elif len(answer) == 5:
        print('Guesses are in the form of:  "<word>", e.g.: "salet"')
        use_answer = True
    else:
        print('Guesses are in the form of:  "<word> - <colours>", e.g.: "salet - gbybb"')
        use_answer = False
    print()

    track = WordTracker()
    guesses = []
    entropies = ENTROPIES.copy()
    print(len(entropies), len(ENTROPIES))
    words = WORDS.copy()

    while True:

        if len(words) < len(WORDS):
            entropies = {}
            print('Recalculating entropy...')
            for word in WORDS:
                entropy = word_entropy(word, words)
                entropies[word] = entropy

        top = [f'{x}: {round(y,2)}' for x,y in sorted(entropies.items(), key=lambda x: x[1], reverse=True)][:8]
        print('Top words:')
        print('\n'.join(top))
        print()

        print(f'Options: {track.count()}')
        new_guess = input('Next guess: ')
        if use_answer:
            guess = new_guess
            colours = compare_to_answer(guess, answer)
        else:
            guess, colours = new_guess.split(' - ')
        guesses.append(guess)
        print()

        information = round(information_gained(guess, colours, words),2)
        entropy = round(entropies[guess],2)

        track.restrict_guess(guess, colours)
        words = track.words()
        if len(words) == 1:
            print(f"Game won in {len(guesses)} moves!")
            exit()

        pprint(guess, colours)
        print()

        print(f'Information gained: {information} bits (Expected {entropy} bits)')
        print(f'Options left: {track.count()}')


