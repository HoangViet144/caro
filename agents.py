#from game import Board
from copy import deepcopy

class Player():
    HUMAN = True
    AI = False

class Node:
    def __init__(self, value=None, children=None):
        if children is None:
            children = []
        self.value, self.children = value, children

def pprint_tree(node, file=None, _prefix="", _last=True):
    print(_prefix, "`- " if _last else "|- ", node.value, sep="", file=file)
    _prefix += "   " if _last else "|  "
    child_count = len(node.children)
    for i, child in enumerate(node.children):
        _last = i == (child_count - 1)
        pprint_tree(child, file, _prefix, _last)

def heuristic(currBoard, playerID):
    score = 0
    if (playerID == Player.HUMAN):
        score += 1
    else:
        score -= 1
    if (currBoard.isWin(playerID)):
        if (playerID == Player.HUMAN):
            score += 99_999_999
        else:
            score -= 99_999_999

    for i in range(int(currBoard.countThreeContinousNoBound(playerID))):
        if (playerID == Player.HUMAN):
            score += 10000
        else:
            score -= 10000

    for i in range(int(currBoard.countThreeContinousBound(playerID))):
        if (playerID == Player.HUMAN):
            score += 800
        else:
            score -= 800

    for i in range(int(currBoard.countTwoContinousNoBound(playerID))):
        if (playerID == Player.HUMAN):
            score += 250
        else:
            score -= 250

    for i in range(int(currBoard.countTwoContinousBound(playerID))):
        if (playerID == Player.HUMAN):
            score += 100
        else:
            score -= 100

    return score


class MultiAgentSearchAgent():

    def __init__(self, depth='1'):
        self.player = Player.AI
        self.evaluationFunction = heuristic
        self.depth = int(depth)


class LookupTableAgent(MultiAgentSearchAgent):
    def getLocation(self, board):
        empty = board.getEmptySpace()
        print("empty", empty)
        width = board.width
        height = board.height
        lookupValue = [[height//2, width//2],
                       [height//2, width//2+1], [height//2, width//2-1],
                       [height//2+1, width//2], [height//2-1, width//2],
                       [height//2-1, width//2-1], [height//2+1, width//2+1],
                       [height//2, width-1], [height-1, width//2],
                       [0, width//2], [height//2, 0],
                       [0, 0], [height-1, width-1]]
        for act in lookupValue:
            if tuple(act) in empty:
                print(act)
                return act


class MinimaxAgent(MultiAgentSearchAgent):

    def getLocation(self, board):
        def maxValue(currBoard, player, currDepth, currAction, parent):
            node = Node(value=str(currAction))
            if currDepth >= self.depth or currBoard.isWin(player) or currBoard.isLose(player):
                val = self.evaluationFunction(currBoard, player)
                # return 
            else:
                val = -99_999_999
                for action in currBoard.getEmptySpace():
                    tempVal = minValue(currBoard.set(action[0], action[1], player), not player, currDepth, action, node)
                    # node.children.append(tempNode)
                    val = max(val, tempVal)
                # print("Minimax-->MAX agent: Visited node = ", currAction, ", Value = ", val)
            node.value += ' ' + str(val)
            parent.children.append(node)
            return val

        def minValue(currBoard, player, currDepth, currAction, parent):
            node = Node(value=str(currAction))
            if currDepth >= self.depth or currBoard.isWin(player) or currBoard.isLose(player):
                val = self.evaluationFunction(currBoard, player)
                # return 
            else:
                val = 99_999_999
                for action in currBoard.getEmptySpace():
                    tempVal = maxValue(currBoard.set(action[0], action[1], player), not player, currDepth + 1, action, node)
                    # node.children.append(tempNode)
                    val = min(val, tempVal)
                # print("Minimax-->MIN agent: Visited node = ", currAction, ", Value = ", val)
            node.value += ' ' + str(val)
            parent.children.append(node)
            return val

        # Initial call:
        act = board.getEmptySpace()[0]
        root = Node()
        maxVal = minValue(board.set(act[0], act[1], self.player), not self.player, 0, act, root)
        for action in board.getEmptySpace():
            if action == board.getEmptySpace()[0]:
                continue
            currVal = minValue(board.set(action[0], action[1], self.player), not self.player, 0, action, root)
            if currVal > maxVal:
                maxVal = currVal
                act = action
        root.value = str(act) + ' ' + str(maxVal)
        pprint_tree(root)
        return act


class AlphaBetaAgent(MultiAgentSearchAgent):
    def getLocation(self, board):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "* YOUR CODE HERE *"
        def maxValue(currBoard, player, currDepth, alpha, beta):
            if currDepth >= self.depth or currBoard.isWin(player) or currBoard.isLose(player):
                return self.evaluationFunction(currBoard, player)
            val = -99_999_999
            for action in currBoard.getEmptySpace():
                val = max(val, minValue(currBoard.set(
                    action[0], action[1], player), not player, currDepth, alpha, beta))

                if val > beta:
                    return val
                alpha = max(val, alpha)
            return val

        def minValue(currBoard, player, currDepth, alpha, beta):
            if currDepth >= self.depth or currBoard.isWin() or currBoard.isLose():
                return self.evaluationFunction(currBoard, player)
            val = 99_999_999
            for action in currBoard.getEmptySpace():
                val = min(val, maxValue(currBoard.set(
                    action[0], action[1], player), not player, currDepth + 1, alpha, beta))

                if val < alpha:
                    return val
                beta = min(val, beta)
            return val

        val = -99_999_999
        alpha = -99_999_999
        beta = 99_999_999
        act = board.getEmptySpace()[0]
        for action in board.getEmptySpace():
            currVal = minValue(board.currBoard.set(
                action[0], action[1], self.player), not self.player, 0, alpha, beta)
            if currVal > val:
                act = action
                val = currVal

                alpha = max(val, alpha)

        return act
