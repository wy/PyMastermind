# PyMastermind
Python UI Game and simple AI for Mini Mastermind

## Overview

PyMastermind is a Python game to play a classic game called Mini Mastermind that came out in the 1970s.
Mini Mastermind is a logic + guessing game where the objective is to figure out a sequence of 4 pegs (each peg can be one of 6 different colour variants: Red, Green, Orange, Blue, Purple and Yellow).
You get the chance to make 6 guesses. After each guess (of a sequence of 4), the opponent evaluates your guess against the hidden sequence.

The evaluation is as follows:

* If you have a peg in the right place and right colour, then you get a black peg (Black in the game)
* If you have a peg in the wrong place but right colour, then you get a white peg (Gray in the game)
* Otherwise, you get no pegs

They then show you the black and white pegs you got, note: the sequence of Black, White or Empty does not tell you anything (it's unordered).

If you cannot guess the sequence by the 6th guess, then you lose. If you get it right, you win.

## Playing the Game

```bash
$ python MastermindUI.py
```
<p align="center">
  
  <img 
    src="Mastermind UI.PNG" 
    width="100%">
</p>


* You must use Capital Letters: R, G, Y, O, B, P.
* You can use the Left and Right arrow keys to move left and right
* You can remove a Peg by pressing <Spacebar>
* Press Enter once you have made your 4 Peg Selections
* The evaluation is Black, Gray, or Empty.
* You can reset the game by pressing Clear Answers

## System Requirements

* Python 3.*

## Code Layout

* `Guess.py` - Defines the Guess Object, which is simply a sequence of 4 pegs
* `Answer.py` - Defines the Answer Object, which is simply a sequence of 4 pegs. Also allows you to generate a random answer too.
* `Evaluation.py` - Evalutes a guess vs answer, returning the Black, White or Empty sequence.
* `Game.py` - Holds the Game State, allowing you to make guesses, evaluate them and figure out if you've won or lost
* `GameCLI.py` - Command-Line Interface version of Gameplay. Has 3 options (1 - You guess the Computer's answer, 2 - You vs. Friend, 3 - Computer AI vs. You)
* `MastermindConstraints.py` - Constants used throughout
* `GameAI.py` - AI implementation using process of elimination and heuristics to rank possible next moves
* `MastermindUI.py` - Mastermind User Interface which is a Tk Windowed Interface for playing vs. Computer's answer
* `GameAIUI.py` - AI User Interface which shows you the best next options

## Game AI

One of the interesting parts of the Game is how to code the AI.
I used the following approach to understand it intuitively:

* Initially there are 6^4 = 1296 possible answers (trivial: 6 colours for each peg, and 4 pegs)
* After each guess, you will get one of a number of evaluations
* Since there a fixed number of evaluations, then you can think of each evaluation corresponding to a set of answers that will give that evaluation for that guess
* If any of the answers does not give that evaluation, then they are no longer possible (and you can remove those answers)
* After each step, the number of possible answers is reducing

The logic of the Next Move Selection:
* For each guess:
** Create a mapping from the evaluation -> number of answers such that eval(guess,answer) = evaluation
** Score(guess) = max length of the number of answers in your mapping
* Pick the guess that minimises Score(guess)

The idea is that you pick the guess such that in the worst case (where the evaluation still leaves the most number of possible answers), it is the lowest amongst all guess possibilities.

Later on, I made an additional tweak to also calculate Expected(guess) = Sum of Score^2/Total Answers



