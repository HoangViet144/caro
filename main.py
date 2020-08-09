from PIL import Image, ImageTk
import copy
from enum import Enum
from tkinter import messagebox
import socket
import threading
from functools import partial
import tkinter as tk
from game import Welcome
from agents import Player
from agents import MultiAgentSearchAgent
from agents import MinimaxAgent
from agents import AlphaBetaAgent


class Game:
    def __init__(self, agentType):
        if agentType == "MinimaxAgent":
            self.agent = MinimaxAgent()
        else:
            self.agent = AlphaBetaAgent()
        self.board = Board(self.agent)

    def run(self):
        self.board.buildFrame()
        self.board.mainloop()


def readCommand():
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--agents',
                        required=True,
                        help='Agents type: MinimaxAgent, AlphabetaAgent.')
    return parser


if __name__ == "__main__":
    try:
        options = readCommand().parse_args()
    except:
        readCommand().print_help()
        sys.exit(0)
    if options.agents == 'MinimaxAgent' or options.agents == "AlphabetaAgent":
        game = Game(options.agents)
    else:
        print("invalid agent")
