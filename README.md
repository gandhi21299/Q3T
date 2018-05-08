Quantum Tic-tac-toe Game engine -- README

Author: Computing Numbers



Game description
-----------------------------------------------------------------
Quantum tic-tac-toe is a 'quantum generalization' of 
tic-tac-toe in which the players' moves are 
superpositions of plays in the classical game. 

Properties:
    - Superposition: the ability of quantum objects to be 
    in two places at once.

    - Entanglement:  the phenomenon where distant parts 
    of a quantum system display correlations that 
    cannot be explained by either timelike causality 
    or common cause.

    - Collapse:      the phenomenon where the quantum 
    states of a system are reduced to classical states.

Gameplay
-----------------------------------------------------------------
    - Quantum tic-tac-toe is played on a square board. 
    Denote n as the number of rows/columns. 
    Initially the board is empty.

    - Players take turns by placing a mark in two 
    distinct cells on the board.

    For example, X plays on (3,1) and (3,3). Following, O plays on 
	(0,2) and (0,3). Then the board configuration looks like the
	following:


      0            1            2            3      
    ----------------------------------------------------
   |             |            |o2          |o2          |
0  |             |            |            |            |  0
   |             |            |            |            |
   |             |            |            |            |
    ----------------------------------------------------
   |             |            |            |            |
1  |             |            |            |            |  1
   |             |            |            |            |
   |             |            |            |            |
    ----------------------------------------------------
   |             |            |            |            |
2  |             |            |            |            |  2
   |             |            |            |            |
   |             |            |            |            |
    ----------------------------------------------------
   |             |x1          |            |x1          |
3  |             |            |            |            |  3
   |             |            |            |            |
   |             |            |            |            |
    ----------------------------------------------------
      0            1            2            3      


    - By superposition, each pair of marks with the same mark value, 
    ,i.e., the mark and the move number concatenated. eg. 'x1',
    are connected. This interaction causes the cells to connect
    to other cells. In the example above, x1 causes a connection
    between the cells (3,1) and (3,3).

    - Eventually, these connections form a cyclic entanglement on
    the board. A cyclic entanglement occurs when a several cells
    in a chain form a cycle. Consider the following example, 
    cells (0,0), (0,1) and (1,0) are connected in a cycle.


      0            1            2            3      
    ----------------------------------------------------
   | x1  x3      | x1  o2     |            |            |
0  |             |            |            |            |  0
   |             |            |            |            |
   |             |            |            |            |
    ----------------------------------------------------
   | o2  x3      |            |            |            |
1  |             |            |            |            |  1
   |             |            |            |            |
   |             |            |            |            |
    ----------------------------------------------------
   |             |            |            |            |
2  |             |            |            |            |  2
   |             |            |            |            |
   |             |            |            |            |
    ----------------------------------------------------
   |             |            |            |            |
3  |             |            |            |            |  3
   |             |            |            |            |
   |             |            |            |            |
    ----------------------------------------------------
      0            1            2            3      

    - When the board attains a cyclic entanglement state, every 
    mark connected within/to the cycle must 'collapse', that is,
    turn back into classical states. In the example above, X 
    played the last move on cells (0,0) and (1,0), forming a 
    cycle. Then on the next move, O must choose one of the
    positions where X played the cycle-forming move, to begin 
    the so-called collapse procedure. 

    - Collapse Procedure: Using the same example as above, let us 
    say that O chooses cell (0,0) to run collapse from. Then O has
    chosen x3 from (0,0) to take over that cell. Each cell may
    only hold upto one mark in classical state, hence every other
    quantum mark is destroyed because of the collapse. In this 
    example, collapse of x3 causes x1 to be destroyed. 

    Now recursively collapse each destroyed quantum mark in their
    respective 'twin' cells. For instance, since x1 was destroyed
    in (0,0), x1 collapses in (0,1). Consequently, o2 is destroyed
    in (0,1) while take over the cell (1,0). The collapse calls
    terminate once each mark involved in the cycle are collapsed.

Program utility
-----------------------------------------------------------------
Use 'python3 server.py <n>' to initialize the game with a board
of size n. (Ignore the angled-brackets)

Ignorance of <n> will yeild a board with size 4, that is, using 
'python3 server.py' instead.

Server commands:
- play <R1> <C1> <R2> <C2> 
    to play at positions (R1, C1) and 
    (R2, C2).

- play <R1> <C1> 
    to play at position (R1, C1).

- undo
    to undo the last move.

- undo <k>
    undo k moves back, if at least k moves have already been played.

- tree
    view game.movesTree

- save <file-path>
    saves game to the provided file path.

- load <file-path>
    loads game from the indicated file path.

- random <k>
    random player plays k moves.

- exit
    exits the game.