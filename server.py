
'''
server.py is an implementation of the server for the
Quantum Tic-tac-toe game engine. 

Features:
- runs the game, performs updates and terminal tests.
- calculates the winner of a game.
- saves game to a file using grammar implemented in game.py.
- loads game from a file with error-check execution.
- previous move in a game.
- displays to the standard i/o.
'''

import random
import sys
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

    def terminateGame(self):
        if self.moveNum >= self.game.board_size**2:
            count = 0
            for k in self.game.board.keys():
                if not self.game.board[k].stable:
                    count += 1

            if count <= 1:

                # calculate scores
                self.evaluateGame()

                # end game
                sys.exit(0)

    def evaluateGame(self):


        def evaluateCell(row, col, changePos, valueDict, initMark):
            currVal = 1
            while (row in range(self.game.board_size) and 
                col in range(self.game.board_size)):
                
                if self.game.board[(row,col)].stable is None:
                    break

                mark = self.game.board[(row,col)].stable[0]
                if mark == initMark:
                    valueDict[(row,col)] = max(currVal, valueDict[(row,col)])
                    currVal += 1
                    row += changePos[0]
                    col += changePos[1]
                else:
                    break

        value = dict()
        for i in range(self.game.board_size):
            for j in range(self.game.board_size):
                value[(i,j)] = 0

        for i in range(self.game.board_size):
            for j in range(self.game.board_size):
                if self.game.board[(i,j)].stable is not None:
                    mark = self.game.board[(i,j)].stable[0]
                    evaluateCell(i,j,(0,1),value,mark)
                    evaluateCell(i,j,(1,0),value,mark)
                    evaluateCell(i,j,(1,1),value,mark)
                    evaluateCell(i,j,(1,-1),value,mark)

        maxLen = 1
        bestkrist = {'x':0, 'o':0}
        for k in value.keys():
            if self.game.board[k].stable is None:
                continue

            mark = self.game.board[k].stable[0]
            
            if value[k] == maxLen:
                bestkrist[mark] += 1

            elif value[k] > maxLen:
                maxLen = value[k]
                bestkrist['x'] = 0
                bestkrist['o'] = 0
                bestkrist[mark] = 1

        print('Krist length:', maxLen)
        print(bestkrist)

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

        def validMarkValue(server, moveStr):
            return moveStr[0] in 'xo'

        def validMarkPos(pos):
            return (pos[0] in range(0,self.game.board_size) 
                and pos[1] in range(0,self.game.board_size))

        loadingGame = False
        errorDetected = False
        collapsing = False
        prevDepth = 0
        currMoveStr = None

        try:
            file = open(filePath, 'r')
                
            for line in file:
                line = line.strip()

                # Set board size and create an instance of
                # the server.
                # format: SIZE=<n>
                if line[0:5] == 'SIZE=':
                    server = Server(int(line[5]))

                # Start reading the game.
                elif line == 'INIT_STATE':
                    loadingGame = True

                # read move string and update server state.
                else:

                    strList = line.split(' ')
                    
                    if not loadingGame:
                        break

                    # input move string
                    currDepth = strList[0].count('.')
                    moveStr = strList[0].lstrip('.')

                    # validate moveStr
                    if not validMarkValue(server, moveStr):
                        errorDetected = False
                        print('Load error: Invalid mark value detecting in line > '+line)
                        return

                    moveStrList = moveStr.split('-')
                    for val in moveStrList[1:]:
                        if val not in '0123456789':
                            errorDetected = True
                            print('Load error: Invalid pos value detecting in line > '+line)
                            return

                    posList = list()
                    pos0 = (int(moveStrList[1]), int(moveStrList[2]))
                    if not validMarkPos(pos0):
                        errorDetected = True
                        print('Load error: Invalid pos value detecting in line > '+line)
                        return
                    posList.append(pos0)

                    if len(moveStrList) == 5:
                        pos1 = (int(moveStrList[3]), int(moveStrList[4]))
                        if not validMarkPos(pos1):
                            errorDetected = True
                            print('Load error: Invalid pos value detecting in line > '+line)
                            return
                        posList.append(pos1)

                    # create move object
                    move = Move(moveStrList[0], posList)
                    print(move)

                    # assign the move where the board 
                    # was saved from.
                    if len(strList) == 2:
                        if strList[1] == '<---':
                            currMoveStr = move.__str__()

                    if prevDepth >= currDepth:
                        while move.markValue != server.game.movesTree.move.markValue:
                            server.previousMove()

                        server.previousMove()

                    prevDepth = currDepth

                    # update server by playing the move.
                    if move.isCollapse():
                        if collapsing:
                            continue
                        else:
                            collapsing = True
                            server.update(move.posList[0])
                    else:
                        collapsing = False
                        server.update(move.posList[0])
                        server.update(move.posList[1])
            
            file.close()

        except OSError:
            print('File "'+filePath+'" not found.')
            return

        # if error was detected, destroy the server.
        if errorDetected:
            del server
            print('Error detected in the file '+filePath)
        
        # otherwise, assign server to self.
        else:
            # set information in self to the information
            # stored in server
            self.posList = server.posList[:]
            self.game = server.game
            self.moveNum = server.moveNum
            self.curr_state = server.curr_state

            # set movesTree at currMove
            self.game.resetTree(currMoveStr)

            print('Game loaded from '+filePath)

    def run(self, cmd):
        cmdList = cmd.split(' ')
        if cmdList[0] == 'play':

            # play a move
            pos = (int(cmdList[1]), int(cmdList[2]))
            server.update(pos)

            if len(cmdList) == 5:
                pos = (int(cmdList[3]), int(cmdList[4]))
                server.update(pos)

        elif cmdList[0] == 'undo':
            count = 1
            if len(cmdList) == 2:
                count = int(cmdList[1])

            while count:
                server.previousMove()
                count -= 1

        elif cmdList[0] == 'tree':
            server.game.printTree()

        elif cmdList[0] == 'save':
            server.saveGame(cmdList[1])

        elif cmdList[0] == 'load':
            server.loadGame(cmdList[1])

        elif cmdList[0] == 'random':
            '''
            Implementation of a built-in random player.
            '''

            def randCollapse(posList):
                server.update(random.choice(posList))

            def randPlay(posList):
                posList = random.sample(posList, 2)
                server.update(posList[0])
                server.update(posList[1])

            numMoves = int(cmdList[1])
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

        elif cmdList[0] == 'exit':
            sys.exit(0)

def printBoard(game):
    '''
    Given 'game', an instance of game.Game class, print the board to stdio.
    '''

    def printColNumbers():
        for col in range(game.board_size):
            print('      {0}      '.format(col), end='')

    def printDashes():
        print('\n    '+'-'*(game.board_size*13))

    def printCell(row, col, k):
        if game.board[(row,col)].stable is not None:

            # If stable, print a big X or a big O

            # draw an evaluated mark
            if game.board[(row,col)].stable[0] == 'x':
                if k == 3  :  print("            |", end="")
                elif k == 6:  print("     \/     |", end="")
                elif k == 9:  print("     /\     |", end="")
                else       :  print("            |", end="")

            elif game.board[(row,col)].stable[0] == 'o':
                if k == 3  :  print("     __     |", end="")
                elif k == 6:  print("    |  |    |", end="")
                elif k == 9:  print("    |__|    |", end="")
                else       :  print("            |", end="")

            return

        # Otherwise, print each spooky mark in the cell.
        numMarks = len(game.board[(row,col)].marksList)
        outStr = ""
        i = k-3
        while i < k and i < numMarks:
            outStr += game.board[(row,col)].marksList[i]

            # If moveNum of the move is a single digit
            # number, pad an extra space to 'outStr'
            if len(game.board[(row,col)].marksList[i]) < 3:
                outStr += " "

            if i < numMarks-1:
                outStr += " "
            i += 1

        while len(outStr) < 12:
            outStr += " "
        outStr += "|"

        print(outStr, end="")

    print()
    printColNumbers()
    for row in range(game.board_size):
        printDashes()
        for k in range(3, 13, 3):
            if k == 6:
                print(str(row)+'  | ', end='')
            else:
                print('   | ', end='')
            for col in range(game.board_size):
                printCell(row,col,k)
            if k < 12:
                if k == 6:
                    print('  '+str(row))
                else:
                    print()
    
    printDashes()
    printColNumbers()
    print('\n')

if __name__ == '__main__':

    # process commandline arguments
    if len(sys.argv) > 1:
        size = int(sys.argv[1])
    else:
        size = 4

    # Initialize server
    server = Server(size)

    # Run game
    printBoard(server.game)
    while True:
        cmd = input('[{}] '.format(server.moveNum))
        server.run(cmd)

        printBoard(server.game)
        print('Server state:', server.curr_state)
        print('Last move:', server.game.movesTree.move)

        # terminate game if done
        server.terminateGame()