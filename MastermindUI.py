from tkinter import Tk, Canvas, Frame, Button, BOTH, TOP, BOTTOM, Toplevel
from Game import Game
from GameAI import GameAI
import GameAIUI
import MastermindConstants

MARGIN = 20  # Pixels around the board
SIDE = 50  # Width of every board cell. Smaller squares are half size
WIDTH = MARGIN * 2 + SIDE * 5
HEIGHT = MARGIN * 2 + SIDE * 6
colors = {'Y': "yellow", 'O': "orange", 'P': "purple", 'B': "blue", 'R': "red", 'G': "green", 'E': "white"}
eval_colors = {'B': "black", 'W': "gray", 'E': "white"}


class MastermindError(Exception):
    """
    An application specific error.
    """
    pass


class MastermindUI(Frame):
    """
    The Tkinter UI, responsible for drawing the board and accepting user input.
    """

    def init_grids(self):
        self.grid = [['E', 'E', 'E', 'E'],
                     ['E', 'E', 'E', 'E'],
                     ['E', 'E', 'E', 'E'],
                     ['E', 'E', 'E', 'E'],
                     ['E', 'E', 'E', 'E'],
                     ['E', 'E', 'E', 'E']]
        self.evaluationGrid = [['E', 'E', 'E', 'E'],
                               ['E', 'E', 'E', 'E'],
                               ['E', 'E', 'E', 'E'],
                               ['E', 'E', 'E', 'E'],
                               ['E', 'E', 'E', 'E'],
                               ['E', 'E', 'E', 'E']]

    def __init__(self, parent, game, ai):
        self.game = game
        self.ai = ai
        Frame.__init__(self, parent)
        self.parent = parent
        self.grid = []
        self.evaluationGrid = []
        self.init_grids()

        self.row, self.col = 5, 0

        self.newWindow = Toplevel(self.parent)
        self.aiApp = GameAIUI.GameAIUI(self.newWindow, self.ai)

        self.__init_ui()

    def __init_ui(self):
        self.parent.title("Mastermind")  # Set Window Title
        self.pack(fill=BOTH)
        self.canvas = Canvas(self,
                             width=WIDTH,
                             height=HEIGHT)
        self.canvas.pack(fill=BOTH, side=TOP)
        submit_button = Button(self,
                               text="Clear Answers",
                               command=self.__clear_answers)
        submit_button.pack(fill=BOTH, side=BOTTOM)

        self.__draw_grid()
        self.__draw_puzzle()
        self.__draw_cursor()
        self.canvas.focus_set()

        self.canvas.bind("<Button-1>", self.__cell_clicked)
        self.canvas.bind("<Key>", self.__key_pressed)
        self.canvas.bind("<Return>", self.__submit_answers)
        self.canvas.bind("<Left>", self.__left_key)
        self.canvas.bind("<Right>", self.__right_key)
        self.canvas.bind("<space>", self.__clear_cell)

    def __draw_grid(self):
        color = "white"

        for i in range(12):
            for j in range(2):
                self.canvas.create_rectangle(MARGIN + j * SIDE / 2, MARGIN + i * SIDE / 2,
                                             MARGIN + j * SIDE / 2 + SIDE / 2,
                                             MARGIN + i * SIDE / 2 + SIDE / 2, fill=color)

        color = "white"
        for i in range(6):
            for j in range(4):
                self.canvas.create_rectangle(MARGIN + j * SIDE + SIDE, MARGIN + i * SIDE,
                                             MARGIN + j * SIDE + SIDE + SIDE,
                                             MARGIN + i * SIDE + SIDE, fill=color)

    def __draw_puzzle(self):
        self.canvas.delete("numbers")

        for i in range(6):
            for j in range(4):
                answer = self.grid[i][j]
                color = colors[answer]
                self.canvas.create_rectangle(MARGIN + j * SIDE + SIDE, MARGIN + i * SIDE,
                                             MARGIN + j * SIDE + SIDE + SIDE,
                                             MARGIN + i * SIDE + SIDE, fill=color)
        for i in range(6):
            for j in range(2):
                eval_answer = self.evaluationGrid[i][j]
                color = eval_colors[eval_answer]
                self.canvas.create_rectangle(MARGIN + j * SIDE / 2, MARGIN + i * SIDE,
                                             MARGIN + j * SIDE / 2 + SIDE / 2,
                                             MARGIN + i * SIDE + SIDE / 2, fill=color)
        for i in range(6):
            for j in range(2, 4):
                eval_answer = self.evaluationGrid[i][j]
                color = eval_colors[eval_answer]
                _j = j - 2
                self.canvas.create_rectangle(MARGIN + _j * SIDE / 2, MARGIN + i * SIDE + SIDE / 2,
                                             MARGIN + _j * SIDE / 2 + SIDE / 2,
                                             MARGIN + i * SIDE + SIDE, fill=color)

    def __draw_cursor(self):
        self.canvas.delete("cursor")

        if self.row >= 0 and self.col >= 0:
            x0 = MARGIN + SIDE + self.col * SIDE + 1
            y0 = MARGIN + self.row * SIDE + 1
            x1 = MARGIN + SIDE + (self.col + 1) * SIDE - 1
            y1 = MARGIN + (self.row + 1) * SIDE - 1
            self.canvas.create_rectangle(
                x0, y0, x1, y1,
                outline="red", tags="cursor"
            )

    def __draw_victory(self):
        # create a oval (which will be a circle)
        x0 = y0 = MARGIN + SIDE * 1
        x1 = y1 = MARGIN + SIDE * 4
        self.canvas.create_oval(
            x0, y0, x1, y1,
            tags="ending", fill="dark orange", outline="orange"
        )
        # create text
        x = y = MARGIN + 2 * SIDE + SIDE / 2
        self.canvas.create_text(
            x, y,
            text="You win! \nIt took {} seconds".format(self.game.get_time_elapsed()), tags="ending",
            fill="white", font=("Arial", 12)
        )

    def __draw_defeat(self):
        # create a oval (which will be a circle)
        x0 = y0 = MARGIN + SIDE * 1
        x1 = y1 = MARGIN + SIDE * 4
        self.canvas.create_oval(
            x0, y0, x1, y1,
            tags="ending", fill="dark red", outline="red"
        )
        # create text
        x = y = MARGIN + 2 * SIDE + SIDE / 2
        self.canvas.create_text(
            x, y,
            text="You lose! \nIt took {} seconds".format(self.game.get_time_elapsed()), tags="ending",
            fill="white", font=("Arial", 12)
        )

    def __cell_clicked(self, event):
        # if self.game.game_over:
        #    return
        x, y = event.x, event.y
        if MARGIN + SIDE < x < WIDTH - MARGIN and MARGIN < y < HEIGHT - MARGIN:

            # get row and col numbers from x,y coordinates
            row, col = int((y - MARGIN) / SIDE), int((x - MARGIN - SIDE) / SIDE)
            # if cell was selected already - deselect it
            if (row, col) == (self.row, self.col):
                self.row, self.col = -1, -1
            elif self.game.get_level() == 6 - row:
                self.row, self.col = row, col
        else:
            self.row, self.col = -1, -1

        self.__draw_cursor()

    def __clear_cell(self, _):
        if self.row >= 0 and self.col >= 0:
            self.grid[self.row][self.col] = 'E'
            self.__draw_puzzle()
            self.__draw_cursor()

    def __key_pressed(self, event):
        if self.row >= 0 and self.col >= 0 and len(event.char) == 1 and event.char in MastermindConstants.valid_keys:
            self.grid[self.row][self.col] = event.char
            # self.game.puzzle[self.row][self.col] = int(event.char)
            self.col, self.row = self.col + 1, self.row
            if self.col == 4:
                self.col, self.row = self.col - 1, self.row
            self.__draw_puzzle()
            self.__draw_cursor()

    def __right_key(self, _):
        if self.row >= 0 and 0 <= self.col < 3:
            self.col, self.row = self.col + 1, self.row
            self.__draw_puzzle()
            self.__draw_cursor()

    def __left_key(self, _):
        if self.row >= 0 and self.col > 0:
            self.col, self.row = self.col - 1, self.row
            self.__draw_puzzle()
            self.__draw_cursor()

    def __clear_answers(self):
        self.game.reset()
        self.game.pick_answer()
        self.init_grids()
        self.canvas.delete("ending")
        self.row, self.col = 5, 0
        self.__draw_puzzle()
        self.__draw_cursor()
        self.ai.reset()
        self.aiApp.reset()

    def __submit_answers(self, _):
        index = 6 - self.game.get_level()
        current_choices = self.grid[index]

        if 'E' in current_choices:
            return
        self.game.make_guess(current_choices)

        evaluation = self.game.get_evaluation()
        self.ai.cull_possibilities(current_choices, evaluation)
        self.evaluationGrid[index] = list(evaluation)
        self.col, self.row = 0, index - 1,
        self.__draw_puzzle()
        self.__draw_cursor()
        self.ai.smart_eval(debug=False)
        self.aiApp.update_selection()
        if self.game.get_status() == "Won":
            print("Well done, you have won.")
            self.__draw_victory()
            self.aiApp.update_selection()
        if self.game.get_level() == 7 and self.game.get_status() != "Won":
            print("Oh no, better luck next time")
            self.__draw_defeat()
            self.aiApp.update_selection()


if __name__ == '__main__':
    g = Game()
    gAI = GameAI()
    g.pick_answer()
    root = Tk()
    MastermindUI(root, g, gAI)
    root.geometry("%dx%d" % (WIDTH, HEIGHT + 40))
    root.mainloop()
