def printBoard(game):
    """
    Given 'game', an instance of game.Game class, print the board to stdo.
    
    """

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
                elif k == 6:  print("    \\/     |", end="")
                elif k == 9:  print("     /\\    |", end="")
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
    print()
    print()
    
    print('SCORES: X = '+str(game.score['x'])+' O = '+str(game.score['o']))

def computeLongestKrist(game):
    '''
    Returns the longest krist in game.board.
    '''
    
    maxn = dict()
    maxn['x'] = list()
    maxn['o'] = list()
    for n in range(1, game.board_size+1):
        maxn['x'].append([n, 0])
        maxn['o'].append([n, 0])
    
    for row in range(game.board_size):
        for col in range(game.board_size):
            if game.board[(row,col)].stable:
                mark = game.board[(row,col)].stable[0]

                # check horizontal krist
                c = col+1
                while c < game.board_size:
                    
                    if game.board[(row,c)].stable is None:
                        break
                    
                    if game.board[(row,c)].stable[0] != mark:
                        break

                    c += 1
                maxn[mark][c-col-1][1] += 1

                # check vertical krist
                r = row+1
                while r < game.board_size:
                    
                    if game.board[(r,col)].stable is None:
                        break
                    if game.board[(r,col)].stable[0] != mark:
                        break
                    r += 1
                maxn[mark][r-row-1][1] += 1

                # check diagonal krist topleft - bottom right
                r = row+1
                c = col+1
                while r < game.board_size and c < game.board_size:
                    if game.board[(r,c)].stable is None:
                        break
                    
                    if game.board[(r,c)].stable[0] != mark:
                        break

                    r += 1
                    c += 1
                maxn[mark][r-row-1][1] += 1

                # check diagonal krist top right - bottom left
                r = row+1
                c = col-1
                while r < game.board_size and c >= 0:
                    if game.board[(r,c)].stable is None:
                        break
                    
                    if game.board[(r,c)].stable[0] != mark:
                        break

                    r += 1
                    c -= 1
                
                maxn[mark][r-row-1][1] += 1

    
    i = 0
    while maxn['o'][i][1] != 0 or maxn['x'][i][1] != 0:
        i += 1

        if i > game.board_size-1:
            break

    i -= 1

    return (maxn['x'][i][0]*maxn['x'][i][1], maxn['o'][i][0]*maxn['o'][i][1])