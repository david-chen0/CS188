# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util, math

from game import Agent

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        minGhostDist = math.inf
        for ghost in newGhostStates:
            x, y = ghost.getPosition()
            if ghost.scaredTimer == 0:
                minGhostDist = min(minGhostDist, manhattanDistance(newPos, (x, y)))
        if minGhostDist == 0:
            return -1 * math.inf

        minFoodDist = math.inf
        foods = successorGameState.getFood().asList()
        if not foods:
            return math.inf
        for food in foods:
            minFoodDist = min(minFoodDist, manhattanDistance(newPos, food))
        
        return successorGameState.getScore() + (2 / minFoodDist) - (5 / minGhostDist)

def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

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

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        legalActions = gameState.getLegalActions(0)
        successors = [gameState.generateSuccessor(0, action) for action in legalActions]
        results = [self.minimize(successor, 0, 1) for successor in successors]
        maxIndex = results.index(max(results))
        return legalActions[maxIndex]

    def maximize(self, gameState, depth):
        if depth == self.depth or gameState.isLose() or gameState.isWin():
            return self.evaluationFunction(gameState)

        legalActions = gameState.getLegalActions(0)
        successors = [gameState.generateSuccessor(0, action) for action in legalActions]
        results = [self.minimize(successor, depth, 1) for successor in successors]
        return max(results)

    def minimize(self, gameState, depth, agent):
        if depth == self.depth or gameState.isLose() or gameState.isWin():
            return self.evaluationFunction(gameState)
        
        legalActions = gameState.getLegalActions(agent)
        successors = [gameState.generateSuccessor(agent, action) for action in legalActions]
        if agent == gameState.getNumAgents() - 1:
            results = [self.maximize(successor, depth + 1) for successor in successors]
        else:
            results = [self.minimize(successor, depth, agent + 1) for successor in successors]
        return min(results)


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        score = -1 * math.inf
        alpha = -1 * math.inf
        beta = math.inf
        bestAction = []

        legalActions = gameState.getLegalActions(0)
        for action in legalActions:
            successor = gameState.generateSuccessor(0, action)
            actionScore = self.minimize(successor, 0, 1, alpha, beta)
            if actionScore > score:
                score = actionScore
                bestAction = action
            alpha = max(alpha, actionScore)
        return bestAction

    def maximize(self, gameState, depth, alpha, beta):
        if depth == self.depth or gameState.isLose() or gameState.isWin():
            return self.evaluationFunction(gameState)

        legalActions = gameState.getLegalActions(0)
        v = -1 * math.inf
        for action in legalActions:
            successor = gameState.generateSuccessor(0, action)
            actionScore = self.minimize(successor, depth, 1, alpha, beta)
            v = max(v, actionScore)
            if v > beta:
                return v
            alpha = max(alpha, v)
        return v  

    def minimize(self, gameState, depth, agent, alpha, beta):
        if depth == self.depth or gameState.isLose() or gameState.isWin():
            return self.evaluationFunction(gameState)

        legalActions = gameState.getLegalActions(agent)
        v = math.inf
        for action in legalActions:
            successor = gameState.generateSuccessor(agent, action)
            if agent == gameState.getNumAgents() - 1:
                value = self.maximize(successor, depth + 1, alpha, beta)
            else:
                value = self.minimize(successor, depth, agent + 1, alpha, beta)
            v = min(v, value)
            if v < alpha:
                return v
            beta = min(beta, v)
        return v

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        legalActions = gameState.getLegalActions(0)
        successors = [gameState.generateSuccessor(0, action) for action in legalActions]
        results = [self.calcExpected(successor, 0, 1) for successor in successors]
        maxIndex = results.index(max(results))
        return legalActions[maxIndex]

    def calcExpected(self, gameState, depth, agent):
        if depth == self.depth or gameState.isLose() or gameState.isWin():
            return self.evaluationFunction(gameState)

        legalActions = gameState.getLegalActions(agent)
        successors = [gameState.generateSuccessor(agent, action) for action in legalActions]
        numAgents = gameState.getNumAgents()
        results = [self.calcExpected(successor, depth + (agent == numAgents - 1), (agent + 1) % numAgents) for successor in successors]
        if agent == 0:
            return max(results)
        return sum(results) / len(results)

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    newPos = currentGameState.getPacmanPosition()
    newFood = currentGameState.getFood()
    newGhostStates = currentGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

    minGhostDist = math.inf
    for ghost in newGhostStates:
        x, y = ghost.getPosition()
        if ghost.scaredTimer == 0:
            minGhostDist = min(minGhostDist, manhattanDistance(newPos, (x, y)))

    minFoodDist = math.inf
    foods = currentGameState.getFood().asList()
    for food in foods:
        minFoodDist = min(minFoodDist, manhattanDistance(newPos, food))
    
    return currentGameState.getScore() + (2 / minFoodDist) - (5 / (minGhostDist + 1))

# Abbreviation
better = betterEvaluationFunction
