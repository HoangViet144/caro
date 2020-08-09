import tkinter as tk
from functools import partial
import threading
import socket
from tkinter import messagebox
import argparse
import sys
from enum import Enum
import copy
import tkinter.font as tkFont
from PIL import Image, ImageTk

from agents import MultiAgentSearchAgent
from agents import MinimaxAgent
from agents import AlphaBetaAgent
from agents import LookupTableAgent


class Player():
    HUMAN = True
    AI = False


class StartScreen(tk.Tk):
    def __init__(self, agentType):
        super().__init__()
        self.title("Fight with AI Caro CSE HCMUT")
        self.geometry('700x500')
        self.agent = agentType

    def buildFrame(self):
        title = tk.Frame(self)
        title.pack()
        fontStyle = tkFont.Font(size=15)
        vnu = tk.Label(
            title, text="VIETNAM NATIONAL UNIVERSITY - HO CHI MINH CITY", font=tkFont.Font(size=14), foreground="blue").grid(row=0)
        hmcut = tk.Label(
            title, text="HO CHI MINH CITY UNIVERSITY OF TECHNOLOGY", font=tkFont.Font(size=14), foreground="blue").grid()
        cse = tk.Label(
            title, text="COMPUTER SCIENCE AND ENGINEERING FACULTY", foreground="blue").grid()
        imgFrame = tk.Frame(self)
        imgFrame.pack()
        image = Image.open("hcmut.png")
        image = image.resize((200, 200), Image.ANTIALIAS)
        self.my_img = ImageTk.PhotoImage(image)
        imgLabel = tk.Label(imgFrame, image=self.my_img)
        imgLabel.grid()
        body = tk.Frame(self)
        body.pack()
        subject = tk.Label(body, text="CO306A Introduction to AI").grid()
        _ = tk.Label(
            body, text="____________________________________________________________").grid()
        titleName = tk.Label(
            body, text="Implement Caro Game", font=tkFont.Font(size=20), foreground="red").grid()
        __ = tk.Label(
            body, text="____________________________________________________________").grid()
        a = tk.Label(body,
                     text="Choose what kind of play do you prefer:").grid(pady=20)
        optionFrame = tk.Frame(self)
        optionFrame.pack()
        onePlayerButton = tk.Button(optionFrame, text="1 player", width=10, command=partial(
            self.onePlayer))
        onePlayerButton.grid(row=11, column=0, padx=30)
        twoPlayerButton = tk.Button(optionFrame, text="2 player", width=10, command=partial(
            self.twoPlayer))
        twoPlayerButton.grid(row=11, column=1, padx=30)

    def onePlayer(self):
        self.destroy()
        board = BoardVisualizaion(self.agent, 1)
        board.buildFrame()
        board.frameControl.pack_forget()
        a = tk.Label(board.frameLabel,
                     text="Player 1 (YOU): X, Player 0 (AI): O. You play first!").grid()
        board.mainloop()

    def twoPlayer(self):
        self.destroy()
        board = BoardVisualizaion(self.agent, 2)
        board.buildFrame()
        a = tk.Label(board.frameLabel,
                     text="Player 1: X, Player 0: O. First player: Player1").grid()
        board.mainloop()


class BoardVisualizaion(tk.Tk):
    def __init__(self, agent, gameType, width=6, height=6):
        super().__init__()
        print(agent)
        if agent == "AlphabetAgent":
            self.agent = AlphaBetaAgent()
        else:
            self.agent = MinimaxAgent()
        self.gameType = gameType
        self.width = width
        self.height = height
        self.title("Fight with AI Caro CSE HCMUT")
        self.geometry('500x350')
        self.board = Board()
        self.button = [[2 for i in range(width)] for j in range(height)]
        self.currentTurn = 1
        self.prevTurn = 0
        self.validCurrentMove = True
        self.numOfTurn = 0

    def buildFrame(self):
        frameLabel = tk.Frame(self)
        frameLabel.pack()
        frameControl = tk.Frame(self)
        frameControl.pack()
        frameBoard = tk.Frame(self)
        frameBoard.pack()
        self.frameBoard = frameBoard
        self.frameControl = frameControl
        self.frameLabel = frameLabel

        switchButton = tk.Button(
            frameControl, text="Switch turn", width=10, command=partial(self.switchTurn))
        switchButton.grid(row=0, column=0, padx=30)
        for x in range(self.height):
            for y in range(self.width):
                self.button[x][y] = tk.Button(frameBoard, font=('arial', 15, 'bold'), height=1, width=2,
                                              borderwidth=2, command=partial(self.play, x=x, y=y))
                self.button[x][y].grid(row=x, column=y)

                self.button[x][y]['text'] = ""

    def switchTurn(self):
        if self.validCurrentMove:
            self.currentTurn ^= 1

    def play(self, x, y):
        if self.prevTurn == self.currentTurn:
            curTurn = "Not your turn. Current turn: hahaa"
            if self.currentTurn == 1:
                curTurn += "Player 1"
            else:
                curTurn += "Player 0"
            self.noti("", curTurn)
            return
        returnVal = self.board.makeMove(x, y, self.currentTurn)
        if returnVal >= 0:
            self.handleButton(x, y, self.currentTurn)
            if returnVal == 1:
                self.noti("Winner is", "Player 1")
                self.newGame()
                return
            elif returnVal == 0:
                self.noti("Winner is", "Player 0")
                self.newGame()
                return
            self.validCurrentMove = True
            self.prevTurn = self.currentTurn
        else:
            self.noti("", "not empty cell")
            self.validCurrentMove = False
            return
        print("c", self.currentTurn)
        if self.gameType == 1:
            print("Ai turn")
            if self.numOfTurn >= 2:
                x, y = self.agent.getLocation(self.board)
            else:
                naiveAgent = LookupTableAgent()
                x, y = naiveAgent.getLocation(self.board)
            self.handleButton(x, y, 0)
            self.numOfTurn += 1
            if self.board.makeMove(x, y, 0) == 0:
                self.noti("Winner is", "Player 0")
                self.newGame()
            self.prevTurn = 0
        print("board turn", self.board.currentTurn)
        print("visual turn", self.currentTurn)
        print("map", self.board.board)
        if self.board.isFull():
            self.noti("", "Draw!!!")
            self.newGame()

    def handleButton(self, x, y, playerId):
        if playerId == 1:
            self.button[x][y]['text'] = 'x'
            self.button[x][y]["foreground"] = 'red'
        else:
            self.button[x][y]['text'] = 'o'
            self.button[x][y]["foreground"] = 'blue'

    def noti(self, title, msg):
        messagebox.showinfo(str(title), str(msg))

    def newGame(self):
        for x in range(self.height):
            for y in range(self.width):
                self.button[x][y]['text'] = ""
        self.board.newGame()
        self.currentTurn = 1
        self.prevTurn = 0
        self.validCurrentMove = True
        self.numOfTurn = 0


class Board():
    def __init__(self,  width=6, height=6):
        # super().__init__()
        self.width = width
        self.height = height
        # self.title("Fight with AI Caro CSE HCMUT")
        # self.geometry('500x350')
        self.board = [[2 for i in range(width)] for j in range(height)]
        # self.button = [[2 for i in range(width)] for j in range(height)]
        self.currentTurn = 1

    def noti(self, title, msg):
        messagebox.showinfo(str(title), str(msg))

    def getEmptySpace(self):
        emp = []
        for i in range(self.width):
            for j in range(self.height):
                if self.board[i][j] == 2:
                    emp.append((i, j))
        return tuple(emp)

    def get(self, x, y):
        if x < 0 or x >= self.height or y < 0 or y >= self.width:
            # error position
            return -1
        return self.board[x][y]

    def newGame(self):
        for x in range(self.height):
            for y in range(self.width):
                self.board[x][y] = 2
        self.currentTurn = 1

    def set(self, x, y, playerId):
        """
        if self.currentTurn != playerId:
            # not playerId turn
            curTurn = "Not your turn. Current turn: "
            if self.currentTurn == 1:
                curTurn += "Player 1"
            else:
                curTurn += "Player 0000"
            self.noti("", curTurn)
            print("not your turn")
            print(self.currentTurn)
            return -1
        """
        if self.board[x][y] != 2:
            # cell not empty
            print("self not empty")
            return -1
        curBoard = copy.deepcopy(self)
        curBoard.board[x][y] = self.currentTurn
        return curBoard

    def makeMove(self, x, y, playerId):
        """
        if self.currentTurn != playerId:
            # not playerId turn
            curTurn = "Not your turn. Current turn: "
            if self.currentTurn == 1:
                curTurn += "Player 1"
            else:
                curTurn += "Player 0"
            self.noti("", curTurn)
            print("not your turn")
            return -1
        """
        if self.board[x][y] != 2:
            # cell not empty
            print("self not empty")
            return -1
        self.board[x][y] = self.currentTurn
        self.currentTurn ^= 1
        print(self.currentTurn)

        if self.isWin(playerId):
            if playerId == 1:
                return 1
            else:
                return 0
        return 2

    def isFull(self):
        for i in range(self.width):
            for j in range(self.height):
                if self.board[i][j] == 2:
                    return False
        return True

    def isEmpty(self):
        return not self.isFull()

    def isWin(self, playerId):
        for x in range(self.width):
            for y in range(self.height):
                # horizontal line
                cnt = 0
                ind = 0
                while ind + y < self.width:
                    if self.board[x][y+ind] != playerId:
                        break
                    cnt += 1
                    ind += 1
                ind = 1
                while y - ind >= 0:
                    if self.board[x][y-ind] != playerId:
                        break
                    cnt += 1
                    ind += 1
                if cnt >= 4:
                    return True
                # vertical line
                cnt = 0
                ind = 0
                while x + ind < self.height:
                    if self.board[x+ind][y] != playerId:
                        break
                    cnt += 1
                    ind += 1
                ind = 1
                while x - ind >= 0:
                    if self.board[x-ind][y] != playerId:
                        break
                    cnt += 1
                    ind += 1
                if cnt >= 4:
                    return True
                # diagonal line
                cnt = 0
                ind = 0
                while x + ind < self.height and y+ind < self.width:
                    if self.board[x+ind][y+ind] != playerId:
                        break
                    cnt += 1
                    ind += 1
                ind = 1
                while x - ind >= 0 and y - ind >= 0:
                    if self.board[x-ind][y-ind] != playerId:
                        break
                    cnt += 1
                    ind += 1
                if cnt >= 4:
                    return True
                # diagonal line
                cnt = 0
                ind = 0
                while x + ind < self.height and y-ind >= 0:
                    if self.board[x+ind][y-ind] != playerId:
                        break
                    cnt += 1
                    ind += 1
                ind = 1
                while x - ind >= 0 and y + ind < self.width:
                    if self.board[x-ind][y+ind] != playerId:
                        break
                    cnt += 1
                    ind += 1
                if cnt >= 4:
                    return True
        return False

    def isLose(self, playerId):
        return self.isWin(playerId ^ 1)

    def isThreeContinous(self, x, y, playerId, opt):
        # opt 1: no bound
        # opt 2: bound
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            return False

        # ngang
        cntBound = 0
        cnt = 0
        ind = 0
        while x + ind < self.width:
            if self.board[x+ind][y] != playerId:
                if self.board[x+ind][y] == playerId ^ 1:
                    cntBound += 1
                break
            cnt += 1
            ind += 1
        if x + ind == self.width:
            cntBound += 1
        ind = 1
        while x-ind >= 0:
            if self.board[x-ind][y] != playerId:
                if self.board[x-ind][y] == playerId ^ 1:
                    cntBound += 1
                break
            cnt += 1
            ind += 1
        if x - ind < 0:
            cntBound += 1
        if cnt >= 3 and opt == 1 and cntBound == 0:
            return True
        if cnt >= 3 and opt == 2 and cntBound == 1:
            return True

        # doc
        cntBound = 0
        cnt = 0
        ind = 0
        while y + ind < self.height:
            if self.board[x][y+ind] != playerId:
                if self.board[x][y+ind] == playerId ^ 1:
                    cntBound += 1
                break
            cnt += 1
            ind += 1
        if y + ind == self.height:
            cntBound += 1
        ind = 1
        while y-ind >= 0:
            if self.board[x][y-ind] != playerId:
                if self.board[x][y-ind] == playerId ^ 1:
                    cntBound += 1
                break
            cnt += 1
            ind += 1
        if y - ind < 0:
            cntBound += 1

        if cnt >= 3 and opt == 1 and cntBound == 0:
            return True
        if cnt >= 3 and opt == 2 and cntBound == 1:
            return True
        # cheo
        cntBound = 0
        cnt = 0
        ind = 0
        while x + ind < self.width and y+ind < self.height:
            if self.board[x+ind][y+ind] != playerId:
                if self.board[x+ind][y+ind] == playerId ^ 1:
                    cntBound += 1
                break
            cnt += 1
            ind += 1
        if x + ind == self.width or y+ind == self.height:
            cntBound += 1
        ind = 1
        while x-ind >= 0 and y - ind >= 0:
            if self.board[x-ind][y-ind] != playerId:
                if self.board[x-ind][y-ind] == playerId ^ 1:
                    cntBound += 1
                break
            cnt += 1
            ind += 1
        if x - ind < 0 or y-ind < 0:
            cntBound += 1

        if cnt >= 3 and opt == 1 and cntBound == 0:
            return True
        if cnt >= 3 and opt == 2 and cntBound == 1:
            return True

        # cheo
        cntBound = 0
        cnt = 0
        ind = 0
        while x + ind < self.width and y-ind >= 0:
            if self.board[x+ind][y-ind] != playerId:
                if self.board[x+ind][y-ind] == playerId ^ 1:
                    cntBound += 1
                break
            cnt += 1
            ind += 1
        if x + ind == self.width or y-ind < 0:
            cntBound += 1
        ind = 1
        while x-ind >= 0 and y + ind < self.width:
            if self.board[x-ind][y+ind] != playerId:
                if self.board[x-ind][y+ind] == playerId ^ 1:
                    cntBound += 1
                break
            cnt += 1
            ind += 1
        if x - ind < 0 or y+ind == self.width:
            cntBound += 1

        if cnt >= 3 and opt == 1 and cntBound == 0:
            return True
        if cnt >= 3 and opt == 2 and cntBound == 1:
            return True
        return False

    def isTwoContinous(self, x, y, playerId, opt):
        # opt 1: no bound
        # opt 2: bound
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            return False

        # ngang
        cntBound = 0
        cnt = 0
        ind = 0
        while x + ind < self.width:
            if self.board[x+ind][y] != playerId:
                if self.board[x+ind][y] == playerId ^ 1:
                    cntBound += 1
                break
            cnt += 1
            ind += 1
        if x + ind == self.width:
            cntBound += 1
        ind = 1
        while x-ind >= 0:
            if self.board[x-ind][y] != playerId:
                if self.board[x-ind][y] == playerId ^ 1:
                    cntBound += 1
                break
            cnt += 1
            ind += 1
        if x - ind < 0:
            cntBound += 1

        if cnt == 2 and opt == 1 and cntBound == 0:
            return True
        if cnt == 2 and opt == 2 and cntBound == 1:
            return True
        # doc
        cntBound = 0
        cnt = 0
        ind = 0
        while y + ind < self.height:
            if self.board[x][y+ind] != playerId:
                if self.board[x][y+ind] == playerId ^ 1:
                    cntBound += 1
                break
            cnt += 1
            ind += 1
        if y + ind == self.height:
            cntBound += 1
        ind = 1
        while y-ind >= 0:
            if self.board[x][y-ind] != playerId:
                if self.board[x][y-ind] == playerId ^ 1:
                    cntBound += 1
                break
            cnt += 1
            ind += 1
        if y - ind < 0:
            cntBound += 1

        if cnt == 2 and opt == 1 and cntBound == 0:
            return True
        if cnt == 2 and opt == 2 and cntBound == 1:
            return True
        # cheo
        cntBound = 0
        cnt = 0
        ind = 0
        while x + ind < self.width and y+ind < self.height:
            if self.board[x+ind][y+ind] != playerId:
                if self.board[x+ind][y+ind] == playerId ^ 1:
                    cntBound += 1
                break
            cnt += 1
            ind += 1
        if x + ind == self.width or y+ind == self.height:
            cntBound += 1
        ind = 1
        while x-ind >= 0 and y - ind >= 0:
            if self.board[x-ind][y-ind] != playerId:
                if self.board[x-ind][y-ind] == playerId ^ 1:
                    cntBound += 1
                break
            cnt += 1
            ind += 1
        if x - ind < 0 or y-ind < 0:
            cntBound += 1

        if cnt == 2 and opt == 1 and cntBound == 0:
            return True
        if cnt == 2 and opt == 2 and cntBound == 1:
            return True
        # cheo
        cntBound = 0
        cnt = 0
        ind = 0
        while x + ind < self.width and y-ind >= 0:
            if self.board[x+ind][y-ind] != playerId:
                if self.board[x+ind][y-ind] == playerId ^ 1:
                    cntBound += 1
                break
            cnt += 1
            ind += 1
        if x + ind == self.width or y-ind < 0:
            cntBound += 1
        ind = 1
        while x-ind >= 0 and y + ind < self.width:
            if self.board[x-ind][y+ind] != playerId:
                if self.board[x-ind][y+ind] == playerId ^ 1:
                    cntBound += 1
                break
            cnt += 1
            ind += 1
        if x - ind < 0 or y+ind == self.width:
            cntBound += 1

        if cnt == 2 and opt == 1 and cntBound == 0:
            return True
        if cnt == 2 and opt == 2 and cntBound == 1:
            return True
        return False

    def countThreeContinousNoBound(self, playerId):
        cnt = 0
        for i in range(self.height):
            for j in range(self.width):
                if self.isThreeContinous(i, j, playerId, 1):
                    cnt += 1
        return cnt/3

    def countThreeContinousBound(self, playerId):
        cnt = 0
        for i in range(self.height):
            for j in range(self.width):
                if self.isThreeContinous(i, j, playerId, 2):
                    cnt += 1
        return cnt/3

    def countTwoContinousNoBound(self, playerId):
        cnt = 0
        for i in range(self.height):
            for j in range(self.width):
                if self.isTwoContinous(i, j, playerId, 1):
                    cnt += 1
        return cnt/2

    def countTwoContinousBound(self, playerId):
        cnt = 0
        for i in range(self.height):
            for j in range(self.width):
                if self.isTwoContinous(i, j, playerId, 2):
                    cnt += 1
        return cnt/2


class Game:
    def __init__(self, agentType):
        self.curGame = StartScreen(agentType)

    def run(self):
        self.curGame.buildFrame()
        self.curGame.mainloop()


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
        game.run()
    else:
        print("invalid agent")
