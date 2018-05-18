'''
_move.py implements classes storing information about
an action in the game.
'''

class Move:
    def __init__(self, markValue = None, posList = None):
        '''
        Stores the value of the marks placed, where the marks were 
        placed.
        '''
        self.markValue = markValue
        self.posList = posList

    def __str__(self):
        '''
        returns 'move' object in string format.
        '''

        moveStr = self.markValue+'-'+str(self.posList[0][0])+'-'+\
            str(self.posList[0][1])
        if not self.isCollapse():
            moveStr += '-'+str(self.posList[1][0])+'-'+\
            str(self.posList[1][1])
        return moveStr

    def isCollapse(self):
        return len(self.posList) == 1

    def read(self, inStr):
        '''
        provided input 'inStr', parses 'inStr' into markValue and
        posList. Assumes 'inStr' follows the parsing rules.
        '''
        inStrList = inStr.split('-')

        # set markValue
        self.markValue = inStrList[0]

        # set positions
        self.posList = list()
        self.posList.append( ( int(inStrList[1]), int(inStrList[2]) ) )

        # if not a collapse move, set the second position
        if len(inStrList) == 5:
            self.posList.append( ( int(inStrList[3]), 
                int(inStrList[4]) ) )

    def getMark(self):
        '''
        Assumes the move has been read already.
        '''
        return self.markValue

class TypeError(Exception):
    def __init__(self, msg):
        self.message = msg

class MoveNode:
    def __init__(self):

        '''
        Implementation of MoveNode class helps create a tree of 
        nodes relating to the moves in the game in chronological
        order.
        parent   - stores a pointer to the parent of the node.
        move     - stores an instance of the 'Move' class associating 
            the node.
        children - map from (index,index) to an instance of move class
            referring to the move placed at positions corresponding to
            the two indices by the get_key() method.
        '''

        self.parent = None
        self.move = None
        self.children = dict()

    def add_child(self, key, move):
        '''
        Creates/updates the child corresponding to 'move' with key 
        'key'. Assumes 'key' is suitable to store 'move' as 
        a child. Checks if 'move' is indeed an instance of the 
        'Move' class.
        '''

        if not isinstance(move, Move):
            raise TypeError("Argument not of 'MoveNode' type.")

        if key not in list(self.children.keys()):
            self.children[key] = MoveNode()

        self.children[key].parent = self
        self.children[key].move = move

    def get_moves(self):
        '''
        Returns a list of moves from 'self' upto its root.
        '''
        _tree = self
        movesList = list()
        while _tree.move is not None:
            movesList.append(_tree.move)
            _tree = _tree.parent

        return movesList

    def has_children(self):
        return len(self.children) > 0

    def get_root(self):
        '''
        Returns the root node of the tree if exists, otherwise returns
        None.
        '''
        node = self
        while node.parent is not None:
            node = node.parent

        return node

    def is_root(self):
        return self.parent is None

    def __str__(self):
        outStr = self.move.markValue + str(self.move.posList[0])
        if len(self.move.posList) > 1:
            outStr += str(self.move.posList[1])
        return outStr