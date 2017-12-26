# Has access to the Guesses and Evaluation but not the Answer of course

import Evaluation
from Answer import Answer


class GameAI:

    starting_possibles = Answer.possible_answers()

    def smart_map(self, guess):
        evaluation_map = {}  # Map from Evaluation -> [answers]
        for p in self.possibles:
            evaluation = Evaluation.Evaluation.evaluate(guess, p)
            if evaluation in evaluation_map:
                answer_list = evaluation_map[evaluation]
                answer_list.append(p)
                evaluation_map[evaluation] = answer_list
            else:
                evaluation_map[evaluation] = [p]
        max_count = 0

        tot = len(self.possibles)
        expectation = 0.0
        for k in evaluation_map:
            cnt = len(evaluation_map[k])
            expectation += cnt * cnt / tot
            if cnt > max_count:
                max_count = cnt
        return max_count, round(expectation, 2)

    def smart_eval(self, debug=True):
        guesses = self.possibles
        scores = []
        minimum = 1296
        best_guess = None
        for guess in guesses:
            maximum, expectation = self.smart_map(guess)
            scores.append((maximum, expectation))
            if maximum < minimum:
                minimum = maximum
                best_guess = guess
        g_s = list(zip(guesses, scores))
        sorted_g_s = sorted(g_s, key=lambda s: s[1])
        self.topList = sorted_g_s
        if debug:
            print("{} possible choices".format(len(sorted_g_s)))
            for i in range(0, min(10, len(sorted_g_s))):
                print("{} max: {}".format(sorted_g_s[i][0], sorted_g_s[i][1]))
        return best_guess

    def __init__(self):
        self.possibles = GameAI.starting_possibles[:]
        self.topList = []

    def reset(self):
        self.possibles = GameAI.starting_possibles[:]
        self.topList = []

    def get_selection(self, maximum=6):
        return self.topList[:min(maximum, len(self.topList))]

    def cull_possibilities(self, guess, evaluation):
        for answer in list(self.possibles):
            possible_answer_evaluation = Evaluation.Evaluation.evaluate(guess, answer)
            if possible_answer_evaluation != evaluation:
                self.possibles.remove(answer)
