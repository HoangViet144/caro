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


def heuristic(currBoard, playerID,x,y):
    score = 0
    # _4AI = currBoard.cntNContinuous(Player.AI,4,1) + currBoard.cntNContinuous(Player.AI,4,2)
    # _4HU = currBoard.cntNContinuous(Player.HUMAN,4,1) + currBoard.cntNContinuous(Player.HUMAN,4,2)
    # open3AI = currBoard.cntNContinuous(Player.AI,3,1)
    # open3HU = currBoard.cntNContinuous(Player.HUMAN,3,1)
    # half3AI = currBoard.cntNContinuous(Player.AI,3,2)
    # half3HU = currBoard.cntNContinuous(Player.HUMAN,3,2)
    # open2AI = currBoard.cntNContinuous(Player.AI,2,1)
    # open2HU = currBoard.cntNContinuous(Player.HUMAN,2,1)
    # half2AI = currBoard.cntNContinuous(Player.AI,2,2)
    # half2HU = currBoard.cntNContinuous(Player.HUMAN,2,2)

    if (currBoard.isWin(Player.AI)):
        score += 999_999_999
    if (currBoard.isWin(Player.HUMAN)):
        score -= 999_999_999
    
    '''
    #Xet chan
    #Viet them ham def BoundedTwoBy(x,y) bên board trả về kiểu int là số đường 2 bị chặn bởi (x,y)
    #Viet them ham def BoundedThreeBy(x,y) bên board trả về kiểu int là số đường 3 bị chặn bởi (x,y)
    # score += BoundedTwoBy(x,y)*999_999
    # score += BoundedThreeBy(x,y)*9_999_999
    '''
    


    # # score += 6000*(_4AI - _4HU)+\
    # #     500*(open3AI-open3HU) + 200*(half3AI - half3HU) +\
    # #     50*(open2AI - open2HU) + 10*(half2AI - half2HU)
    # # return score
    # # if (currBoard.isWin(Player.AI)):
    # #     score += 6000
    # # if (currBoard.isWin(Player.HUMAN)):
    # #     score -= 6000

    # score = 0
    # # if (currBoard.isWin(Player.AI)):
    # #     score += 99_999_999
    # # if (currBoard.isWin(Player.HUMAN)):
    # #     score -= 99_999_999
    score += int(currBoard.countThreeContinousNoBound(Player.AI)) * \
        4*4*4 + 100*100
    score += int(currBoard.countThreeContinousBound(Player.AI))*4*4*4

    # twoContiAI = int(currBoard.countTwoContinousNoBound(
    #     Player.AI)) + int(currBoard.countTwoContinousBound(Player.AI))
    # score += twoContiAI*2*2
    score += int(currBoard.countTwoContinousNoBound(Player.AI))*2*2
    score += int(currBoard.countTwoContinousBound(Player.AI))*2*2

    score -= int(currBoard.countTwoContinousNoBound(Player.HUMAN)
                 )*4*4*4 + 1000
    score -= int(currBoard.countTwoContinousBound(Player.HUMAN))*4*4*4

    # twoContiHU = int(currBoard.countTwoContinousNoBound(
    #     Player.HUMAN)) + int(currBoard.countTwoContinousBound(Player.HUMAN))
    # score -= twoContiHU*2*2
    score -= int(currBoard.countThreeContinousNoBound(Player.HUMAN))*2*2
    score -= int(currBoard.countThreeContinousBound(Player.HUMAN))*2*2

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
                    tempVal = minValue(currBoard.set(
                        action[0], action[1], player), not player, currDepth, action, node)
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
                    tempVal = maxValue(currBoard.set(
                        action[0], action[1], player), not player, currDepth + 1, action, node)
                    # node.children.append(tempNode)
                    val = min(val, tempVal)
                # print("Minimax-->MIN agent: Visited node = ", currAction, ", Value = ", val)
            node.value += ' ' + str(val)
            parent.children.append(node)
            return val

        # Initial call:
        act = board.getEmptySpace()[0]
        root = Node()
        maxVal = minValue(
            board.set(act[0], act[1], self.player), not self.player, 0, act, root)
        for action in board.getEmptySpace():
            if action == board.getEmptySpace()[0]:
                continue
            currVal = minValue(
                board.set(action[0], action[1], self.player), not self.player, 0, action, root)
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
