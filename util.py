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
    print()
    print()
    
    print('SCORES: X = '+str(game.score['x'])+' O = '+str(game.score['o']))