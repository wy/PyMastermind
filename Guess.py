########################
# Author: ~wy
# Date: 25/12/2017
# Description: Represents one of the 6 Guesses in the game
########################


class Guess:

    def __init__(self, choices):
        self.choices = choices

    def get_choices(self):
        return self.choices

    def __str__(self):
        return "[{}]".format(self.choices)



