#      ___    ____
#     /   |  /  _/
#    / /| |  / /  
#   / ___ |_/ /   
#  /_/  |_/___/   


import random, board, math, time, os

#Placement Values

pawnPlacementWhite = [
    [0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0],
    [5.0,  5.0,  5.0,  5.0,  5.0,  5.0,  5.0,  5.0],
    [1.0,  1.0,  2.0,  3.0,  3.0,  2.0,  1.0,  1.0],
    [0.5,  0.5,  1.0,  2.5,  2.5,  1.0,  0.5,  0.5],
    [0.0,  0.0,  0.0,  2.0,  2.0,  0.0,  0.0,  0.0],
    [0.5, -0.5, -1.0,  0.0,  0.0, -1.0, -0.5,  0.5],
    [0.5,  1.0, 1.0,  -2.0, -2.0,  1.0,  1.0,  0.5],
    [0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0]
]

knightPlacementWhite = [
    [-5.0, -4.0, -3.0, -3.0, -3.0, -3.0, -4.0, -5.0],
    [-4.0, -2.0,  0.0,  0.0,  0.0,  0.0, -2.0, -4.0],
    [-3.0,  0.0,  1.0,  1.5,  1.5,  1.0,  0.0, -3.0],
    [-3.0,  0.5,  1.5,  2.0,  2.0,  1.5,  0.5, -3.0],
    [-3.0,  0.0,  1.5,  2.0,  2.0,  1.5,  0.0, -3.0],
    [-3.0,  0.5,  1.0,  1.5,  1.5,  1.0,  0.5, -3.0],
    [-4.0, -2.0,  0.0,  0.5,  0.5,  0.0, -2.0, -4.0],
    [-5.0, -4.0, -3.0, -3.0, -3.0, -3.0, -4.0, -5.0]
]

bishopPlacementWhite = [
    [ -2.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -2.0],
    [ -1.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -1.0],
    [ -1.0,  0.0,  0.5,  1.0,  1.0,  0.5,  0.0, -1.0],
    [ -1.0,  0.5,  0.5,  1.0,  1.0,  0.5,  0.5, -1.0],
    [ -1.0,  0.0,  1.0,  1.0,  1.0,  1.0,  0.0, -1.0],
    [ -1.0,  1.0,  1.0,  1.0,  1.0,  1.0,  1.0, -1.0],
    [ -1.0,  0.5,  0.0,  0.0,  0.0,  0.0,  0.5, -1.0],
    [ -2.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -2.0]
]

rookPlacementWhite = [
    [  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0],
    [  0.5,  1.0,  1.0,  1.0,  1.0,  1.0,  1.0,  0.5],
    [ -0.5,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -0.5],
    [ -0.5,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -0.5],
    [ -0.5,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -0.5],
    [ -0.5,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -0.5],
    [ -0.5,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -0.5],
    [  0.0,   0.0, 0.0,  0.5,  0.5,  0.0,  0.0,  0.0]
]

queenPlacement = [
    [ -2.0, -1.0, -1.0, -0.5, -0.5, -1.0, -1.0, -2.0],
    [ -1.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -1.0],
    [ -1.0,  0.0,  0.5,  0.5,  0.5,  0.5,  0.0, -1.0],
    [ -0.5,  0.0,  0.5,  0.5,  0.5,  0.5,  0.0, -0.5],
    [  0.0,  0.0,  0.5,  0.5,  0.5,  0.5,  0.0, -0.5],
    [ -1.0,  0.5,  0.5,  0.5,  0.5,  0.5,  0.0, -1.0],
    [ -1.0,  0.0,  0.5,  0.0,  0.0,  0.0,  0.0, -1.0],
    [ -2.0, -1.0, -1.0, -0.5, -0.5, -1.0, -1.0, -2.0]
]

kingPlacementWhite = [
    [ -3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
    [ -3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
    [ -3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
    [ -3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
    [ -2.0, -3.0, -3.0, -4.0, -4.0, -3.0, -3.0, -2.0],
    [ -1.0, -2.0, -2.0, -2.0, -2.0, -2.0, -2.0, -1.0],
    [  2.0,  2.0,  0.0,  0.0,  0.0,  0.0,  2.0,  2.0 ],
    [  2.0,  3.0,  1.0,  0.0,  0.0,  1.0,  3.0,  2.0 ]
]

pieceValues = {"King": 9000, "Pawn": 100, "Knight": 300, "Bishop": 300, "Queen": 900, "Rook": 500}

neccessaryImgs = [r"ChessImages\Chess_rlt60.png",
                  r"ChessImages\Chess_rdt60.png"]

def findTotalValueAfterMove(grid, piece, move):
    value = 0
    
    boardCopy = [[None for i in range(8)] for j in range(8)]
    for y in range(len(boardCopy)):
        for x in range(len(boardCopy[0])):
            if grid[y][x] != None:
                boardCopy[y][x] = board.Piece(grid[y][x].typeOfPiece, grid[y][x].color, (y, x), grid[y][x].img)

    gridCopy = board.Grid(boardCopy)
        
    gridCopy.deleteCellContents(move[0], move[1])
    gridCopy.grid[move[0]][move[1]] = gridCopy.grid[piece.coord[0]][piece.coord[1]]
    gridCopy.deleteCellContents(piece.coord[0], piece.coord[1])
    gridCopy.grid[move[0]][move[1]].changeCoordinates(move[0], move[1])

    for row in gridCopy.grid:
        for cell in row:
            if cell != None:
                value += pieceValues[cell.typeOfPiece] * ((cell.color * -2) + 1)

    #print(value)
    return value
        

def findCurrentValue(grid):
    #if board.checkIfKingInCheck(grid, color):
        #if color == 0:
            #return -900
        #return 900
    valueCurrent = 0
    for row in grid:
        for cell in row:
            if cell != None:
                if cell.typeOfPiece == "Pawn":
                    if cell.color == 0:
                        valueCurrent += (pieceValues[cell.typeOfPiece] * ((cell.color * -2) + 1)) + pawnPlacementWhite[cell.coord[0]][cell.coord[1]] / 2
                    else:
                        valueCurrent += (pieceValues[cell.typeOfPiece] * ((cell.color * -2) + 1)) - pawnPlacementWhite[7 - cell.coord[0]][cell.coord[1]] / 2
                if cell.typeOfPiece == "Knight":
                    if cell.color == 0:
                        valueCurrent += (pieceValues[cell.typeOfPiece] * ((cell.color * -2) + 1)) + knightPlacementWhite[cell.coord[0]][cell.coord[1]] / 2
                    else:
                        valueCurrent += (pieceValues[cell.typeOfPiece] * ((cell.color * -2) + 1)) - knightPlacementWhite[7 - cell.coord[0]][cell.coord[1]] / 2
                if cell.typeOfPiece == "Bishop":
                    if cell.color == 0:
                        valueCurrent += (pieceValues[cell.typeOfPiece] * ((cell.color * -2) + 1)) + bishopPlacementWhite[cell.coord[0]][cell.coord[1]] / 2
                    else:
                        valueCurrent += (pieceValues[cell.typeOfPiece] * ((cell.color * -2) + 1)) - bishopPlacementWhite[7 - cell.coord[0]][cell.coord[1]] / 2
                if cell.typeOfPiece == "Rook":
                    if cell.color == 0:
                        valueCurrent += (pieceValues[cell.typeOfPiece] * ((cell.color * -2) + 1)) + rookPlacementWhite[cell.coord[0]][cell.coord[1]] / 2
                    else:
                        valueCurrent += (pieceValues[cell.typeOfPiece] * ((cell.color * -2) + 1)) - rookPlacementWhite[7 - cell.coord[0]][cell.coord[1]] / 2
                if cell.typeOfPiece == "King":
                    if cell.color == 0:
                        valueCurrent += (pieceValues[cell.typeOfPiece] * ((cell.color * -2) + 1)) + kingPlacementWhite[cell.coord[0]][cell.coord[1]] / 2
                    else:
                        valueCurrent += (pieceValues[cell.typeOfPiece] * ((cell.color * -2) + 1)) - kingPlacementWhite[7 - cell.coord[0]][cell.coord[1]] / 2
                if cell.typeOfPiece == "Queen":
                    valueCurrent += (pieceValues[cell.typeOfPiece] + queenPlacement[cell.coord[0]][cell.coord[1]] / 2) * ((cell.color * -2) + 1)
                        

    return valueCurrent

def findRandomMove(grid, color):
    allPiecesPossible = []

    for row in grid:
        for cell in row:
            if cell != None and cell.color == color and len(board.determineMoves(grid, cell)) > 0:
                allPiecesPossible.append(cell)

    notFound = True
    if len(allPiecesPossible) == 0:
        if board.checkIfKingInCheck(grid, color):
            return "Checkmate"
    pieceSelected = allPiecesPossible[random.randrange(len(allPiecesPossible))]
    allPossibleMoves = board.determineMoves(grid, pieceSelected)
    moveSelected = allPossibleMoves[random.randrange(len(allPossibleMoves))]
    return (pieceSelected, moveSelected)

def findRandomMovePlusValues(grid, color, depth):
    allPiecesPossible = []
    movesToSelectFrom = []

    mostValue = 100000
    minValue = -100000
    mostValuableMove = ()
    
    for row in grid:
        for cell in row:
            if cell != None and cell.color == color and len(board.determineMoves(grid, cell)) > 0:
                allPiecesPossible.append(cell)
    
    notFound = True
    if len(allPiecesPossible) == 0:
        if board.checkIfKingInCheck(grid, color):
            return "Checkmate"
        else:
            return "Draw"

    for piece in allPiecesPossible:
        for move in board.determineMoves(grid, piece):
            newValue = findTotalValueAfterMove(grid, piece, move)
            if color == 0:
                if newValue > minValue:
                    minValue = newValue
                    mostValuableMove = (piece, move)
                    movesToSelectFrom = [(piece, move)]
                if newValue == minValue:
                    movesToSelectFrom.append((piece, move))
            if color == 1:
                if newValue < mostValue:
                    mostValue = newValue
                    mostValuableMove = (piece, move)
                    movesToSelectFrom = [(piece, move)]
                if newValue == mostValue:
                    movesToSelectFrom.append((piece, move))

    #print(mostValuableMove)
    if len(movesToSelectFrom) > 0:
        return movesToSelectFrom[random.randrange(len(movesToSelectFrom))]
    return mostValuableMove


def minMaxGame(grid, color, depth):
    allPiecesPossible = []
    for row in grid:
        for cell in row:
            if cell != None and cell.color == color and len(board.determineMoves(grid, cell)) > 0:
                allPiecesPossible.append(cell)
    
    notFound = True
    if len(allPiecesPossible) == 0:
        if board.checkIfKingInCheck(grid, color):
            return "Checkmate"
        else:
            return "Draw"

    mmg = [[None for i in range(8)] for j in range(8)]
    for y in range(len(mmg)):
        for x in range(len(mmg[0])):
            if grid[y][x] != None:
                mmg[y][x] = board.Piece(grid[y][x].typeOfPiece, grid[y][x].color, (y, x), grid[y][x].img, grid[y][x].canCastle, grid[y][x].movesTaken)

    return minMax(mmg, color, depth, True, color, 1000000, -1000000)

#MINIMAX
def minMax(grid, color, depth, findMax, startColor, alpha, beta):
    minMaxGrid = board.Grid(grid)
    if depth == 0:
        #print(findCurrentValue(grid))
        return (None, None, findCurrentValue(grid))

    else:
        currentMax = 100000
        currentMin = -100000
        piecesChecked = []
        returnCell = None
        returnMove = None
        save = ((), (), None, None)
        allMoves = []
        
        for row in minMaxGrid.grid:
            for cell in row:
                if cell != None and cell.color == color:
                    for move in board.determineMoves(minMaxGrid.grid, cell):
                        if cell.coord != move:
                            allMoves.append((cell, move))

        #print(allMoves)
        allMovesPossible = [(None, None)]
        if findMax:
            bestVal = 1000000
            banishedCells = []
            if len(allMoves) == 0:
                if not depth == 3:
                    if board.checkIfKingInCheck(minMaxGrid.grid, startColor):
                        return (None, None, 90000 * (startColor * 2) - 1)
                    elif board.checkIfKingInCheck(minMaxGrid.grid, abs(startColor - 1)):
                        return (None, None, 90000 * (startColor * -2) + 1)
                    else:
                        return (None, None, 9000 * (startColor * 2) - 1)
                elif depth == 3:
                    if board.checkIfKingInCheck(minMaxGrid.grid, startColor):
                        return "Checkmate"
                    else:
                        return "Draw"
                    
            for row in minMaxGrid.grid:
                for cell in row:
                    if cell != None and cell.color == color:
                        for pieceMove in board.determineMoves(minMaxGrid.grid, cell):
                            if cell.coord != move:
                                move = (cell, pieceMove)
                                #print(banishedCells)
                                #print(str(bestValue) + "\n")
                                #if not move[0] in banishedCells:
                                save = (move[0].coord, move[1], minMaxGrid.grid[move[0].coord[0]][move[0].coord[1]], minMaxGrid.grid[move[1][0]][move[1][1]])
                                
                                minMaxGrid.movePiece(move[0].coord[0], move[0].coord[1], move[1][0], move[1][1], True, True)

                                
                                value = minMax(minMaxGrid.grid, abs(color - 1), depth - 1, False, startColor, alpha, beta)[2]
                                
                                #if depth == 3:
                                    #print("\n\nLayer 1:")
                                    #minMaxGrid.printBoard()
                                    #print(value)
                                #else:
                                    #print("\n\nLayer 3:")
                                    #minMaxGrid.printBoard()
                                    #print(value)
                                    
                                bestVal = min(bestVal, value)
                                alpha = min(alpha, bestVal)

                                if move[0].typeOfPiece == "King" and abs(save[0][1] - move[1][1]) == 2:
                                    if move[1][1] == 6:
                                        minMaxGrid.movePiece(move[0].coord[0], 5, move[0].coord[0], 7)
                                        minMaxGrid.grid[move[0].coord[0]][7].changeCoordinates(move[0].coord[0], 7)
                                        #minMaxGrid.grid[move[0].coord[0]][7] = board.Piece("Rook", move[0].color, (move[0].coord[0], 7), neccessaryImgs[move[0].color], False, 0)
                                    elif move[1][1] == 2:
                                        minMaxGrid.movePiece(move[0].coord[0], 3, move[0].coord[0], 0)
                                        minMaxGrid.grid[move[0].coord[0]][0].changeCoordinates(move[0].coord[0], 0)
                                        #minMaxGrid.grid[move[0].coord[0]][0] = board.Piece("Rook", move[0].color, (move[0].coord[0], 0), neccessaryImgs[move[0].color], False, 0)
                                minMaxGrid.grid[save[0][0]][save[0][1]] = save[2]
                                minMaxGrid.grid[save[1][0]][save[1][1]] = save[3]
                                if minMaxGrid.grid[save[0][0]][save[0][1]] != None:
                                    minMaxGrid.grid[save[0][0]][save[0][1]].changeCoordinates(save[0][0], save[0][1])
                                if minMaxGrid.grid[save[1][0]][save[1][1]] != None:
                                    minMaxGrid.grid[save[1][0]][save[1][1]].changeCoordinates(save[1][0], save[1][1])

                                #alphabeta
                                if beta >= alpha:
                                    #print(bestVal)
                                    #if depth == 3:
                                        #print(allMovesPossible[0][0], allMovesPossible[0][1], bestVal)
                                        #print("alphabeta found!")
                                    #print(allMovesPossible)
                                    return (allMovesPossible[0][0], allMovesPossible[0][1], bestVal)
                                    break

                                if startColor == 0:
                                    if value > currentMin:
                                        currentMin = value
                                        currentMax = None
                                        allMovesPossible = [move]
                                    elif value == currentMin:
                                        allMovesPossible.append(move)
                                    #else:
                                        #banishedCells.append(move[0])
                                        
                                if startColor == 1:
                                    if value < currentMax:
                                        currentMax = value
                                        currentMin = None
                                        allMovesPossible = [move]
                                    elif value == currentMax:
                                        allMovesPossible.append(move)
                                    #else:
                                        #banishedCells.append(move[0])
        else:

            bestVal = -1000000
            if len(allMoves) == 0:
                if board.checkIfKingInCheck(minMaxGrid.grid, abs(startColor - 1)):
                    return (None, None, 90000 * (startColor * -2) + 1)
                elif board.checkIfKingInCheck(minMaxGrid.grid, startColor):
                    return (None, None, 90000 * (startColor * 2) - 1)
                else:
                    return (None, None, 9000 * (startColor * 2) - 1)

            for row in minMaxGrid.grid:
                for cell in row:
                    if cell != None and cell.color == color:
                        for pieceMove in board.determineMoves(minMaxGrid.grid, cell):
                            move = (cell, pieceMove)
                            if cell.coord != move:
                                #print(move[0].coord)
                                save = (move[0].coord, move[1], minMaxGrid.grid[move[0].coord[0]][move[0].coord[1]], minMaxGrid.grid[move[1][0]][move[1][1]])
                                #print((cell.coord[0], cell.coord[1], move[0], move[1]))
                                minMaxGrid.movePiece(move[0].coord[0], move[0].coord[1], move[1][0], move[1][1], True, True)
                                #print(move[0])
                                #print(save[1])
                                #print(move[1])
                                #print("2d Layer")
                                value = minMax(minMaxGrid.grid, abs(color - 1), depth - 1, True, startColor, alpha, beta)[2]
                                #if depth == 2:
                                    #print("\n\nLayer 2:")
                                    #minMaxGrid.printBoard()
                                    #print(value)

                                bestVal = max(bestVal, value)
                                beta = max(beta, bestVal)

                                if move[0].typeOfPiece == "King" and abs(save[0][1] - move[1][1]) == 2:
                                    if move[1][1] == 6:
                                        minMaxGrid.movePiece(move[0].coord[0], 5, move[0].coord[0], 7)
                                        minMaxGrid.grid[move[0].coord[0]][7].changeCoordinates(move[0].coord[0], 7)
                                        #minMaxGrid.grid[move[0].coord[0]][7] = board.Piece("Rook", move[0].color, (move[0].coord[0], 7), neccessaryImgs[move[0].color], False, 0)
                                    elif move[1][1] == 2:
                                        minMaxGrid.movePiece(move[0].coord[0], 3, move[0].coord[0], 0)
                                        minMaxGrid.grid[move[0].coord[0]][0].changeCoordinates(move[0].coord[0], 0)
                                        #minMaxGrid.grid[move[0].coord[0]][0] = board.Piece("Rook", move[0].color, (move[0].coord[0], 0), neccessaryImgs[move[0].color], False, 0)
                                minMaxGrid.grid[save[0][0]][save[0][1]] = save[2]
                                minMaxGrid.grid[save[1][0]][save[1][1]] = save[3]
                                if minMaxGrid.grid[save[0][0]][save[0][1]] != None:
                                    minMaxGrid.grid[save[0][0]][save[0][1]].changeCoordinates(save[0][0], save[0][1])
                                if minMaxGrid.grid[save[1][0]][save[1][1]] != None:
                                    minMaxGrid.grid[save[1][0]][save[1][1]].changeCoordinates(save[1][0], save[1][1])

                                #alphabeta
                                if beta >= alpha:
                                    return (None, None, bestVal)
                                    break
                                #print("2:  " + str(value))
                                if startColor == 0:
                                    if value < currentMax:
                                        currentMax = value
                                        currentMin = None
                                        
                                if startColor == 1:
                                    if value > currentMin:
                                        currentMin = value
                                        currentMax = None

                #if save[2] != None
            allMovesPossible = [(None, None)]

        possibleMoveUsed = []
        possibleMoveUsed = allMovesPossible[random.randrange(len(allMovesPossible))]
        
        if currentMax == None:
            #print((returnCell.coord, returnMove[1], currentMin))
            return (possibleMoveUsed[0], possibleMoveUsed[1], currentMin)
        else:
            #print((returnCell.coord, returnMove[1], currentMax))
            return (possibleMoveUsed[0], possibleMoveUsed[1], currentMax)
