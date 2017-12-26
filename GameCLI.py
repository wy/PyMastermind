########################
# Author: ~wy
# Date: 25/12/2017
# Description: Lets you play the game via CLI
########################

from Game import Game
from GameAI import GameAI
from Answer import Answer
import random
import MastermindConstants

hidden_answer_prompt = "Enter Your Hidden Answer as 4 Letter String. " \
                       "e.g. YYYY for Yellow, Yellow, Yellow, Yellow. Colours " \
                       "are Y=Yellow,R=Red,G=Green,B=Blue,O=Orange,P=Purple\n"
guess_prompt = "Enter Your Guess. Colours" \
               " are Y=Yellow,R=Red,G=Green,B=Blue,O=Orange,P=Purple\n"


def main():
    print("Welcome to Mini Master Mind (PyMasterMind)")

    mode_select = input("Please pick a mode. 1 = Computer creates a hidden answer. "
                        "2 = You create a hidden answer for your friend. "
                        "3 = You create a hidden answer for the computer to guess\n")

    input_var = ""
    if mode_select == "1":
        arr = MastermindConstants.valid_keys
        for i in range(0, 4):
            input_var += random.choice(arr)
    elif mode_select == "2":
        input_var = input(hidden_answer_prompt)
        assert (len(input_var) == 4), "Please enter 4 Letters"
    elif mode_select == "3":
        input_var = input(hidden_answer_prompt)
        assert (len(input_var) == 4), "Please enter 4 Letters"

    game_ai = GameAI()
    g = Game()
    g.pick_answer(input_var)
    while g.get_level() < 7:
        choices = []
        print("You are starting level {}".format(g.get_level()))
        if mode_select == "1" or mode_select == "2":
            input_var = input(guess_prompt)
            if len(input_var) != 4:
                input_var = input(guess_prompt)
            choices = list(input_var)
            g.make_guess(choices)
        if mode_select == "3":
            if g.get_level() == 1:
                recommended_guess = MastermindConstants.starting_recommendation
            else:
                recommended_guess = game_ai.smart_eval(debug=False)
            choices = recommended_guess
            g.make_guess(recommended_guess)
        evaluation = g.get_evaluation()
        print(g)
        game_ai.cull_possibilities(choices, evaluation.get_evaluation())
        if g.get_status() == "Won":
            print("Well done, you have won.")
            break

    if g.get_status() != "Won":
        print("The answer was {}".format(g.get_answer()))
        print("Sorry, you failed this time.")


def play_game_ai(answer, game_ai, g):
    g.pick_answer(answer)
    while g.get_level() < 7:
        if g.get_level() == 1:
            recommended_guess = MastermindConstants.starting_recommendation
        else:
            recommended_guess = game_ai.smart_eval(debug=False)
        g.make_guess(recommended_guess)
        game_ai.cull_possibilities(recommended_guess, g.get_evaluation())
        if g.get_status() == "Won":
            break
    return g.get_status()


def iter_game_ai():
    """"
    Plays every single game (i.e. for each hidden answer possible)
    """
    i = 0
    wins = 0
    possibles = Answer.possible_answers()
    game_ai = GameAI()
    g = Game()
    for p in possibles:
        i += 1
        game_ai.reset()
        g.reset()
        status = play_game_ai(p, game_ai, g)
        if status == "Won":
            wins += 1
        print("{} / {} wins".format(wins, i))


if __name__ == "__main__":
    iter_game_ai()
