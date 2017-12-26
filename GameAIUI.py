# Shows a helpful AI User Interface
from tkinter import Canvas, Frame, BOTH, TOP

MARGIN = 20  # Pixels around the board
SIDE = 30  # Width of every board cell. Smaller squares are half size
NUM_ROWS = 20
WIDTH = MARGIN * 2 + SIDE * 8
HEIGHT = MARGIN * 3 + SIDE * NUM_ROWS
colors = {'Y': "yellow", 'O': "orange", 'P': "Purple", 'B': "blue", 'R': "red", 'G': "green", 'E': "white"}


class MastermindError(Exception):
    """
    An application specific error.
    """
    pass


class GameAIUI(Frame):
    """
    The Tkinter UI, responsible for drawing the board and accepting user input.
    """

    def init_grids(self):
        self.grid = []
        self.scores = []
        self.possible_answer_count = 1296
        for i in range(NUM_ROWS):
            self.grid.append(['E', 'E', 'E', 'E'])
            self.scores.append(0)

    def __init__(self, parent, ai):
        Frame.__init__(self, parent)
        self.parent = parent
        self.possible_answer_count = 1296
        self.ai = ai
        self.grid = []
        self.scores = []
        self.init_grids()
        self.__init_ui()

    def reset(self):
        self.init_grids()
        self.__draw_best_choices()

    def update_selection(self):
        selects = self.ai.get_selection(NUM_ROWS)
        self.possible_answer_count = len(self.ai.possibles)
        for i in range(0, len(selects)):
            pick = selects[i][0]
            self.scores[i] = selects[i][1]
            for j in range(0, 4):
                self.grid[i][j] = pick[j]

        for i in range(len(selects), NUM_ROWS):
            for j in range(0, 4):
                self.grid[i][j] = 'E'
                self.scores[i] = 0

        self.__draw_best_choices()

    def __init_ui(self):
        self.parent.title("Mastermind AI UI")  # Set Window Title
        self.pack(fill=BOTH)
        self.canvas = Canvas(self,
                             width=WIDTH,
                             height=HEIGHT)
        self.canvas.pack(fill=BOTH, side=TOP)

        self.__draw_grid()
        self.__draw_best_choices()
        self.canvas.focus_set()

    def __draw_grid(self):
        color = "white"
        for i in range(NUM_ROWS):
            for j in range(4):
                self.canvas.create_rectangle(MARGIN + j * SIDE, 2 * MARGIN + i * SIDE, MARGIN + j * SIDE + SIDE,
                                             2 * MARGIN + i * SIDE + SIDE, fill=color)
            self.canvas.create_rectangle(MARGIN + 5 * SIDE, 2 * MARGIN + i * SIDE, MARGIN + 5 * SIDE + 3 * SIDE,
                                         2 * MARGIN + i * SIDE + SIDE, fill=color)

    def __draw_best_choices(self):
        self.canvas.delete("numbers")
        for i in range(NUM_ROWS):
            for j in range(4):
                answer = self.grid[i][j]
                color = colors[answer]
                self.canvas.create_rectangle(MARGIN + j * SIDE, 2 * MARGIN + i * SIDE, MARGIN + j * SIDE + SIDE,
                                             2 * MARGIN + i * SIDE + SIDE, fill=color)
        for i in range(NUM_ROWS):
            number = self.scores[i]
            self.canvas.create_text(WIDTH - MARGIN - 1.5 * SIDE, 2 * MARGIN + i * SIDE + SIDE / 2,
                                    text="{}".format(number), tags="numbers", font=("Arial", 12))

        self.canvas.create_text(4 * MARGIN, MARGIN, text="{} available choices".format(self.possible_answer_count),
                                tags="numbers", font=("Arial", 10))
