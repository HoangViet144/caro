from game import Board
class Player():
    HUMAN = True
    AI = False

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn, depth = '5'):
        self.player = Player.AI
        self.evaluationFunction = evalFn
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):

    def getLocation(self, board):
        def maxValue(currBoard, player, currDepth):
            if currDepth >= self.depth or currBoard.isWin(player) or currBoard.isLose(player):
                return self.evaluationFunction(currBoard)
            val = -99_999_999
            for action in currBoard.getEmptySpace():
                val = max(val, minValue(currBoard.set(action[0], action[1], player), not player, currDepth))
            return val

        def minValue(currBoard, player, currDepth):
            if currDepth >= self.depth or currBoard.isWin(player) or currBoard.isLose(player):
                return self.evaluationFunction(currBoard)
            val = 99_999_999
            for action in currBoard.getEmptySpace():
                val = min(val, maxValue(currBoard.set(action[0], action[1], player), not player, currDepth + 1))
            return val

        # Initial call:
        act = board.getEmptySpace()[0]
        maxVal = minValue(board.set(act[0], act[1], self.player), self.evaluationFunction, not self.player, 0)
        for action in board.getEmptySpace(0):
            if action == board.getEmptySpace(0)[0]:
                continue
            currVal = minValue(board.set(action[0], action[1], self.player), self.evaluationFunction, not self.player, 0)
            if currVal > maxVal:
                maxVal = currVal
                act = action

        return act

class AlphaBetaAgent(MultiAgentSearchAgent):
    def getLocation(self, board):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        def maxValue(currBoard, player, currDepth, alpha, beta):
            if currDepth >= self.depth or currBoard.isWin(player) or currBoard.isLose(player):
                return self.evaluationFunction(currBoard)
            val = -99_999_999
            for action in currBoard.getEmptySpace():
                val = max(val, minValue(currBoard.set(action[0], action[1], player), not player, currDepth, alpha, beta))
               
                if val > beta:
                    return val
                alpha = max(val, alpha)
            return val

        def minValue(currBoard, player, currDepth, alpha, beta):
            if currDepth >= self.depth or currBoard.isWin() or currBoard.isLose():
                return self.evaluationFunction(currBoard)
            val = 99_999_999
            for action in currBoard.getEmptySpace():
                val = min(val, maxValue(currBoard.set(action[0], action[1], player), not player, currDepth + 1, alpha, beta))    
            
                if val < alpha:
                    return val
                beta = min(val, beta)
            return val

        val = -99_999_999
        alpha = -99_999_999
        beta = 99_999_999
        act = board.getEmptySpace()[0]
        for action in board.getEmptySpace():
            currVal = minValue(board.currBoard.set(action[0], action[1], self.player), not self.player, 0, alpha, beta)
            if currVal > val:
                act = action
                val = currVal
                
                alpha = max(val, alpha)
        
        return act

def heuristic(currBoard,playerID):
    score = 0
    if (playerID==Player.HUMAN):
        score+=1
    else:
        score-=1
    if (currBoard.isWin(playerID)):
        if (playerID==Player.HUMAN):
            score+=99_999_999
        else:
            score-=99_999_999
    
    for i in range(currBoard.countThreeContinousNoBound(playerID)):
        if (playerID==Player.HUMAN):
            score+=100
        else:
            score-=100

    for i in range(currBoard.countThreeContinousBound(playerID)):
        if (playerID==Player.HUMAN):
            score+=80
        else: 
            score-=80
    
    for i in range(currBoard.countTwoContinousNoBound(playerID)):
        if (playerID==Player.HUMAN):
            score+=30
        else:
            score-=30
    
    for i in range(currBoard.countTwoContinousBound(playerID)):
        if (playerID==Player.HUMAN):
            score+=10
        else:
            score-=10
    

    return score