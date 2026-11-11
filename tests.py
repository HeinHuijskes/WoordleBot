import unittest
from solver import compare_to_answer, WordTracker, WORDS


class TestCompareToAnswerMethod(unittest.TestCase):

    def testDifferentWords(self):
        guess, answer = "SUPER", "BLOOD"
        result = compare_to_answer(guess, answer)
        self.assertEqual(result, "bbbbb")
        result = compare_to_answer(answer, guess)
        self.assertEqual(result, "bbbbb")
        self.assertNotEqual(result, "gggyy")

    def testSameWords(self):
        guess, answer = "DOUBT", "DOUBT"
        result = compare_to_answer(guess, answer)
        self.assertEqual(result, "ggggg")
        result = compare_to_answer(answer, guess)
        self.assertEqual(result, "ggggg")

    def testYellows(self):
        guess, answer = "LIARS", "RAILS"
        result = compare_to_answer(guess, answer)
        self.assertEqual(result, "yyyyg")
        result = compare_to_answer(answer, guess)
        self.assertEqual(result, "yyyyg")

    def testRepetition(self):
        guess, answer = "QUEUE", "USURP"
        result = compare_to_answer(guess, answer)
        self.assertEqual(result, "bybyb")
        result = compare_to_answer(answer, guess)
        self.assertEqual(result, "ybybb")

    def testEmptyRepetition(self):
        guess, answer = "AARGH", "BANDS"
        result = compare_to_answer(guess, answer)
        self.assertEqual(result, "bgbbb")
        result = compare_to_answer(answer, guess)
        self.assertEqual(result, "bgbbb")

    def testEmptyRepetition(self):
        guess, answer = "SHOOT", "OVERT"
        result = compare_to_answer(guess, answer)
        self.assertEqual(result, "bbybg")
        result = compare_to_answer(answer, guess)
        self.assertEqual(result, "ybbbg")


class TestWordRestriction(unittest.TestCase):

    tracker: WordTracker

    def setUp(self):
        self.tracker = WordTracker()
        return super().setUp()

    def initialSetupCheck(self):
        self.assertEqual(len(WORDS), len(self.tracker.words()))
        self.assertEqual(len(WORDS), self.tracker.count())

    def testGreenRestrict(self):
        colours, guess = 'ggggg', 'provo'
        self.tracker.restrict_guess(guess, colours)
        self.assertEqual(self.tracker.count(), 1)
        self.assertEqual(self.tracker.words()[0], guess)
        
    def testGreenRestrict(self):
        colours, guess = 'gggbb', 'aafst'
        results = ['aafje','aafke']
        self.tracker.restrict_guess(guess, colours)
        self.assertEqual(self.tracker.count(), 2)
        self.assertListEqual(self.tracker.words(), results)
        
    # def testGreenishRestrict(self):
    #     colours, guess = 'bgggg', 'AARGH'
    #     self.tracker.restrict_guess(guess, colours)
    #     self.assertEqual(self.tracker.count(), 1)
    #     self.assertEqual(self.tracker.options()[0], guess)



if __name__ == '__main__':
    unittest.main()