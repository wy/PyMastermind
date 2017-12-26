########################
# Author: ~wy
# Date: 25/12/2017
# Description: Represents an evaluation of the Guess
########################
import MastermindConstants


class Evaluation:

    @staticmethod
    def evaluate(guess, answer):

        black = 0
        white = 0
        _answer = list(answer[:])
        _guess = list(guess[:])
        evaluation = ""
        for i in range(0, 4):
            if _answer[i] == _guess[i]:
                # Matches exactly, so it's a black
                black += 1
                _answer[i] = "X"
                _guess[i] = "Z"
                # Prevent duplicate marking
        for i in range(0, 4):
            for j in range(0, 4):
                if _answer[i] == _guess[j]:
                    white += 1
                    _answer[i] = "X"
                    _guess[j] = "Z"
        while black > 0:
            evaluation += "B"
            black -= 1
        while white > 0:
            evaluation += "W"
            white -= 1
        while len(evaluation) < 4:
            evaluation += "E"
        return evaluation