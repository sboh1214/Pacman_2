
from captureAgents import CaptureAgent
import distanceCalculator
import random, time, util, sys, capture
from game import Directions
import game
from util import nearestPoint
from capture import GameState
from game import AgentState
from capture import AgentRules
from game import Agent
from game import GameStateData
from game import Configuration

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

    weight={"PalletNum":50, \
    "NearestPallet":-3, \
    "EnemyBaseOppAgentDist":3, \
    "ScaredOppAgentDist":0, \
    "OurBaseDist":-3, \
    "OurBaseDistInMax5":-10, \
    "OurBaseDistUnder2":-15, \
    "EatenPallet":1, \
    "OppAgentKill":20, \
    "OurBaseOppAgentDist":3, \
    "ScaredAgentDist":-20, \
    "DefensePointDist":3}
    GameTime = 0

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
    FirstHistory = []    
    def probability(self, gameState, action) :
        return 1/len(gameState.getLegalActions(self.index))

    def terminalEvaluation(self, gameState, foodLeft) :
        try:
            foodLeft1 = self.getFood(gameState).asList()

            terminal = [foodLeft-len(foodLeft1), 'Stop']
            foodNearest = float("inf")
            redIndex=gameState.getRedTeamIndices()
            blueIndex=gameState.getBlueTeamIndices()
    
            for a in foodLeft1 : #Pellet 섭취 여부와 가장 가까운 Pellet의 거리 계산
                dist = self.getMazeDistance(a, gameState.getAgentPosition(self.index))
                if(dist<foodNearest):
                    foodNearest = dist
            if(len(foodLeft1) == 0) :
                foodNearest = 0

            configuration = Configuration(gameState.getAgentPosition(self.index),Directions.STOP) #좌표,Action
            agentState = AgentState(configuration,True)
            State = agentState.copy()

            if(self.isRed): # RED 일때
                enemyDistance= 0
                distanceFromDefend = 0
                if(gameState.getAgentPosition(blueIndex[0]) != None) :
                    enemyDistance1= self.getMazeDistance(gameState.getAgentPosition(self.index), gameState.getAgentPosition(blueIndex[0]))
                    if(gameState.getAgentPosition(blueIndex[0])[0]>= 15 and enemyDistance1<= 6): #적과의 거리
                        
                            enemyDistance-= (7-enemyDistance1)** self.weight["EnemyBaseOppAgentDist"]
                    if(gameState.getAgentPosition(blueIndex[0])[0]<= 14 and enemyDistance1<= 6):
                     
                            enemyDistance+= (7-enemyDistance1)* self.weight["OurBaseOppAgentDist"]
                       

                if(gameState.getAgentPosition(blueIndex[1])!=None) :
                    enemyDistance2= self.getMazeDistance(gameState.getAgentPosition(self.index), gameState.getAgentPosition(blueIndex[1]))
                    if(gameState.getAgentPosition(blueIndex[1])[0]>= 15 and enemyDistance2<= 6): #적과의 거리
                        
                            enemyDistance-= (7-enemyDistance2)** self.weight["EnemyBaseOppAgentDist"]
                            
                    if(gameState.getAgentPosition(blueIndex[1])[0]<= 14 and enemyDistance2<= 6):
                        
                            
                            enemyDistance+= (7-enemyDistance2)* self.weight["OurBaseOppAgentDist"]
                if(gameState.getScore()> 0) :
                    distanceFromDefend-=(self.getMazeDistance(gameState.getAgentPosition(self.index), (12,10) ))**2


            else: # BLUE 일때
                enemyDistance= 0
                distanceFromDefend = 0
                if(gameState.getAgentPosition(redIndex[0])!=None) :
                    enemyDistance1= self.getMazeDistance(gameState.getAgentPosition(self.index), gameState.getAgentPosition(redIndex[0]))
                    if(gameState.getAgentPosition(redIndex[0])[0]<= 14 and enemyDistance1<= 6): #적과의 거리
                        enemyDistance-= (7-enemyDistance1)** self.weight["EnemyBaseOppAgentDist"]
                            
                    if(gameState.getAgentPosition(redIndex[0])[0]>= 15 and enemyDistance1<= 6):
                        enemyDistance+= (7-enemyDistance1)* self.weight["OurBaseOppAgentDist"]
                            

                if(gameState.getAgentPosition(redIndex[1])!=None) :
                    enemyDistance2= self.getMazeDistance(gameState.getAgentPosition(self.index), gameState.getAgentPosition(redIndex[1]))
                    if(gameState.getAgentPosition(redIndex[1])[0]<= 14 and enemyDistance2<= 6): #적과의 거리
                        
                           enemyDistance-= (7-enemyDistance2)** self.weight["EnemyBaseOppAgentDist"]
                            
                    if(gameState.getAgentPosition(redIndex[1])[0]>= 15 and enemyDistance2<= 6):
                        
                            enemyDistance+= (7-enemyDistance2)* self.weight["OurBaseOppAgentDist"]
                            
                if(gameState.getScore()< 0) :
                    distanceFromDefend-=(self.weight["DefensePointDist"]* self.getMazeDistance(gameState.getAgentPosition(self.index), (19,5) ))**2
            terminal[0] = terminal[0]*self.weight["PalletNum"] + foodNearest*self.weight["NearestPallet"] + distanceFromDefend + enemyDistance
            return terminal
        except:
            return 10
    
    def value(self, gameState, depth, foodLeft, alpha, beta) :
        if depth >= 1 :

            return self.terminalEvaluation(gameState, foodLeft)
        elif depth%2 == 0 :
            return self.maxValue(gameState, depth, alpha, beta)
        else :
            return self.minValue(gameState, depth, alpha, beta)

    def maxValue(self, gameState, depth, alpha, beta) :
        saves = [float("-inf"), 'Stop']

        actions = gameState.getLegalActions(self.index)

        for action in actions:
            if action is not 'Stop' :
                successor = self.getSuccessor(gameState, action)
                compare = self.value(successor, depth+1, len(self.getFood(gameState).asList()), alpha, beta)

                if type(compare) is list :
                    compare = float(compare[0])
                if(compare>saves[0]):
                    saves[0] = compare
                    saves[1] = action
                if (saves[0]>beta):
                    return saves

                alpha = max(alpha,saves[0])

        return saves

    def minValue(self, gameState, depth, alpha, beta):
        saves = [float("inf"), 'Stop']

        actions = gameState.getLegalActions(self.index)

        for action in actions:
            if action is not 'Stop':
                successor = self.getSuccessor(gameState, action)
                compare = self.value(successor, depth + 1, len(self.getFood(gameState).asList()), alpha, beta)

                if type(compare) is list:
                    compare = float(compare[0])
                if (compare < saves[0]):
                    saves[0] = compare
                    saves[1] = action
                if (saves[0] < alpha ):
                    return saves

                beta = min(beta, saves[0])

        return saves

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

    def HowToAction(self, gameState): #30X14 오승빈
        redIndex=gameState.getRedTeamIndices()
        blueIndex=gameState.getBlueTeamIndices()
        self.GameTime += 1
        LeftTime = 300 - self.GameTime
        
        Score = gameState.getScore()
        RB = self.isRed
        if (Score > 0 and RB == True):
            IsWin = True
        else:
            IsWin = False
        if (RB==True): #When our team is red
            FAPos = gameState.getAgentPosition(redIndex[0]) #Red First Agent Position
            SAPOs = gameState.getAgentPosition(redIndex[1]) #Red Second Agent Position
            if (FAPos[0]==0 and FAPos[1]<13 and SAPOs[0]==0 and SAPOs[1]<13):
                InitialTime = True
            else:
                InitialTime = False
        else: #when our team is blue
            FAPos = gameState.getAgentPosition(blueIndex[0]) #Blue First Agent Position
            SAPos = gameState.getAgentPosition(blueIndex[1]) #Blue Second Agent Position
            if (FAPos[0]==29 and FAPos[1]>0 and SAPos[0]==29 and SAPos[1]>0):
                InitialTime = True
            else:
                InitialTime = False

        if (LeftTime <= 30 and IsWin==False):
            return "TimeAttack"
        elif (LeftTime <= 30 and IsWin==True):
            return "TimeDefense"
        elif (InitialTime == True):
            return "InitialTime"
        elif (len(self.FirstHistory) > 3):
            if (self.FirstHistory[-1]==self.FirstHistory[-3] and self.FirstHistory[-2]==self.FirstHistory[-4]):
                return "Thrashing"
        else:
            return "AI"        

    def chooseTimeAttack(self,gameState): #오승빈
        redIndex=gameState.getRedTeamIndices()
        blueIndex=gameState.getBlueTeamIndices()
        if (gameState.isRed==True):
            RedSecond = gameState.getLegalActions(redIndex[1])
            for item in RedSecond:
                if (item is "EAST"):
                    return Directions.EAST
            return Directions.STOP
        else:
            BlueSecond = gameState.getLegalActions(blueIndex[1])
            for item in BlueSecond:
                if (item is "WEST"):
                    return Directions.WEST
            return Directions.STOP

    def chooseTimeDefense(self, gameState): #오승빈
        redIndex=gameState.getRedTeamIndices()
        blueIndex=gameState.getBlueTeamIndices()
        if (gameState.isRed==True):
            RedSecond = gameState.getLegalActions(redIndex[1])
            for item in RedSecond:
                if (item is "WEST"):
                    return Directions.WEST
            return Directions.STOP
        else:
            BlueSecond = gameState.getLegalActions(blueIndex[1])
            for item in BlueSecond:
                if (item is "EAST"):
                    return Directions.EAST
            return Directions.STOP

    def chooseInitial(self, gameState): #오승빈
        if (gameState.isRed == True):
            return Directions.NORTH
        else:
            return Directions.SOUTH

    def chooseMustMove(self, gameState): #오승빈
        redIndex=gameState.getRedTeamIndices()
        blueIndex=gameState.getBlueTeamIndices()
        if (gameState.isRed==True):
            RedFirst = gameState.getLegalActions(redIndex[0])
            for item in RedFirst:
                if (item is "WEST"):
                    return Directions.WEST
                elif (item is "EAST"):
                    return Directions.EAST
                elif (item is "SOUTH"):
                    return Directions.SOUTH
                elif (item is "NORTH"):
                    return Directions.NORTH
            return Directions.STOP
        else:
            BlueFirst = gameState.getLegalActions(blueIndex[0])
            for item in BlueFirst:
                if (item is "WEST"):
                    return Directions.WEST
                elif (item is "EAST"):
                    return Directions.EAST
                elif (item is "SOUTH"):
                    return Directions.SOUTH
                elif (item is "NORTH"):
                    return Directions.NORTH
            return Directions.STOP

    def chooseMove(self, gameState): #오승빈
        if(abs(gameState.getAgentPosition(self.index)[0]-self.start[0])<=14) :
            FirstAgent.count=0

        if FirstAgent.count>3 or (FirstAgent.count is not 0 and len(self.getFood(gameState).asList())<=2) :
            return self.goHome(gameState)

        foodLeft = len(self.getFood(gameState).asList())

        selection = self.HowToAction(gameState) #AI가 필요한지 노가다가 필요한지 결정
        if (selection == "AI"):
            choice = self.value(gameState, 0, foodLeft,float("-inf"),float("inf")) #AI사용
        elif (selection == "TimeAttack"):
            choice = self.chooseTimeAttack(gameState) #시간이 얼마 남지 않았는데 지고 있을때
        elif (selection == "TimeDefense"):
            choice = self.chooseTimeDefense(gameState) #시간이 얼마 남지 않았는데 이기고 있을때
        elif (selection == "InitialTime"):
            choice = self.chooseInitial(gameState) #처음 시작할때
        elif (selection == "Thrashing"):
            choice = self.chooseMustMove(gameState)
        else:
            choice = self.value(gameState, 0, foodLeft,float("-inf"),float("inf"))

        successor = self.getSuccessor(gameState, choice[1])


        if (foodLeft - len(self.getFood(successor).asList())) is 1 :
            FirstAgent.count += 1

        self.FirstHistory.append(choice)
        print ("First : ",choice)

        return choice

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

class SecondAgent(myAgent) :

    count = 0
    SecondHistory = []

    def probability(self, gameState, action) :
        return 1/len(gameState.getLegalActions(self.index))

    def terminalEvaluation(self, gameState, foodLeft) :
        try:
            foodLeft1 = self.getFood(gameState).asList()
    
            terminal = [foodLeft-len(foodLeft1), 'Stop']
            foodNearest = float("inf")
            redIndex=gameState.getRedTeamIndices()
            blueIndex=gameState.getBlueTeamIndices()
     
            for a in foodLeft1 : #Pellet 섭취 여부와 가장 가까운 Pellet의 거리 계산
                dist = self.getMazeDistance(a, gameState.getAgentPosition(self.index))
                if(dist<foodNearest):
                    foodNearest = dist
                if(len(foodLeft1) == 0) :
                    foodNearest = 0
                
    
            if(self.isRed): # RED 일때
                enemyDistance= 0
                distanceFromDefend = 0
                if(gameState.getAgentPosition(blueIndex[0])!=None) :
                    enemyDistance1= self.getMazeDistance( gameState.getAgentPosition(self.index),gameState.getAgentPosition(blueIndex[0]) )
                    if(gameState.getAgentPosition(blueIndex[0])[0]>= 15 and enemyDistance1<= 6): #적과의 거리
                        
                            enemyDistance-= (7-enemyDistance1)** self.weight["EnemyBaseOppAgentDist"]
                            
                    if(gameState.getAgentPosition(blueIndex[0])[0]<= 14 and enemyDistance1<= 6):
                        
                            enemyDistance+= (7-enemyDistance1)* self.weight["OurBaseOppAgentDist"]
                           

                if(gameState.getAgentPosition(blueIndex[1])!=None) :
                    enemyDistance2= self.getMazeDistance(gameState.getAgentPosition(self.index), gameState.getAgentPosition(blueIndex[1]))
                    if(gameState.getAgentPosition(blueIndex[1])[0]>= 15 and enemyDistance2<= 6): #적과의 거리
                        
                            enemyDistance-= (7-enemyDistance2)** self.weight["EnemyBaseOppAgentDist"]
                            
                    if(gameState.getAgentPosition(blueIndex[1])[0]<= 14 and enemyDistance2<= 6):
                        
                            enemyDistance+= (7-enemyDistance2)* self.weight["OurBaseOppAgentDist"]
                            
                            
                if(gameState.getScore()> 0) :
                    distanceFromDefend-=(self.getMazeDistance(gameState.getAgentPosition(self.index), (12,4) ))**2
            else: # BLUE 일때
                enemyDistance= 0
                distanceFromDefend = 0
                if(gameState.getAgentPosition(redIndex[0])!=None) :
                    enemyDistance1= self.getMazeDistance(gameState.getAgentPosition(self.index), gameState.getAgentPosition(redIndex[0]))
                    if(gameState.getAgentPosition(redIndex[0])[0]<= 14 and enemyDistance1<= 6): #적과의 거리
                        
                            enemyDistance-= (7-enemyDistance1)** self.weight["EnemyBaseOppAgentDist"]
                            
                    if(gameState.getAgentPosition(redIndex[0])[0]>= 15 and enemyDistance1<= 6):
                        
                            enemyDistance+= (7-enemyDistance1)* self.weight["OurBaseOppAgentDist"]
                           

                if(gameState.getAgentPosition(redIndex[1])!=None) :
                    enemyDistance2= self.getMazeDistance(gameState.getAgentPosition(self.index), gameState.getAgentPosition(redIndex[1]))
                    if(gameState.getAgentPosition(redIndex[1])[0]<= 14 and enemyDistance2<= 6): #적과의 거리
                        
                            enemyDistance-= (7-enemyDistance2)** self.weight["EnemyBaseOppAgentDist"]
                            
                    if(gameState.getAgentPosition(redIndex[1])[0]>= 15 and enemyDistance2<= 6):
                        
                            enemyDistance+= (7-enemyDistance2)* self.weight["OurBaseOppAgentDist"]
                            
                if(gameState.getScore()< 0) :
                    distanceFromDefend-=(self.weight["DefensePointDist"]* self.getMazeDistance(gameState.getAgentPosition(self.index), (19,11) ))**2
        
    
            terminal[0] = terminal[0]*self.weight["PalletNum"] + foodNearest*self.weight["NearestPallet"]*0.7 + distanceFromDefend + enemyDistance*1.5
            return terminal
        except:
            return 10

    def value(self, gameState, depth, foodLeft, alpha, beta) :
        if depth >= 1 :
            return self.terminalEvaluation(gameState, foodLeft)
        elif depth%2 == 0 :
            return self.maxValue(gameState, depth, alpha, beta)
        else :
            return self.minValue(gameState, depth, alpha, beta)


    def maxValue(self, gameState, depth, alpha, beta) :
        saves = [float("-inf"), 'Stop']

        actions = gameState.getLegalActions(self.index)

        for action in actions:
            if action is not 'Stop' :
                successor = self.getSuccessor(gameState, action)
                compare = self.value(successor, depth+1, len(self.getFood(gameState).asList()), alpha, beta)

                if type(compare) is list :
                    compare = float(compare[0])
                if(compare>saves[0]):
                    saves[0] = compare
                    saves[1] = action
                if (saves[0]>beta):
                    return saves

                alpha = max(alpha,saves[0])

        return saves

    def minValue(self, gameState, depth, alpha, beta):
        saves = [float("inf"), 'Stop']

        actions = gameState.getLegalActions(self.index)

        for action in actions:
            if action is not 'Stop':
                successor = self.getSuccessor(gameState, action)
                compare = self.value(successor, depth + 1, len(self.getFood(gameState).asList()), alpha, beta)

                if type(compare) is list:
                    compare = float(compare[0])
                if (compare < saves[0]):
                    saves[0] = compare
                    saves[1] = action
                if (saves[0] < alpha ):
                    return saves

                beta = min(beta, saves[0])

        return saves

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

    def HowToAction(self, gameState): #30X14 오승빈
        redIndex=gameState.getRedTeamIndices()
        blueIndex=gameState.getBlueTeamIndices()
        self.GameTime += 1
        LeftTime = 300 - self.GameTime
        
        Score = gameState.getScore()
        RB = self.isRed
        if (Score > 0 and RB == True):
            IsWin = True
        else:
            IsWin = False
        if (RB==True): #When our team is red
            FAPos = gameState.getAgentPosition(redIndex[0]) #Red First Agent Position
            SAPOs = gameState.getAgentPosition(redIndex[1]) #Red Second Agent Position
            if (FAPos[0]==0 and FAPos[1]<13 and SAPOs[0]==0 and SAPOs[1]<13):
                InitialTime = True
            else:
                InitialTime = False
        else: #when our team is blue
            FAPos = gameState.getAgentPosition(blueIndex[0]) #Blue First Agent Position
            SAPos = gameState.getAgentPosition(blueIndex[1]) #Blue Second Agent Position
            if (FAPos[0]==29 and FAPos[1]>0 and SAPos[0]==29 and SAPos[1]>0):
                InitialTime = True
            else:
                InitialTime = False

        if (LeftTime <= 30 and IsWin==False):
            return "TimeAttack"
        elif (LeftTime <= 30 and IsWin==True):
            return "TimeDefense"
        elif (InitialTime == True):
            return "InitialTime"
        elif (len(self.SecondHistory) > 3):
            if (self.SecondHistory[-1]==self.SecondHistory[-3] and self.SecondHistory[-2]==self.SecondHistory[-4]):
                return "Thrashing"
        else:
            return "AI"        

    def chooseTimeAttack(self,gameState): #오승빈
        redIndex=gameState.getRedTeamIndices()
        blueIndex=gameState.getBlueTeamIndices()
        if (gameState.isRed==True):
            RedSecond = gameState.getLegalActions(redIndex[1])
            for item in RedSecond:
                if (item is "EAST"):
                    return Directions.EAST
            return Directions.STOP
        else:
            BlueSecond = gameState.getLegalActions(blueIndex[1])
            for item in BlueSecond:
                if (item is "WEST"):
                    return Directions.WEST
            return Directions.STOP

    def chooseTimeDefense(self, gameState): #오승빈
        redIndex=gameState.getRedTeamIndices()
        blueIndex=gameState.getBlueTeamIndices()
        if (gameState.isRed==True):
            RedSecond = gameState.getLegalActions(redIndex[1])
            for item in RedSecond:
                if (item is "WEST"):
                    return Directions.WEST
            return Directions.STOP
        else:
            BlueSecond = gameState.getLegalActions(blueIndex[1])
            for item in BlueSecond:
                if (item is "EAST"):
                    return Directions.EAST
            return Directions.STOP

    def chooseInitial(self, gameState): #오승빈
        if (gameState.isRed == True):
            return Directions.NORTH
        else:
            return Directions.SOUTH

    def chooseMustMove(self, gameState): #오승빈
        redIndex=gameState.getRedTeamIndices()
        blueIndex=gameState.getBlueTeamIndices()
        if (gameState.isRed==True):
            RedSecond = gameState.getLegalActions(redIndex[1])
            for item in RedSecond:
                if (item is "WEST"):
                    return Directions.WEST
                elif (item is "EAST"):
                    return Directions.EAST
                elif (item is "SOUTH"):
                    return Directions.SOUTH
                elif (item is "NORTH"):
                    return Directions.NORTH
            return Directions.STOP
        else:
            BlueSecond = gameState.getLegalActions(blueIndex[1])
            for item in BlueSecond:
                if (item is "WEST"):
                    return Directions.WEST
                elif (item is "EAST"):
                    return Directions.EAST
                elif (item is "SOUTH"):
                    return Directions.SOUTH
                elif (item is "NORTH"):
                    return Directions.NORTH
            return Directions.STOP

    def chooseMove(self, gameState): #오승빈
        if(abs(gameState.getAgentPosition(self.index)[0]-self.start[0])<=14) :
            FirstAgent.count=0

        if FirstAgent.count>3 or (FirstAgent.count is not 0 and len(self.getFood(gameState).asList())<=2) :
            return self.goHome(gameState)

        foodLeft = len(self.getFood(gameState).asList())

        selection = self.HowToAction(gameState) #AI가 필요한지 노가다가 필요한지 결정
        if (selection == "AI"):
            choice = self.value(gameState, 0, foodLeft,float("-inf"),float("inf")) #AI사용
        elif (selection == "TimeAttack"):
           choice = self.chooseTimeAttack(gameState) #시간이 얼마 남지 않았는데 지고 있을때
        elif (selection == "TimeDefense"):
           choice = self.chooseTimeDefense(gameState) #시간이 얼마 남지 않았는데 이기고 있을때
        elif (selection == "InitialTime"):
            choice = self.chooseInitial(gameState) #처음 시작할때
        elif (selection == "Thrashing"):
            choice = self.chooseMustMove(gameState)
        else:
            choice = self.value(gameState, 0, foodLeft,float("-inf"),float("inf"))

        successor = self.getSuccessor(gameState, choice[1])


        if (foodLeft - len(self.getFood(successor).asList())) is 1 :
            FirstAgent.count += 1

        self.SecondHistory.append(choice)
        print("Second : ",choice)

        return choice

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