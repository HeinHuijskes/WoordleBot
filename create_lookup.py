from solver import *
import json


# Create a lookup table for each inital pattern possible from "SALET"
# Possibly recurse this to build a tree to all the correct answers 
# Store as JSON


if __name__ == "__main__":
    START = "salet"
    TREE = (START, {})

    for word in WORDS[29:]:
        words = WORDS.copy()
        guess = START
        track = WordTracker()
        subtree = TREE[1]
        
        guesses = 0
        print(word)
        while True:
            guesses += 1

            # Restrict possible words
            colours = compare_to_answer(guess, word)
            track.restrict_guess(guess, colours)
            words = track.words()
            print(guesses, guess, colours)

            if len(words) == 1:
                # Arrived at a leaf! Stop looping
                subtree[colours] = guess
                break

            if colours not in subtree.keys():
                print('Calculating entropy...', len(track.words()), [(w, word_entropy(w, words)) for w in track.words() + ['inrol']])
                print()
                # New branch, calculate highest entropy
                highest = -1
                guess = ''
                for w in WORDS:
                    entropy = word_entropy(w, words)
                    if entropy > highest:
                        guess, highest = w, entropy
                subtree[colours] = (guess, {})

            # Move further into the branch
            guess, subtree = subtree[colours]
        
        print(f'Word: {word}, Guesses: {guesses}, Tree trunk size: {len(TREE[1])}')
        

    with open('./data/'+LOCATION+'/tree.json', 'w') as f:
        json.dump(TREE, f)
