
from _move import Move, MoveNode
from util import *
import random

# -------------------------------------------------------------------
# Implementation of the Union Find Data Structure. Uses path
# compression and the rank heuristic to speedup union and find
# operations.
class UnionFind:
    def __init__(self):
        self.par = {}
        self.rank = {}

    def makeSet(self, u):
        self.par[u] = u
        self.rank[u] = 0

    def find(self, u):
        if self.par[u] != u:
            self.par[u] = self.find(self.par[u])

        return self.par[u]

    def union(self, u, v):
        ru = self.find(u)
        rv = self.find(v)

        if ru == rv:
            return False

        if self.rank[ru] > self.rank[rv]:
            self.par[rv] = ru

        else:
            self.par[ru] = rv
            if self.rank[ru] == self.rank[rv]:
                self.rank[rv] += 1

        return True

    def printSets(self):
        for v in self.par.keys():
            print(v, '->', self.par[v], self.rank[v])
# -------------------------------------------------------------------

# Class for handling exceptions
class InputError(Exception):
    def __init__(self, msg):
        self.message = msg
# -------------------------------------------------------------------
class Cell:
    def __init__(self, row, col):
        self.pos = (row,col)
        self.marksList = list()
        self.stable = None


# Implementation of the game.
class Game:
    def __init__(self, board_size):

        '''
        Intialize data structures involved in the game.
        - board_size: size of the board. (#rows = #columns)
        - board: maps position on the board to the cell instance
            corresponding to that indexed position.
        - unionFind: an instance of 'UnionFind' with nodes 
            representing each cell on the board.
        - movesTree: stores a pointer to the current moveNode. Used for
            pointing to previous and next 
        '''

        self.board_size = board_size
        self.movesTree = MoveNode()
        self.board = dict()
        self.unionFind = UnionFind()
        self.cycleDetected = False
        self.score = {'x': 0, 'o': 0}
        
        self.initializeStruct()

    def initializeStruct(self):
        '''
        Initialize 'board' and 'unionFind'.
        '''

        for i in range(0, self.board_size):
            for j in range(0, self.board_size):
                self.board[(i,j)] = Cell(i,j)
                self.unionFind.makeSet((i,j))

    def getCellIndex(self, pos):
        return pos[0]*self.board_size + pos[1]

    def updateMovesHistory(self, move):
        '''
        Computes key for each pos stored in 'move'. Creates a new
        'moveNode' as a child at the computed key to the current 
        moveNode 'movesTree' and stores 'move'. Sets the parent of 
        the new moveNode to 'movesTree'. Updates 'movesTree'.
        '''
        def update_pos_order(posList):
            if self.getCellIndex(posList[1]) < self.getCellIndex(posList[0]):
                tmp = posList[0]
                posList[0] = posList[1]
                posList[1] = tmp


        if self.movesTree is None:
            self.movesTree = MoveNode()

        # Compute key for the move to be processed.
        key = 0
        if move.isCollapse():
            key = 1
            key = key << 4
            key += self.getCellIndex(move.posList[0])
            key = key << 4

        else:
            update_pos_order(move.posList)

            key = self.getCellIndex(move.posList[0])
            key = key << 4
            key += self.getCellIndex(move.posList[1])

        # Add move to the tree.
        self.movesTree.add_child(key, move)

        # Update movesTree
        self.movesTree = self.movesTree.children[key]

    def entangle(self, pos0, pos1):
        '''
        Connects pos0 and pos1.
        '''
        self.cycleDetected = not self.unionFind.union(pos0, pos1)

    def updateState(self, markValue, posList, collapse = False):

        '''
        First checks if the move is legal. If it is, then the state is
        updated and the moves history is also updated.
        '''

        # check if 'pos' is already stable.
        for pos in posList:
            if self.board[pos].stable is not None:
                print('Error: ({},{}) is stable.'.format(pos[0], pos[1]))
                return False

            if pos[0] < 0 or pos[1] >= self.board_size:
                print('Error: ({},{}) out of bounds.'.format(pos[0], pos[1]))

        # checks if the marks are placed in distinct cells.
        if len(posList) == 2:
            if posList[0] == posList[1]:
                print('Error: ({},{}) already contains a mark with the same value.'.
                    format(posList[0], posList[1]))
                return False

        # update board configuration with the move.
        move = Move(markValue, posList)
        if collapse:
            if pos in self.movesTree.move.posList:
                self.evaluateCell(move)
            else:
                print('Error: Illegal move at ({0},{1}) to begin collapse.'.format(pos[0], pos[1]))
                return False
        else:
            self.board[posList[-1]].marksList.append(markValue)
            if len(posList) == 2:
                self.entangle(posList[0], posList[1])
                self.updateMovesHistory(move)

        return True

    def previousState(self):
        '''
        Performs a previous move operation. Firstly, ensures that the
        'movesTree' has a parent. Brings states of the last played move
        markValue back to quantum state. Recreates the UnionFind data 
        structure.
        '''
        moveNum = 0
        
        # Perform 'anti-collapse' move
        lastMove = self.movesTree
        undoCompleted = False
        while self.movesTree.move.isCollapse() and self.movesTree.parent is not None:
            self.board[self.movesTree.move.posList[0]].stable = None
            self.movesTree = self.movesTree.parent

            undoCompleted = True

        if undoCompleted:
            moveNum  = int(self.movesTree.move.markValue[1:])+1
        else:
            self.board[self.movesTree.move.posList[0]].marksList.remove(self.movesTree.move.markValue)
            self.board[self.movesTree.move.posList[1]].marksList.remove(self.movesTree.move.markValue)
            moveNum  = int(self.movesTree.move.markValue[1:])

            self.movesTree = self.movesTree.parent

        # Destroy the UnionFind data.
        # Now reconnect each pair cells connected via superposition. Define
        # a nested function that stores each pair of cells on the grid until
        # the move that was undone.
        self.unionFind = UnionFind()
        self.cycleDetected = False

        # Reinitialize unionFind
        for i in range(self.board_size):
            for j in range(self.board_size):
                self.unionFind.makeSet((i, j))

        moves = self.movesTree.get_moves()
        while len(moves):
            move = moves.pop()
            if not move.isCollapse():
                self.entangle(move.posList[0], move.posList[1])

        if self.cycleDetected and self.movesTree.move.isCollapse():
            self.cycleDetected = False

        return moveNum

    def evaluateCell(self, move):
        '''
        Perform the collapse move. Bring 'markValue' in 'pos0' back to
        classical state. Bring every other mark in 'pos0' back to their
        classical states wherever they exist apart from 'pos0'. 
        Recursively perform this operation until each cell in the cycle
        is evaluated.

        Scores are updated as a cell is turned into a classical state.
        '''
        self.updateMovesHistory(move)

        # Get a list marks in the target cell. Remove the mark that is
        # collapsing in the target cell.
        marksList = self.board[move.posList[0]].marksList[:]
        marksList.remove(move.markValue)

        # Assign the classical state of the target cell.
        self.board[move.posList[0]].stable = move.markValue

        # For each mark in 'marksList', find their respective twin location.
        # Recursively play a collapse move on that cell.
        for mark in marksList:
            for pos1 in self.board.keys():
                if mark in self.board[pos1].marksList and not self.board[pos1].stable:
                    self.evaluateCell(Move(mark, [pos1]))
                    break

        # Collapse procedure has terminated.
        self.cycleDetected = False

    def printTree(self, file=None):
        '''
        Output moves in chronological order, using depth-first traversal.
        '''
        root = self.movesTree.get_root()
        def dfs(node, depth):
            if node is None:
                return

            if node.move is None:
                if file is not None:
                    file.write('INIT_STATE ')
                print('INIT_STATE', end=' ')

            else:
                if file is not None:
                    file.write(('.'*depth)+str(node.move)+' ')
                print(('.'*depth)+str(node.move), end=' ')

            if node.move == self.movesTree.move:
                if file is not None:
                    file.write('<---')
                print('<---')
            else:
                print()

            if file is not None:
                file.write('\n')

            for key in node.children.keys():
                dfs(node.children[key], depth+1)

        if file is not None:
            file.write('SIZE='+str(self.board_size)+'\n')

        dfs(root, 0)

    def resetTree(self, moveStr):
        '''
        resets the display position of the board to the 
        move whose string is 'moveStr'
        '''
        def dfs(node):
            if node.move.__str__() == moveStr:
                self.movesTree = node

            else:
                for key in node.children.keys():
                    dfs(node.children[key])

        root = self.movesTree.get_root()
        dfs(root)

    def getMoves(self):
        '''
        Return a list of legal moves from the current
        state of the board.

        NEED TO TEST

        Implement in server.py for player-computer 
        interaction.
        '''
        if self.cycleDetected:
            return self.movesTree.move.posList

        else:
            posList = list()
            for row in range(self.board_size):
                for col in range(self.board_size):
                    if not self.board[(row,col)].stable:
                        posList.append((row,col))

            return posList

    def neighbourhoodCells(self, pos):
        nbd_cells = list()
        for i in [-1,0,1]:
            for j in [-1,0,1]:
                if (i or j):
                    if(self.isValidCell((pos[0] + i, pos[1] + j)) and self.board[(pos[0] + i, pos[1] + j)].stable is not None):
                        nbd_cells.append((pos[0] + i, pos[1] + j))
        return nbd_cells
    
    def degree(self, pos):
        deg = 0
        for n_cell in self.neighbourhoodCells(pos):
            if (self.board[n_cell].stable[0] == self.board[pos].stable[0]):
                deg += 1
        return deg 

    def isValidCell(self, pos):
        return not (pos[0] < 0 or pos[0] >= self.board_size or pos[1] < 0 or pos[1] >= self.board_size)

# -------------------------------------------------------------------
