import tkinter as tk
from functools import partial
import threading
import socket
from tkinter import messagebox

from enum import Enum
import copy


class Player():
    HUMAN = True
    AI = False


class Welcome(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Fight with AI Caro CSE HCMUT")
        self.geometry('375x150')

    def buildFrame(self):
        a = tk.Label(self,
                     text="Choose what kind of play do you prefer:").grid()
        onePlayerButton = tk.Button(self, text="1 player", width=10, command=partial(
            self.onePlayer))
        onePlayerButton.grid(column=0, row=2)
        twoPlayerButton = tk.Button(self, text="2 player", width=10, command=partial(
            self.twoPlayer))
        twoPlayerButton.grid(column=1, row=2)

    def onePlayer(self):
        self.destroy()
        board = Board()
        board.buildFrame()
        board.frameControl.pack_forget()
        a = tk.Label(board.frameLabel,
                     text="Player1 (YOU): X, Player2 (AI): O. You play first!").grid()
        board.mainloop()

    def twoPlayer(self):
        self.destroy()
        board = Board()
        board.buildFrame()
        a = tk.Label(board.frameLabel,
                     text="Player1: X, Player2: O. First player: Player1").grid()
        board.mainloop()


class Board(tk.Tk):
    def __init__(self, width=6, height=6):
        super().__init__()
        self.width = width
        self.height = height
        self.title("Fight with AI Caro CSE HCMUT")
        self.geometry('500x350')
        self.board = [[0 for i in range(width)] for j in range(height)]
        self.button = [[0 for i in range(width)] for j in range(height)]
        self.currentTurn = 1

    def buildFrame(self):
        self.frameLabel = tk.Frame(self)
        self.frameLabel.pack()

        frameControl = tk.Frame(self)
        frameControl.pack()
        frameBoard = tk.Frame(self)
        frameBoard.pack()
        self.frameBoard = frameBoard
        self.frameControl = frameControl

        switchButton = tk.Button(frameControl, text="Switch turn", width=10, command=partial(
            self.switchTurn))
        switchButton.grid(row=0, column=0, padx=30)
        for x in range(self.height):
            for y in range(self.width):
                self.button[x][y] = tk.Button(frameBoard, font=('arial', 15, 'bold'), height=1, width=2,
                                              borderwidth=2, command=partial(self.set, x=x, y=y, playerId=self.currentTurn))
                self.button[x][y].grid(row=x, column=y)

                self.button[x][y]['text'] = ""

    def switchTurn(self):

        for x in range(self.height):
            for y in range(self.width):
                if self.button[x][y]['text'] == "":
                    self.button[x][y] = tk.Button(self.frameBoard, font=('arial', 15, 'bold'), height=1, width=2,
                                                  borderwidth=2, command=partial(self.set, x=x, y=y, playerId=self.currentTurn))
                    self.button[x][y].grid(row=x, column=y)

                    self.button[x][y]['text'] = ""

    def newGame(self):
        for x in range(self.height):
            for y in range(self.width):
                self.button[x][y]['text'] = ""
                self.board[x][y] = 0
        self.currentTurn = 1

    def getEmptySpace(self):
        emp = []
        for i in range(self.width):
            for j in range(self.height):
                if self.board[i][j] == 0:
                    emp.append((i, j))
        return tuple(emp)

    def get(self, x, y):
        if x < 0 or x >= self.height or y < 0 or y >= self.width:
            # error position
            return -1
        return self.board[x][y]

    def noti(self, title, msg):
        messagebox.showinfo(str(title), str(msg))

    def set(self, x, y, playerId):
        if self.currentTurn != playerId:
            # not playerId turn
            curTurn = "Not your turn. Current turn: "
            if self.currentTurn == 1:
                curTurn += "Player 1"
            else:
                curTurn += "Player 2"
            self.noti("", curTurn)
            print("not your turn")
            return -1
        if self.board[x][y] != 0:
            # cell not empty
            print("self not empty")
            return -1

        self.board[x][y] = self.currentTurn
        if self.currentTurn == 1:
            self.button[x][y]['text'] = 'x'
            self.button[x][y]["foreground"] = 'red'
        else:
            self.button[x][y]['text'] = 'o'
            self.button[x][y]["foreground"] = 'blue'

        self.currentTurn = -self.currentTurn+3

        if self.isWin(playerId):
            if playerId == 1:
                self.noti("Winner is", "Player 1")
                self.newGame()
            else:
                self.noti("Winner is", "Player 2")

        return copy.deepcopy(self.board)

    def undo(self, playerId):
        pass

    def isFull(self, x, y):
        for i in range(self.width):
            for j in range(self.height):
                if self.board[i][j] == 0:
                    return False
        return True

    def isEmpty(self, x, y):
        return not self.isFull(x, y, playerId)

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
        return isWin(self, not playerId)

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
                if self.board[x+ind][y] == -playerId + 3:
                    cntBound += 1
                break
            cnt += 1
            ind += 1
        if x + ind == self.width:
            cntBound += 1
        ind = 1
        while x-ind >= 0:
            if self.board[x-ind][y] != playerId:
                if self.board[x-ind][y] == -playerId + 3:
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
                if self.board[x][y+ind] == -playerId + 3:
                    cntBound += 1
                break
            cnt += 1
            ind += 1
        if y + ind == self.height:
            cntBound += 1
        ind = 1
        while y-ind >= 0:
            if self.board[x][y-ind] != playerId:
                if self.board[x][y-ind] == -playerId + 3:
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
                if self.board[x+ind][y+ind] == -playerId + 3:
                    cntBound += 1
                break
            cnt += 1
            ind += 1
        if x + ind == self.width or y+ind == self.height:
            cntBound += 1
        ind = 1
        while x-ind >= 0 and y - ind >= 0:
            if self.board[x-ind][y-ind] != playerId:
                if self.board[x-ind][y-ind] == -playerId + 3:
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
                if self.board[x+ind][y-ind] == -playerId + 3:
                    cntBound += 1
                break
            cnt += 1
            ind += 1
        if x + ind == self.width or y-ind < 0:
            cntBound += 1
        ind = 1
        while x-ind >= 0 and y + ind < self.width:
            if self.board[x-ind][y+ind] != playerId:
                if self.board[x-ind][y+ind] == -playerId + 3:
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

    def isTwoContinous(self, x, y, playerId):
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
                if self.board[x+ind][y] == -playerId + 3:
                    cntBound += 1
                break
            cnt += 1
            ind += 1
        if x + ind == self.width:
            cntBound += 1
        ind = 1
        while x-ind >= 0:
            if self.board[x-ind][y] != playerId:
                if self.board[x-ind][y] == -playerId + 3:
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
                if self.board[x][y+ind] == -playerId + 3:
                    cntBound += 1
                break
            cnt += 1
            ind += 1
        if y + ind == self.height:
            cntBound += 1
        ind = 1
        while y-ind >= 0:
            if self.board[x][y-ind] != playerId:
                if self.board[x][y-ind] == -playerId + 3:
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
                if self.board[x+ind][y+ind] == -playerId + 3:
                    cntBound += 1
                break
            cnt += 1
            ind += 1
        if x + ind == self.width or y+ind == self.height:
            cntBound += 1
        ind = 1
        while x-ind >= 0 and y - ind >= 0:
            if self.board[x-ind][y-ind] != playerId:
                if self.board[x-ind][y-ind] == -playerId + 3:
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
                if self.board[x+ind][y-ind] == -playerId + 3:
                    cntBound += 1
                break
            cnt += 1
            ind += 1
        if x + ind == self.width or y-ind < 0:
            cntBound += 1
        ind = 1
        while x-ind >= 0 and y + ind < self.width:
            if self.board[x-ind][y+ind] != playerId:
                if self.board[x-ind][y+ind] == -playerId + 3:
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


if __name__ == "__main__":
    board = Welcome()
    board.buildFrame()
    board.mainloop()
