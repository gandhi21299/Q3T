
'''
Implementation of the game server. This program is capable of running
the game on stdio.
'''

import random
import sys
from util import *
from _game import *

class Server:

    # class attributes
    curr_state = "X_0"    # x plays the first move.
    moveNum   = 1         # the number of moves

    def __init__(self, board_size):
        
        # class constructor
        self.posList = list()
        self.game = Game(board_size)

    def currMark(self):
        return self.curr_state[0].lower()+str(self.moveNum)

    def update(self, pos):
        '''
        Implementation of state transitions of the
        server. 'pos', a 2-tuple is required by this function.
        '''

        if self.curr_state == "X_0":
            if self.game.updateState('x'+str(self.moveNum), [pos]):
                self.posList = [pos]
                self.curr_state = "X_1"

        elif self.curr_state == "X_1":
            self.posList.append(pos)
            if self.game.updateState('x'+str(self.moveNum), self.posList):
                if self.game.cycleDetected:
                    self.curr_state = "O_COLLAPSE"
                else:
                    self.curr_state = "O_0"
                self.moveNum += 1
            else:
                self.posList.pop()
                
        elif self.curr_state == "X_COLLAPSE":
            if self.game.updateState('o'+str(self.moveNum-1), [pos], True):
                self.curr_state = "X_0"

        elif self.curr_state == "O_0":
            self.posList = [pos]
            if self.game.updateState('o'+str(self.moveNum), self.posList):
                self.curr_state = "O_1"

        elif self.curr_state == "O_1":
            self.posList.append(pos)
            if self.game.updateState('o'+str(self.moveNum), self.posList):
                if self.game.cycleDetected:
                    self.curr_state = "X_COLLAPSE"
                else:
                    self.curr_state = "X_0"
                self.moveNum += 1

        elif self.curr_state == "O_COLLAPSE":
            if self.game.updateState('x'+str(self.moveNum-1), [pos], True):
                self.curr_state = "O_0"

    def previousMove(self):
        '''
        Return to the most recent move played, provided that the 
        move is complete.
        '''
        if self.curr_state == 'X_1' or self.curr_state == 'O_1':
            print('Error: Current state does not allow reversing back a move.')
            return

        if self.moveNum == 1:
            print('Error: Board is empty.')
            return
        
        self.moveNum = self.game.previousState()
        mark = ''
        if self.game.movesTree.move is None:
            self.moveNum = 1
            self.curr_state = 'X_0'

        else:
            if self.moveNum%2:
                mark = 'X'
            else:
                mark = 'O'

            if self.game.cycleDetected:
                self.curr_state = mark+'_COLLAPSE'
            else:
                self.curr_state = mark+'_0'

    def saveGame(self, filePath):
        '''
        Saves game to the provided 'filePath'. Creates a
        file if it does not exist, otherwise replaces the
        original file.
        '''
        file = open(filePath, 'w+')
        self.game.printTree(file)
        file.close()

        print ('Game saved to '+filePath)

    def loadGame(self, filePath):
        '''
        Loads a game from the passed in 'filePath'.
        TO DO: Improve error-checking in the file grammar.
        '''

        loadingGame = False
        errorDetected = False
        collapsing = False
        prevDepth = 0
        currMoveStr = None

        with open(filePath, 'r+') as file:
            
            for line in file:
                line = line.strip()
                print(line)

                # Set board size and create an instance of
                # the server.
                if line[0:4] == 'SIZE':
                    server = Server(int(line[5]))

                # Start reading the game.
                elif line == 'INIT_STATE':
                    loadingGame = True

                # read move string and update server state.
                else:

                    strList = line.split(' ')
                    
                    if loadingGame:

                        # input move string
                        currDepth = strList[0].count('.')
                        moveStr = strList[0].lstrip('.')

                        # create move object
                        move = Move()
                        move.read(moveStr)

                        # assign the move where the board 
                        # was saved from.
                        if len(strList) == 2:
                            if strList[1] == '<---':
                                currMoveStr = move.__str__()

                        # check if the current move was played
                        # higher in the tree.
                        count = prevDepth - currDepth + 1
                        while count:
                            if server.game.movesTree.move.isCollapse():
                                server.previousMove()
                                if move.isCollapse():
                                    collapsing = False
                                    break

                            else:
                                server.previousMove()
                                count -= 1
                        prevDepth = currDepth

                        # update server by playing the move.
                        if move.isCollapse():
                            if collapsing:
                                continue
                            else:
                                collapsing = True
                                server.update(move.posList[0])
                                print('collapse: ', move)
                        else:
                            collapsing = False
                            server.update(move.posList[0])
                            server.update(move.posList[1])

        # if error was detected, destroy the server.
        if errorDetected:
            del server
            print('Error detected in the file '+filePath)
        
        # otherwise, assign server to self.
        else:

            # set movesTree at currMove
            server.game.resetTree(currMoveStr)

            # set information in self to the information
            # stored in server
            self.posList = server.posList[:]
            self.game = server.game
            self.moveNum = server.moveNum
            self.curr_state = server.curr_state

            print('Game loaded from '+filePath)

if __name__ == '__main__':

    if len(sys.argv) > 1:
        size = int(sys.argv[1])
    else:
        size = 4

    # Initialize server
    server = Server(size)

    printBoard(server.game)

    while True:
        print('Server state:', server.curr_state)
        print('movesTree.move =', server.game.movesTree.move)
        
        inList = input('[{}] '.format(server.moveNum)).split()
        if inList[0] == 'play':
            pos0 = (int(inList[1]), int(inList[2]))
            server.update(pos0)
            
            if len(inList) == 5:
                pos1 = (int(inList[3]), int(inList[4]))
                server.update(pos1)

        elif inList[0] == 'undo':
            if len(inList) == 2:
                count = int(inList[1])
            else:
                count = 1
            while count:
                server.previousMove()
                count -= 1

        elif inList[0] == 'tree':
            server.game.printTree()

        elif inList[0] == 'save':
            server.saveGame(inList[1])

        elif inList[0] == 'load':
            server.loadGame(inList[1])

        elif inList[0] == 'random':

            '''
            TO FIX: A random call should play a full legal
            random move.

            A collapse move is breaking a cycle + a play move.
            '''

            def randCollapse(posList):
                server.update(random.choice(posList))

            def randPlay(posList):
                posList = random.sample(posList, 2)
                server.update(posList[0])
                server.update(posList[1])

            numMoves = int(inList[1])
            while numMoves:
                posList = server.game.getMoves()

                if len(posList) < 2:
                    break

                if server.curr_state[1:] == '_COLLAPSE':
                    randCollapse(posList)

                    posList = server.game.getMoves()

                    if len(posList) < 2:
                        break
                    randPlay(posList)

                elif server.curr_state[1:] == '_0':
                    randPlay(posList)

                numMoves -= 1

        elif inList[0] == 'exit':
            sys.exit(0)

        printBoard(server.game)