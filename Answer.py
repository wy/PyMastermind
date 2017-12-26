########################
# Author: ~wy
# Date: 25/12/2017
# Description: Represents the Answer
########################

import MastermindConstants


class Answer:

    def __init__(self, choices):
        self.choices = choices

    def get_choices(self):
        return self.choices

    def __str__(self):
        return "[{}]".format(self.choices)

    @staticmethod
    def possible_answers():
        answer_possibilities = []
        arr = MastermindConstants.valid_keys
        for i in range(6):
            for j in range(6):
                for k in range(6):
                    for m in range(6):
                        answer = arr[i] + arr[j] + arr[k] + arr[m]
                        answer_possibilities.append(answer)
        return answer_possibilities



