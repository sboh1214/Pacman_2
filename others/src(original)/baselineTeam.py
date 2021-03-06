
from captureAgents import CaptureAgent
import distanceCalculator
import random, time, util, sys, capture
from game import Directions
import game
from util import nearestPoint
from capture import GameState
from game import AgentState

#################
# Team creation #
#################

def createTeam(firstIndex, secondIndex, isRed,
               first = 'FirstAgent', second = 'SecondAgent'):
  """
  This function should return a list of two agents that will form the
  team, initialized using firstIndex and secondIndex as their agent
  index numbers.  isRed is True if the red team is being created, and
  will be False if the blue team is being created.

  As a potentially helpful development aid, this function can take
  additional string-valued keyword arguments ("first" and "second" are
  such arguments in the case of this function), which will come from
  the --redOpts and --blueOpts command-line arguments to capture.py.
  For the nightly contest, however, your team will be created without
  any extra arguments, so you should make sure that the default
  behavior is what you want for the nightly contest.
  """

  return [eval(first)(firstIndex), eval(second)(secondIndex)]

class myAgent(CaptureAgent) :

    """
    A Dummy agent to serve as an example of the necessary agent structure.
    You should look at baselineTeam.py for more details about how to
    create an agent as this is the bare minimum.
    """

    def registerInitialState(self, gameState):
        """
        This method handles the initial setup of the
        agent to populate useful fields (such as what team
        we're on).

        A distanceCalculator instance caches the maze distances
        between each pair of positions, so your agents can use:
        self.distancer.getDistance(p1, p2)

        IMPORTANT: This method may run for at most 15 seconds.
        """

        '''
        Make sure you do not delete the following line. If you would like to
        use Manhattan distances instead of maze distances in order to save
        on initialization time, please take a look at
        CaptureAgent.registerInitialState in captureAgents.py.
        '''
        CaptureAgent.registerInitialState(self, gameState)

        '''
        Your initialization code goes here, if you need any.
        '''

        self.start = gameState.getAgentPosition(self.index)
        self.isRed = gameState.isOnRedTeam(self.index)

    def chooseAction(self, gameState):
        """
        Picks among actions randomly.
        """
        actions = gameState.getLegalActions(self.index)

        '''
        You should change this in your own agent.
        '''

        move = self.chooseMove(gameState)[1]

        return move

    def getSuccessor(self, gameState, action):
        """
        Finds the next successor which is a grid position (location tuple).
        """
        successor = gameState.generateSuccessor(self.index, action)
        pos = successor.getAgentState(self.index).getPosition()
        if pos != nearestPoint(pos):
            # Only half a grid position was covered
            return successor.generateSuccessor(self.index, action)
        else:
            return successor


class FirstAgent(myAgent) :

    count = 0

    def probability(self, gameState, action) :
        return 1/len(gameState.getLegalActions(self.index))

    def terminalEvaluation(self, gameState, foodLeft) :

        foodLeft1 = self.getFood(gameState).asList()

        terminal = [foodLeft-len(foodLeft1), 'Stop']
        foodNearest = float("inf")

        for a in foodLeft1 :
            dist = self.getMazeDistance(a, gameState.getAgentPosition(self.index))
            if(dist<foodNearest):
                foodNearest = dist
        if(len(foodLeft1) == 0) :
            foodNearest = 0

        terminal[0] = terminal[0]*100 - foodNearest*5

        return terminal

    def value(self, gameState, depth, foodLeft) :
        if depth >= 1 :
            return self.terminalEvaluation(gameState, foodLeft)
        elif depth%2 == 0 :
            return self.maxValue(gameState, depth)
        else :
            return self.expValue(gameState, depth)

    def maxValue(self, gameState, depth) :
        saves = [float("-inf"), 'Stop']

        actions = gameState.getLegalActions(self.index)

        for action in actions:
            if action is not 'Stop' :
                successor = self.getSuccessor(gameState, action)
                compare = self.value(successor, depth+1, len(self.getFood(gameState).asList()))

                if type(compare) is list :
                    compare = float(compare[0])
                if(compare>saves[0]):
                    saves[0] = compare
                    saves[1] = action

        return saves

    def expValue(self, gameState, depth) :
        val = 0
        actions = gameState.getLegalActions(self.index)

        for action in actions:
            p = self.probability(gameState, action)
            val += p*self.value(self.getSuccessor(gameState, action), depth+1, len(self.getFood(gameState).asList()))[0]

        return val

    def goHomeEvaluation(self, gameState) :
        position = gameState.getAgentPosition(self.index)

        distToHome = self.getMazeDistance(gameState.getAgentPosition(self.index), self.start)


        if abs(gameState.getAgentPosition(self.index)[0] - self.start[0]) <= 13 :
            return 0

        distToHome = 100-distToHome

        return distToHome

    def goHome(self, gameState) :
        saves = [float("-inf"), 'Stop']

        actions = gameState.getLegalActions(self.index)

        for action in actions:
            if action is not 'Stop' :
                compare = self.goHomeEvaluation(self.getSuccessor(gameState, action))

                if type(compare) is list :
                    compare = float(compare[0])
                if(compare>saves[0]):
                    saves[0] = compare
                    saves[1] = action

        return saves

    def chooseMove(self, gameState):

        if(abs(gameState.getAgentPosition(self.index)[0]-self.start[0])<=14) :
            FirstAgent.count=0

        if FirstAgent.count>3 or (FirstAgent.count is not 0 and len(self.getFood(gameState).asList())<=2) :
            return self.goHome(gameState)

        foodLeft = len(self.getFood(gameState).asList())
        choice = self.value(gameState, 0, foodLeft)


        successor = self.getSuccessor(gameState, choice[1])


        if (foodLeft - len(self.getFood(successor).asList())) is 1 :
            FirstAgent.count += 1

        return choice

class SecondAgent(myAgent) :

    count = 0

    def probability(self, gameState, action) :
        return 1/len(gameState.getLegalActions(self.index))

    def terminalEvaluation(self, gameState, foodLeft) :

        foodLeft1 = self.getFood(gameState).asList()

        terminal = [foodLeft-len(foodLeft1), 'Stop']
        foodNearest = float("inf")

        for a in foodLeft1 :
            dist = self.getMazeDistance(a, gameState.getAgentPosition(self.index))
            if(dist<foodNearest):
                foodNearest = dist
        if(len(foodLeft1) == 0) :
            foodNearest = 0

        terminal[0] = terminal[0]*100 - foodNearest*5

        return terminal

    def value(self, gameState, depth, foodLeft) :
        if depth >= 1 :
            return self.terminalEvaluation(gameState, foodLeft)
        elif depth%2 == 0 :
            return self.maxValue(gameState, depth)
        else :
            return self.expValue(gameState, depth)

    def maxValue(self, gameState, depth) :
        saves = [float("-inf"), 'Stop']

        actions = gameState.getLegalActions(self.index)

        for action in actions:
            if action is not 'Stop' :
                successor = self.getSuccessor(gameState, action)
                compare = self.value(successor, depth+1, len(self.getFood(gameState).asList()))

                if type(compare) is list :
                    compare = float(compare[0])
                if(compare>saves[0]):
                    saves[0] = compare
                    saves[1] = action

        return saves

    def expValue(self, gameState, depth) :
        val = 0
        actions = gameState.getLegalActions(self.index)

        for action in actions:
            p = self.probability(gameState, action)
            val += p*self.value(self.getSuccessor(gameState, action), depth+1, len(self.getFood(gameState).asList()))[0]

        return val

    def goHomeEvaluation(self, gameState) :
        position = gameState.getAgentPosition(self.index)

        distToHome = self.getMazeDistance(gameState.getAgentPosition(self.index), self.start)


        if abs(gameState.getAgentPosition(self.index)[0] - self.start[0]) <= 13 :
            return 0

        distToHome = 100-distToHome

        return distToHome

    def goHome(self, gameState) :
        saves = [float("-inf"), 'Stop']

        actions = gameState.getLegalActions(self.index)

        for action in actions:
            if action is not 'Stop' :
                compare = self.goHomeEvaluation(self.getSuccessor(gameState, action))

                if type(compare) is list :
                    compare = float(compare[0])
                if(compare>saves[0]):
                    saves[0] = compare
                    saves[1] = action

        return saves

    def chooseMove(self, gameState):

        if(abs(gameState.getAgentPosition(self.index)[0]-self.start[0])<=14) :
            SecondAgent.count = 0

        if SecondAgent.count>3 or (SecondAgent.count is not 0 and len(self.getFood(gameState).asList())<=2) :
            return self.goHome(gameState)

        foodLeft = len(self.getFood(gameState).asList())
        choice = self.value(gameState, 0, foodLeft)


        successor = self.getSuccessor(gameState, choice[1])


        if (foodLeft - len(self.getFood(successor).asList())) is 1 :
            SecondAgent.count += 1

        return choice
