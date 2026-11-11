from typing import Literal
from colorama import Fore, Back, Style
from itertools import product
from math import log


CMAP = {'g': Back.GREEN, 'y': Back.YELLOW, 'b': Back.WHITE}
RESET = Style.RESET_ALL
EMPTY = ' '
LOCATION = 'volkskrant_woord'


with open('./data/'+LOCATION+'/woordenlijst.txt', 'r') as f:
    WORDS = f.read().split('\n')

with open('./data/'+LOCATION+'/entropies.txt', 'r') as f:
    ENTROPIES = {word: float(entropy) for word, entropy in [x.split(': ') for x in f.read().split('\n')]}

PATTERNS = [''.join(word) for word in product('gby', repeat=5)]


def pprint(word, result):
    '''Print out in a pretty wordle format'''
    print(' '.join([CMAP[char]+' '+ Fore.BLACK + word[i]+' '+RESET for i, char in enumerate(result)]))


def compare_to_answer(word: str, answer: str) -> str:
    '''
    Compute the "gyb" colour string by comparing `word` to `answer`.
    '''
    result = ['b' for b in range(len(word))]
    word, answer = [c for c in word], [c for c in answer]

    for i, char in enumerate(word):
        # Find all greens, replace the letters with empty space " "
        if answer[i] == char:
            result[i] = 'g'
            word[i] = EMPTY
            answer[i] = EMPTY

    for i, char in enumerate(word):
        if char == EMPTY or char not in answer:
            continue

        # Check that the word so far does not contain more of this char than present in the answer
        if word[:i].count(char) < answer.count(char):
            result[i] = 'y'

    return ''.join(result)


class WordTracker:
    options: list[str]

    def __init__(self):
        self.options = WORDS.copy()

    def restrict_guess(self, word: str, colours: str):
        # Greens first
        greendices = [i for i, colour in enumerate(colours) if colour == 'g']
        for i in range(len(word)):
            char, colour = word[i], colours[i]
            if colour == 'g':
                self.restrict_green(char, i)

        for i in range(len(word)):
            char, colour = word[i], colours[i]
            self.restrict(char, i, colour, word, greendices)
        return self

    def restrict_green(self, letter: chr, position: int):
        self.options = [word for word in self.options if word[position] == letter]
        return self

    def restrict(self, letter: chr, position: int, colour: Literal['g','y','b'], word: str, greendices: list[int]):
        if colour == 'y':
            self.restrict_yellow(letter, position, word, greendices)
        if colour == 'b':
            self.restrict_black(letter, position, word, greendices)
        return self

    def restrict_yellow(self, letter: chr, position: int, full_word: str, greendices: list[int]):
        options = []
        for word in self.options:
            # Check 1: exact letter position
            if word[position] == letter:
                continue

            old_word = word
            for index in greendices:
                # Remove already green same letters
                if word[index] == letter:
                    word = word[:index] + ' ' + word[index+1:]
                    full_word = full_word[:index] + ' ' + full_word[index+1:]

            # Check 2: non-green part contains this letter AND total amount of yellow matches
            if letter in word and full_word[:position+1].count(letter) <= word.count(letter):
                options.append(old_word)
        self.options = options.copy()
        return self

    def restrict_black(self, letter: chr, position: int, full_word: str, greendices: list[int]):
        options = []
        for word in self.options:
            # Check 1: exact letter position
            if word[position] == letter:
                continue

            old_word = word
            for index in greendices:
                # Remove already green same letters
                if word[index] == letter:
                    word = word[:index] + ' ' + word[index+1:]

            # Check 2: non-green part does not contain this letter, no yellow letter before
            if letter not in word or letter in word[:position]:
                options.append(old_word)
        self.options = options.copy()
        return self

    def count(self):
        return len(self.options)

    def words(self):
        return self.options.copy()


def recalc_entropies(word, words):  
    entropies = {}
    for word in WORDS:
        entropy = word_entropy(word, words)
        entropies[word] = entropy
    return entropies


def word_entropy(word, words):
    counts = {pattern: 0 for pattern in PATTERNS}

    for w in words:
        pattern = compare_to_answer(word, w)
        counts[pattern] += 1

    counts = {key:val for key,val in counts.items() if val != 0}
    total = sum(counts.values())
    entropy = 0
    for key in counts.keys():
        p = counts[key] / total
        entropy += - p * log(p,2)

    return entropy


def information_gained(word, colours, words):
    counts = {pattern: 0 for pattern in PATTERNS}

    for w in words:
        pattern = compare_to_answer(word, w)
        counts[pattern] += 1

    counts = {key:val for key,val in counts.items() if val != 0}
    total = sum(counts.values())

    p = counts[colours] / total
    information = - log(p,2)
    return information

