from os import system
from time import sleep
from msvcrt import getch
from colorama import Fore, Back, Style
from random import randint, choice

HEIGHT = 6
WIDTH = 7

#(n = one board dimension)

#O(1)
#Asks the player if they wish to play against their friend or the computer
#And reads the rules to the player
def init_game():

    playAI = 0

    #determines play vs player or AI
    while(not(playAI == 1 or playAI == 2)):
        system('cls')
        print(Back.BLACK + '.')
        system('cls')
        print("Select one: \n\n(1): 2 players \n(2): play versus ai\n")

        playAI = getch()
        if playAI == b'1' or playAI == b'2':
            playAI = int(playAI)

    rules = 0

    #outputs rules on choice
    while(not(rules == b'1' or rules == b'2')):
        system('cls')
        print("Select one: \n\n(1): View rules and controls \n(2): Play game without viewing rules or controls")
        rules = getch()

    system('cls')

    if rules == b'1':
        print("Controls: \n\n'a': move left \n'd': move right \n's': drop piece in current column \n'q': quit game \n\n")
        print("Rules: \n\nConnect four of your colored checker pieces in a row.")
        print("This can be done horizontally, vertically or diagonally.")
        print("Each player will drop in one checker piece at a time.")
        print("This will give you a chance to either build your row, or stop your opponent from getting four in a row.")
        print("The game is over either when you or your opponent reaches four in a row, ")
        print("or when all forty two slots are filled, ending in a stalemate. ")
        system('pause')

    return True if playAI == 2 else False

#O(1)
#Asks the player if they would like to play first or second against AI
def init_firstplayer(playAI):
    if playAI:
        first = False
        while not(first == b'1' or first == b'2'):
            system('cls')
            print("Would you like to play first? (1 for Yes, 2 for No)")
            first = getch()

        if first == b'2':
            return 'o'

    return 'x'

#O(n)
#initializes a blank top row with a player piece 'x' in the center column
def init_topRow(topRow, xPos, player):

    for i in range(WIDTH):
        topRow.append(' ')
    topRow[xPos] = player

    return topRow

#O(n**2)
#initializes an empty 6x7 board with '-' representing empty playable spaces
def init_board(board):

    for i in range(HEIGHT):
        board.append([])
        for j in range(WIDTH):
            board[i].append('-')

    return board

#O(1)
#displays moveing a piece in the top row
def updateTopRow(topRow, xPos, newxPos, player):

    topRow[xPos] = ' '
    topRow[newxPos] = player

    return topRow

#O(1)
#displays dropping a piece on the board
def updateboard(board, xPos, yPos, player):
    board[yPos][xPos] = player

    return board

#O(1)
#determines if a recent move won the game
def win(board, xPos, yPos, player):

    if yPos == None:
        return False

    inarow = 1
    error = False

    #vertical check
    for i in range(1, 4):
        if yPos + i >= HEIGHT:
            break
        if board[yPos + i][xPos] == player:
            inarow += 1
        else:
            break

    if inarow >= 4:
        return True

    #horizontal check
    inarow = 1
    for i in range(1, 4):
        if error:
            error = False
            break
        if xPos + i >= WIDTH:
            break
        if board[yPos][xPos + i] == player:
            inarow += 1
        else:
            break
    for i in range(1, 4):
        if error:
            error = False
            break
        if xPos - i < 0:
            break
        if board[yPos][xPos - i] == player:
            inarow += 1
        else:
            break

    if inarow >= 4:
        return True

    #negative diagonal check
    inarow = 1
    for i in range(1, 4):
        if yPos + i >= HEIGHT or xPos + i >= WIDTH:
            break
        if board[yPos + i][xPos + i] == player:
            inarow += 1
        else:
            break
    for i in range(1, 4):
        if yPos - i < 0 or xPos - i < 0:
            break
        if board[yPos - i][xPos - i] == player:
            inarow += 1
        else:
            break

    if inarow >= 4:
        return True

    #positive diagonal check
    inarow = 1
    for i in range(1, 4):
        if yPos - i < 0 or xPos + i >= WIDTH:
            break
        if board[yPos - i][xPos + i] == player:
            inarow += 1
        else:
            break
    for i in range(1, 4):
        if yPos + i >= HEIGHT or xPos - i < 0:
            break
        if board[yPos + i][xPos - i] == player:
            inarow += 1
        else:
            break

    if inarow >= 4:
        return True

    return False

#O(n)
#gets an array of all playable columns
def getvalidmoves(board):
    possibleMoves = [3, 4, 2, 5, 1, 6, 0] #a more optimal minimax search sequence for pruning (middle first, outside last)
    validMoves = []
    for aMove in possibleMoves:
        if board[0][aMove] == '-':
            validMoves.append(aMove)

    return validMoves

#O(1)
#performs calculations for moving left or right
def move(char, xPos):
    #move left
    if char == b'a':
        if xPos > 0:
            xPos -= 1
        else:
            xPos = WIDTH - 1

    #move right
    elif char == b'd':
        if xPos < WIDTH - 1:
            xPos += 1
        else:
            xPos = 0

    return xPos

#O(logn)
#performs calculations for dropping a piece on the board
def drop(board, xPos, player):

    #drop chip using binary search
    start = 0
    end = HEIGHT - 1

     #this case is no longer necessary but is left as commented code to note that it has been accounted for
    # if board[0][xPos] != '-': #if the column is already full
    #     return board

    #O(logn) binary search
    while start <= end and not (start == 0 and end == 0):
        midIndex = (start + end) / 2

        #round up
        if midIndex % 1 != 0:
            midIndex = (midIndex // 1) + 1
        midIndex = int(midIndex)

        midValue = board[midIndex][xPos]
        aboveMidValue = board[midIndex - 1][xPos]

        if midValue != '-' and aboveMidValue == '-':
            #just right
            break
        elif midValue == '-' and aboveMidValue == '-':
            #too high
            start = midIndex + 1
        elif midValue != '-' and aboveMidValue != '-':
            #too low
            end = midIndex - 1

    #update the board
    if board[midIndex][xPos] == '-': #the first piece in a column
        yPos = midIndex
    else:
        yPos = midIndex - 1

    return yPos

#O(n)
#increases or decreases the score of a simulated future move for the AI
def addscore(searchDirection, player, depth, startDepth):

    #pass in depth and assign score relative to depth to play win with least depth
    score = 0
    depthScore = 5 * (startDepth - depth)
    if player == 'o':
        opponent = 'x'
    else:
        opponent = 'o'

    #O(n)
    playerCount = searchDirection.count(player)
    opponentCount = searchDirection.count(opponent)
    emptyCount = 4 - playerCount - opponentCount

    #O(1)
    if playerCount == 4:
        score += 999999
    elif playerCount == 3 and emptyCount == 1:
        score += 10
    elif playerCount == 2 and emptyCount == 2:
        score += 4

    if opponentCount == 4:
        score -= 999999
    if opponentCount == 3 and emptyCount == 1:
        score -= 8
    if opponentCount == 2 and emptyCount == 2:
        score -= 3

    score -= depthScore
    return score

#O(n**2) disregarding addscore, otherwise O(n**3)
#creates all 4-in-a-row search windows on the board to assign scores to
def boardscore(board, player, depth, startDepth):

    tempSearch = []
    score = 0

    #vertical search
    for i in range(WIDTH):
        tempSearch = []
        for j in range(HEIGHT):
            tempSearch.append(board[j][i])
        for j in range(HEIGHT - 3):
            verticalSearch = tempSearch[j:j+4]
            score += addscore(verticalSearch, player, depth, startDepth)

    #horizontal search
    for i in range(HEIGHT):
        tempSearch = []
        for j in range(WIDTH):
            tempSearch.append(board[i][j])
        for j in range(WIDTH - 3): # four in a row search from the left ends at column 3
            horizontalSearch = tempSearch[j:j+4]
            score += addscore(horizontalSearch, player, depth, startDepth)

    #negative diagonal search
    for w in range(WIDTH - 3):
        for i in range(HEIGHT - 3):
            tempSearch = []
            negativeSearch = []
            for j in range(WIDTH - 3):
                tempSearch.append(board[i + j][j + w])
            negativeSearch = tempSearch
            score += addscore(negativeSearch, player, depth, startDepth)

    #positive diagonal search
    for w in range(WIDTH - 3):
        for i in range(3, HEIGHT):
            tempSearch = []
            positiveSearch = []
            for j in range(WIDTH - 3):
                tempSearch.append(board[i - j][j + w])
            positiveSearch = tempSearch
            score += addscore(positiveSearch, player, depth, startDepth)

    if player == 'x':
        opponent = 'o'
    else:
        opponent = 'x'
    center = []
    centerLeft = []
    centerRight = []
    for i in range(HEIGHT):
        center.append(board[i][WIDTH // 2])
        centerRight.append(board[i][(WIDTH // 2) + 1])
        centerLeft.append(board[i][(WIDTH // 2) - 1])
    score += 6 * center.count(player)
    score -= 5 * center.count(opponent)
    score += 3 * centerRight.count(player)
    score -= 2 * centerRight.count(opponent)
    score += 3 * centerLeft.count(player)
    score -= 2 * centerLeft.count(opponent)

    return score

#O(n)
#determines if the board is full
def boardisfull(board):

    if '-' in board[0]:
        return False

    return True

#O(depth**n)
#finds the AI's best move up to depth simulated moves in the future
def bestmove(depth, startDepth, board, alpha, beta, xPos, yPos, player):

    if player == 'x':
        opponent = 'o'
    else:
        opponent = 'x'

    #recursive base case
    if depth == 0 or win(board, xPos, yPos, opponent) or boardisfull(board):
        #output(board, [' ',' ',' ',' ',' ',' ',' '])
        #sleep(1)
        if player == 'x':
            return boardscore(board, opponent, depth, startDepth) #opponent because they made the most recent move
        else:
            return boardscore(board, opponent, depth, startDepth)  * (-1) #opponent because they made the most recent move

    tempboard = []
    validmoves = getvalidmoves(board)

    #minimax algorithm
    if player == 'o': #'o' is maximizing player

        maxEval = -999999999

        for aMove in validmoves:
            tempBoard = []
            for row in board:
                tempBoard.append(row[:]) #copy of board that doesn't point to board
            yPos = drop(tempBoard, aMove, player)
            tempBoard = updateboard(tempBoard, aMove, yPos, player)

            eval = bestmove(depth - 1, startDepth, tempBoard, alpha, beta, aMove, yPos, 'x')

            if maxEval < eval:
                if depth == startDepth: #to return the column with the best score on the final recursive step instead of the score itself
                    maxMove = aMove
                maxEval = eval
                alpha = max(alpha, maxEval) #pruning
            if beta <= alpha:
                break

        if depth == startDepth:
            return maxMove
        else:
            return maxEval

    elif player == 'x': #player is minimizing player

        minEval = 999999999
        for aMove in validmoves:
            tempBoard = []
            for row in board:
                tempBoard.append(row[:]) #copy of board that doesn't point to board
            yPos = drop(tempBoard, aMove, player)
            tempBoard = updateboard(tempBoard, aMove, yPos, player)

            eval = bestmove(depth - 1, startDepth, tempBoard, alpha, beta, aMove, yPos, 'o')

            if minEval > eval:
                if depth == startDepth:
                    minMove = aMove
                minEval = eval
                beta = min(beta, minEval) #pruning
            if beta <= alpha:
                break

        if depth == startDepth:
            return minMove
        else:
            return minEval

#O(n**2) disregarding bestmove, othwewise O(depth**n)
#moves AI piece on the display
def AImove(board, topRow, xPos, player):

    DEPTH = 7 #depth of minimax search

    AIpos = bestmove(DEPTH, DEPTH, board, -999999999, 999999999, xPos, None, player)
    newxPos = xPos

    #AI moving piece
    while AIpos != xPos:
        if AIpos > xPos:
            newxPos += 1
        else:
            newxPos -= 1
        topRow = updateTopRow(topRow, xPos, newxPos, player)
        xPos = newxPos
        sleep(0.1)
        output(board, topRow)

    return xPos

#O(n**2)
#outputs the board and topRow
def output(board, topRow):

    system('cls')

    print(Fore.WHITE + Style.BRIGHT + ' ', end = '')

    for i in range(WIDTH):
        if topRow[i] == 'x':
            print(Fore.RED + Style.BRIGHT + topRow[i], end = '')
        if topRow[i] == 'o':
            print(Fore.YELLOW + Style.BRIGHT + topRow[i], end = '')
        if topRow[i] == ' ':
            print(Fore.WHITE + Style.BRIGHT + topRow[i], end = '')

        print(Fore.WHITE + Style.BRIGHT + ' ', end = '')

    print()

    for i in range(HEIGHT):
        print(Fore.WHITE + Style.BRIGHT + '|', end = '')

        for j in range(WIDTH):
            if board[i][j] == 'x':
                print(Fore.RED + Style.BRIGHT + board[i][j], end = '')
            if board[i][j] == 'o':
                print(Fore.YELLOW + Style.BRIGHT + board[i][j], end = '')
            if board[i][j] == '-':
                print(Fore.WHITE + Style.BRIGHT + board[i][j], end = '')

            print(Fore.WHITE + Style.BRIGHT + '|', end = '')

        print()

#O(1) disregarding output(), otherwise O(n**2)
#displays endgame messages
def endgame(board, topRow, gameWon, player):
    output(board, topRow)

    if gameWon:
        if player == 'x':
            print(Fore.RED + Style.BRIGHT + "Player : " + player + " wins!!")
        if player == 'o':
            print(Fore.YELLOW + Style.BRIGHT + "Player : " + player + " wins!!")
    else:
        print(Fore.WHITE + Style.BRIGHT + "The game resulted in a draw.")
    print(Fore.WHITE)

#O(n**2) disregarding function calls, otherwise O(depth**n)
#enforces the rules of connect 4
def main():
    realBoard = []
    realtopRow = []
    xPos = 3
    yPos = 0
    gameWon = False

    playAI = init_game()
    player = init_firstplayer(playAI)
    realtopRow = init_topRow(realtopRow, xPos, player)
    realBoard = init_board(realBoard)

    output(realBoard, realtopRow)

    while not boardisfull(realBoard): #O(n**2)
        #player turn
        if(not playAI or (playAI and player == 'x')):
            char = getch()
            if char == b'q':
                break
            elif char == b'a' or char == b'd':
                newxPos = move(char, xPos)
                realtopRow = updateTopRow(realtopRow, xPos, newxPos, player)
                xPos = newxPos
            elif char == b's':
                if realBoard[0][xPos] == '-':
                    yPos = drop(realBoard, xPos, player)
                    realBoard = updateboard(realBoard, xPos, yPos, player)
                    gameWon = win(realBoard, xPos, yPos, player)
                    if(gameWon):
                        break
                    if player == 'x':
                        player = 'o'
                    else:
                        player = 'x'
                    realtopRow = updateTopRow(realtopRow, xPos, xPos, player)
            else: #invalid input case
                continue
        else:
            #AI turn
            xPos = AImove(realBoard, realtopRow, xPos, player)
            yPos = drop(realBoard, xPos, player)
            realBoard = updateboard(realBoard, xPos, yPos, player)
            sleep(0.1)
            gameWon = win(realBoard, xPos, yPos, player)
            if(gameWon):
                break
            if player == 'x':
                player = 'o'
            else:
                player = 'x'
            realtopRow = updateTopRow(realtopRow, xPos, xPos, player)
        output(realBoard, realtopRow)

    endgame(realBoard, realtopRow, gameWon, player)

if __name__ == "__main__":
    main()
