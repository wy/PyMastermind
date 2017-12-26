########################
# Author: ~wy
# Date: 25/12/2017
# Description: Represents the Game State
########################

from Answer import Answer
from Guess import Guess
from Evaluation import Evaluation
import random
import datetime
import MastermindConstants


class Game:
    def __init__(self):
        self.currentLevel = 1
        self.Answer = None
        self.Guesses = []
        self.Evaluations = []
        self.status = "Not Won"
        self.startTime = datetime.datetime.now()
        self.endTime = None

    def reset(self):
        self.__init__()

    def get_time_elapsed(self):
        return (self.endTime - self.startTime).seconds

    def get_answer(self):
        return self.Answer

    def get_status(self):
        return self.status

    def pick_answer(self, choices=None):
        if choices is None:
            arr = MastermindConstants.starting_recommendation
            input_var = ""
            for i in range(0, 4):
                input_var += random.choice(arr)
            choices = input_var
        self.Answer = Answer(choices)

    def get_level(self):
        return self.currentLevel

    def make_guess(self, choices):
        guess = Guess(choices)
        self.Guesses.append(guess)
        self.evaluate_guess()
        self.currentLevel += 1
        if self.currentLevel == 7:
            self.endTime = datetime.datetime.now()

    def evaluate_guess(self):
        guess = self.Guesses[-1].get_choices()
        answer = self.Answer.get_choices()
        evaluation = Evaluation.evaluate(guess,answer)
        self.Evaluations.append(evaluation)
        if Game.has_won(evaluation):
            self.status = "Won"
            self.endTime = datetime.datetime.now()

    @staticmethod
    def has_won(evaluation):
        return evaluation == MastermindConstants.winning_evaluation

    def get_evaluation(self):
        return self.Evaluations[-1]

    def __str__(self):
        s = ""
        for i in range(1, self.currentLevel):
            s += "{}[{}]{}\n".format(self.Evaluations[i - 1], i, self.Guesses[i - 1])
        return s
