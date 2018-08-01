from captureAgents import CaptureAgent
import random
import game

def createTeam(firstIndex, secondIndex, isRed):
    return [StupidAgent(firstIndex), StupidAgent(secondIndex)]

class StupidAgent(CaptureAgent):

    def registerInitialState(self, gameState):
        CaptureAgent.registerInitialState(self, gameState)

    def chooseAction(self, gameState):
        actions = gameState.getLegalActions(self.index)
        return random.choice(actions)