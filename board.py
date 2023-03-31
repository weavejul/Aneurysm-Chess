#      ____                       __
#     / __ )____  ____ __________/ /
#    / __  / __ \/ __ `/ ___/ __  / 
#   / /_/ / /_/ / /_/ / /  / /_/ /  
#  /_____/\____/\__,_/_/   \__,_/   
                                 
import math, time

#GLOBAL VARS

previousPieceMoved = ((0, 0), (0, 0), None)
isCheckMoveSolved = True
chessPieces = [r"ChessImages\Chess_pdt60.png",
               r"ChessImages\Chess_plt60.png",
               r"ChessImages\Chess_rdt60.png",
               r"ChessImages\Chess_rlt60.png",
               r"ChessImages\Chess_kdt60.png",
               r"ChessImages\Chess_klt60.png",
               r"ChessImages\Chess_qdt60.png",
               r"ChessImages\Chess_qlt60.png",
               r"ChessImages\Chess_ndt60.png",
               r"ChessImages\Chess_nlt60.png",
               r"ChessImages\Chess_bdt60.png",
               r"ChessImages\Chess_blt60.png",]


#GRID ##################################################################
########################################################################

class Grid():
    def __init__(self, grid = None):
        self.previousMove = []
        if grid != None:
            self.grid = grid
        else:
            self.grid = [[None for i in range(8)] for j in range(8)]

    #Sets the board to the standard chess game beginning
    def initializeStandardBoard(self):
        self.gridArray = [[None for i in range(8)] for j in range(8)]
        for i in range(8):
            self.grid[1][i] = Piece("Pawn", 1, (1, i), chessPieces[0])
            self.grid[6][i] = Piece("Pawn", 0, (6, i), chessPieces[1])
        for i in range(2):
            self.grid[0][i * 7] = Piece("Rook", 1, (0, i*7), chessPieces[2])
            self.grid[7][i * 7] = Piece("Rook", 0, (7, i*7), chessPieces[3])
        for i in range(2):
            self.grid[0][(i*5)+1] = Piece("Knight", 1, (0, (i*5)+1), chessPieces[8])
            self.grid[7][(i*5)+1] = Piece("Knight", 0, (7, (i*5)+1), chessPieces[9])
        for i in range(2):
            self.grid[0][(i*3)+2] = Piece("Bishop", 1, (0, (i*3)+2), chessPieces[10])
            self.grid[7][(i*3)+2] = Piece("Bishop", 0, (7, (i*3)+2), chessPieces[11])

        self.grid[0][3] = Piece("Queen", 1, (0, 3), chessPieces[6])
        self.grid[7][3] = Piece("Queen", 0, (7, 3), chessPieces[7])
        self.grid[0][4] = Piece("King", 1, (0, 4), chessPieces[4], True, 0)
        self.grid[7][4] = Piece("King", 0, (7, 4), chessPieces[5], True, 0)
        ####
        #self.grid[2][2] = piece.Piece("King", 0, (2, 2))
        ####

    #Deletes the content of a cell
    def deleteCellContents(self, y, x):
        #print(y)
        #print(x)
        #print(self.grid)
        self.grid[y][x] = None

    #Moves a piece from one cell to another
    def movePiece(self, y1, x1, y2, x2, ai = False, loop = False):
        global previousPieceMoved
        
        self.deleteCellContents(y2, x2)
        self.grid[y2][x2] = self.grid[y1][x1]
        self.deleteCellContents(y1, x1)
        self.grid[y2][x2].changeCoordinates(y2, x2)

        try:
            self.grid[y2][x2].hasTakenFirstMove = True
        except:
            print(y1, x1, y2, x2)
            #self.printBoard()
            time.sleep(1000)
        self.grid[y2][x2].canCastle = False

        if self.grid[y2][x2].typeOfPiece == "King":
            if abs(x2-x1) > 1:
                if x2 == 2:
                    self.movePiece(y1, 0, y1, 3)
                elif x2 == 6:
                    self.movePiece(y1, 7, y1, 5)

        elif self.grid[y2][x2].typeOfPiece == "Pawn":
            if abs(x2 - x1) == 1 and abs(y2 - y1) == 1:
                if previousPieceMoved[2] != None and previousPieceMoved[2].typeOfPiece == "Pawn":
                    if previousPieceMoved[1][0] == y2 and abs(previousPieceMoved[1][0] - previousPieceMoved[0][0]) == 2:
                        self.deleteCellContents(y2 - (2 * self.grid[y2][x2].color - 1), x2)
            
        if y2 == self.grid[y2][x2].color * 7 and self.grid[y2][x2].typeOfPiece == "Pawn":
            if ai:
                self.grid[y2][x2] = Piece("Queen", self.grid[y2][x2].color, (y2, x2), chessPieces[7 - self.grid[y2][x2].color])
            else:
                promotion = input("Promote to (q: Queen, r: Rook, b: Bishop, k: Knight): ")
                if promotion.lower() == "q":
                    self.grid[y2][x2] = Piece("Queen", self.grid[y2][x2].color, (y2, x2), chessPieces[7 - self.grid[y2][x2].color])
                elif promotion.lower() == "k":
                    self.grid[y2][x2] = Piece("Knight", self.grid[y2][x2].color, (y2, x2), chessPieces[9 - self.grid[y2][x2].color])
                elif promotion.lower() == "b":
                    self.grid[y2][x2] = Piece("Bishop", self.grid[y2][x2].color, (y2, x2), chessPieces[11 - self.grid[y2][x2].color])
                elif promotion.lower() == "r":
                    self.grid[y2][x2] = Piece("Rook", self.grid[y2][x2].color, (y2, x2), chessPieces[3 - self.grid[y2][x2].color])


        if not loop:
            self.grid[y2][x2].changeCastlePlusMoveState()
        previousPieceMoved = ((y1, x1), (y2, x2), self.grid[y2][x2])
        isCheckMoveSolved = True

        

    #Prints the board state (for debugging)
    def printBoard(self):
        strBoard = ""
        strBoard += "   a   b   c   d   e   f   g   h  X\n"
        for i in range(8):
            strBoard += str(8 - i) + " |"
            for j in range(8):
                if j == 7:
                    if self.grid[i][j] != None and self.grid[i][j].color == 0:
                        strBoard += returnLetterForPiece(self.grid[i][j]) + "|\n"
                    elif self.grid[i][j] != None and self.grid[i][j].color == 1:
                        strBoard += returnLetterForPiece(self.grid[i][j]).lower() + "|\n"
                    else:
                        strBoard += " |\n"
                else:
                    if self.grid[i][j] != None and self.grid[i][j].color == 0:
                        strBoard += (returnLetterForPiece(self.grid[i][j])) + " | "
                    elif self.grid[i][j] != None and self.grid[i][j].color == 1:
                        strBoard += (returnLetterForPiece(self.grid[i][j])).lower() + " | "
                    else:
                        strBoard += "  | "
            if i != 7:
                strBoard += "  |" + ("----" * 7) + "-|/n"
        return strBoard

#PIECE ##################################################################
#########################################################################

#The piece class represents all pieces on the board
                
class Piece():
    def __init__(self, typeOfPiece, color, coord, img, canCastle = False, movesTaken = 0):
        self.typeOfPiece = typeOfPiece
        # 0-White 1-Black
        self.color = color
        #Starts from zero
        self.coord = coord
        #(y, x)
        self.canCastle = canCastle
        self.movesTaken = movesTaken
        self.img = img

    #Changes the piece's coordinates.
    def changeCoordinates(self, y, x):
        self.coord = (y, x)

    def changeCastlePlusMoveState(self):
        self.canCastle = False
        self.movesTaken += 1


#MISC ##################################################################
########################################################################

#Is (y, x) inside the board?
def outOfBoard(y, x):
    if x < 0 or x > 7 or y < 0 or y > 7:
        return True
    return False

#if opposite color, you can capture it. King exception is left out for check testing. The king exception will be implemented in the 'move' function.
def canCapture(piece1, piece2):
    if piece1.color != piece2.color:
        return True
    return False

#Determine whether the King is in Check
def checkIfKingInCheck(grid, color, coords = ()):
    kingCoords = ()
    if coords == ():
        for row in grid:
            for cell in row:
                if cell != None and cell.typeOfPiece == "King" and cell.color == color:
                    kingCoords = (cell.coord[0], cell.coord[1])
    else:
        kingCoords = coords

    for row in grid:
        for cell in row:
            if cell != None and cell.color != color:
                movePossibilities = determineMoves(grid, cell, True)
                #if cell.typeOfPiece == "Queen":
                    #print(movePossibilities)

                for move in movePossibilities:
                    if move == (kingCoords[0], kingCoords[1]):
                        return True
    return False

def doesMoveSolveCheck(grid, piece, move):
    boardCopy = [[None for i in range(8)] for j in range(8)]
    for y in range(len(boardCopy)):
        for x in range(len(boardCopy[0])):
            if grid[y][x] != None:
                boardCopy[y][x] = Piece(grid[y][x].typeOfPiece, grid[y][x].color, (y, x), grid[y][x].img)
    gridCopy = Grid(boardCopy)
    
    gridCopy.deleteCellContents(move[0], move[1])
    gridCopy.grid[move[0]][move[1]] = gridCopy.grid[piece.coord[0]][piece.coord[1]]
    gridCopy.deleteCellContents(piece.coord[0], piece.coord[1])
    gridCopy.grid[move[0]][move[1]].changeCoordinates(move[0], move[1])
    
    if checkIfKingInCheck(gridCopy.grid, piece.color):
        #gridCopy.printBoard()
        gridCopy = None
        return False
    gridCopy = None
    return True
    

def returnLetterForPiece(x):
    if x == None:
        return " "
    elif x.typeOfPiece == "Knight":
        return "N"

    return x.typeOfPiece[0]

#MOVEMENT FUNCTIONS ##################################################################
######################################################################################


#PIECE VARIABLES: MOVES TAKEN, CAN CASTLE?, COORDS, TYPE OF PIECE, COLOR (0 or 1)


#Find the moves possible for any given piece.

def determineMoves(grid, piece, checkOverride = False):

    #list of all moves found for the piece (including king captures)
    possibleMovesFound = []

    #Shadow moves are possible moves stored if a piece moves foward, like a king into a pawn's diagonals
    shadowMovesFound = []

    #Self-explanatory.
    if piece.typeOfPiece == "Rook":

        #CHANGING Y VALUES
        #Get -1 and 1
        for i in range(-1, 2, 2):
            #get numbers from 1 to 8
            for j in range(1, 9):
                #If its not out of the board,
                if not outOfBoard(piece.coord[0] + i*j, piece.coord[1]):
                    #If its a blank space,
                    if grid[piece.coord[0] + i*j][piece.coord[1]] == None:
                        #append the move to the list
                        possibleMovesFound.append((piece.coord[0] + i*j, piece.coord[1]))
                    #Otheriwse,
                    else:
                        # If the space has a piece and its not the same color as the piece being moved,
                        if canCapture(grid[piece.coord[0] + i*j][piece.coord[1]], grid[piece.coord[0]][piece.coord[1]]):
                            #Append that move
                            possibleMovesFound.append((piece.coord[0] + i*j, piece.coord[1]))
                            break
                        else:
                            break
        for i in range(-1, 2, 2):
            for j in range(1, 9):
                if not outOfBoard(piece.coord[0], piece.coord[1] + i*j):
                    if grid[piece.coord[0]][piece.coord[1] + i*j] == None:
                        possibleMovesFound.append((piece.coord[0], piece.coord[1] + i*j))
                    else:
                        if canCapture(grid[piece.coord[0]][piece.coord[1] + i*j], grid[piece.coord[0]][piece.coord[1]]):
                            possibleMovesFound.append((piece.coord[0], piece.coord[1] + i*j))
                            break
                        else:
                            break
    
    #Bishop Moves ----------------------------------------

    elif piece.typeOfPiece == "Bishop":

        for i in range(-1, 2, 2):
            for j in range(1, 9):
                if not outOfBoard(piece.coord[0] + i*j, piece.coord[1] + j):
                    if grid[piece.coord[0] + i*j][piece.coord[1] + j] == None:
                        possibleMovesFound.append((piece.coord[0] + i*j, piece.coord[1] + j))
                    else:
                        if canCapture(grid[piece.coord[0] + i*j][piece.coord[1] + j], grid[piece.coord[0]][piece.coord[1]]):
                            possibleMovesFound.append((piece.coord[0] + i*j, piece.coord[1] + j))
                            break
                        else:
                            break
        for i in range(-1, 2, 2):
            for j in range(1, 9):
                if not outOfBoard(piece.coord[0] + i*j, piece.coord[1] - j):
                    if grid[piece.coord[0] + i*j][piece.coord[1] - j] == None:
                        possibleMovesFound.append((piece.coord[0] + i*j, piece.coord[1] - j))
                    else:
                        if canCapture(grid[piece.coord[0] + i*j][piece.coord[1] - j], grid[piece.coord[0]][piece.coord[1]]):
                            possibleMovesFound.append((piece.coord[0] + i*j, piece.coord[1] - j))
                            break
                        else:
                            break

    #Knight moves --------------------------------------------------------

    elif piece.typeOfPiece == "Knight":

        for j in range (-1, 2, 2):
            for i in range(-1, 2, 2):
                if not outOfBoard(piece.coord[0] + j*2, piece.coord[1] - i):
                    if grid[piece.coord[0] + j*2][piece.coord[1] - i] == None:
                        possibleMovesFound.append((piece.coord[0] + j*2, piece.coord[1] - i))
                    else:
                        if canCapture(grid[piece.coord[0] + j*2][piece.coord[1] - i], grid[piece.coord[0]][piece.coord[1]]):
                            possibleMovesFound.append((piece.coord[0] + j*2, piece.coord[1] - i))
        for j in range (-1, 2, 2):
            for i in range(-1, 2, 2):
                if not outOfBoard(piece.coord[0] + i, piece.coord[1] + j*2):
                    if grid[piece.coord[0] + i][piece.coord[1] + j*2] == None:
                        possibleMovesFound.append((piece.coord[0] + i, piece.coord[1] + j*2))
                    else:
                        if canCapture(grid[piece.coord[0] + i][piece.coord[1] + j*2], grid[piece.coord[0]][piece.coord[1]]):
                            possibleMovesFound.append((piece.coord[0] + i, piece.coord[1] + j*2))


    #Queen moves -----------------------------------------
    elif piece.typeOfPiece == "Queen":
        
        for i in range(-1, 2, 2):
            for j in range(1, 9):
                if not outOfBoard(piece.coord[0] + i*j, piece.coord[1] + j):
                    if grid[piece.coord[0] + i*j][piece.coord[1] + j] == None:
                        possibleMovesFound.append((piece.coord[0] + i*j, piece.coord[1] + j))
                    else:
                        if canCapture(grid[piece.coord[0] + i*j][piece.coord[1] + j], grid[piece.coord[0]][piece.coord[1]]):
                            possibleMovesFound.append((piece.coord[0] + i*j, piece.coord[1] + j))
                            break
                        else:
                            break
        for i in range(-1, 2, 2):
            for j in range(1, 9):
                if not outOfBoard(piece.coord[0] + i*j, piece.coord[1] - j):
                    if grid[piece.coord[0] + i*j][piece.coord[1] - j] == None:
                        possibleMovesFound.append((piece.coord[0] + i*j, piece.coord[1] - j))
                    else:
                        if canCapture(grid[piece.coord[0] + i*j][piece.coord[1] - j], grid[piece.coord[0]][piece.coord[1]]):
                            possibleMovesFound.append((piece.coord[0] + i*j, piece.coord[1] - j))
                            break
                        else:
                            break
    
        #Rook Part
        for i in range(-1, 2, 2):
            for j in range(1, 9):
                if not outOfBoard(piece.coord[0] + i*j, piece.coord[1]):
                    if grid[piece.coord[0] + i*j][piece.coord[1]] == None:
                        possibleMovesFound.append((piece.coord[0] + i*j, piece.coord[1]))
                    else:
                        if canCapture(grid[piece.coord[0] + i*j][piece.coord[1]], grid[piece.coord[0]][piece.coord[1]]):
                            possibleMovesFound.append((piece.coord[0] + i*j, piece.coord[1]))
                            break
                        else:
                            break
        for i in range(-1, 2, 2):
            for j in range(1, 9):
                if not outOfBoard(piece.coord[0], piece.coord[1] + i*j):
                    if grid[piece.coord[0]][piece.coord[1] + i*j] == None:
                        possibleMovesFound.append((piece.coord[0], piece.coord[1] + i*j))
                    else:
                        if canCapture(grid[piece.coord[0]][piece.coord[1] + i*j], grid[piece.coord[0]][piece.coord[1]]):
                            possibleMovesFound.append((piece.coord[0], piece.coord[1] + i*j))
                            break
                        else:
                            break

    # Pawn moves --------------------------------------

    elif piece.typeOfPiece == "Pawn":

        if piece.movesTaken == 0:
            if not outOfBoard(piece.coord[0] + (((piece.color * 2) - 1) * 2), piece.coord[1]):
                if grid[piece.coord[0] + (((piece.color * 2) - 1) * 2)][piece.coord[1]] == None and grid[piece.coord[0] + ((piece.color * 2) - 1)][piece.coord[1]] == None:
                    possibleMovesFound.append((piece.coord[0] + (((piece.color * 2) - 1) * 2), piece.coord[1]))

        if not outOfBoard(piece.coord[0] + ((piece.color * 2) - 1), piece.coord[1]):
                if grid[piece.coord[0] + ((piece.color * 2) - 1)][piece.coord[1]] == None:
                    possibleMovesFound.append((piece.coord[0] + ((piece.color * 2) - 1), piece.coord[1]))

        for i in range(-1, 2, 2):
            if not outOfBoard(piece.coord[0] + ((piece.color * 2) - 1), piece.coord[1] + i):
                if grid[piece.coord[0] + ((piece.color * 2) - 1)][piece.coord[1] + i] != None and canCapture(grid[piece.coord[0] + ((piece.color * 2) - 1)][piece.coord[1] + i], grid[piece.coord[0]][piece.coord[1]]):
                    possibleMovesFound.append((piece.coord[0] + ((piece.color * 2) - 1), piece.coord[1] + i))
        
        if piece.color + 3 == piece.coord[0]:
            for i in range(-1, 2, 2):
                if not outOfBoard(piece.coord[0], piece.coord[1] + i):
                    if not grid[piece.coord[0]][piece.coord[1] + i] == None and grid[piece.coord[0]][piece.coord[1] + i].color != piece.color and grid[piece.coord[0]][piece.coord[1] + i].movesTaken == 1:
                        if grid[piece.coord[0] + ((piece.color * 2) - 1)][piece.coord[1] + i] == None and previousPieceMoved[1] == (piece.coord[0], piece.coord[1] + i):
                            possibleMovesFound.append((piece.coord[0] + ((piece.color * 2) - 1), piece.coord[1] + i))

    #King moves -------------------------------------------------

    elif piece.typeOfPiece == "King":
  
        if piece.canCastle:
            if grid[piece.coord[0]][7] != None:
                if grid[piece.coord[0]][7].typeOfPiece == "Rook" and grid[piece.coord[0]][7].color == piece.color:
                    if grid[piece.coord[0]][7].movesTaken == 0 and grid[piece.coord[0]][6] == grid[piece.coord[0]][5] == None:
                        possibleMovesFound.append((piece.coord[0], 6))
            if grid[piece.coord[0]][0] != None:
                if grid[piece.coord[0]][0].typeOfPiece == "Rook" and grid[piece.coord[0]][0].color == piece.color:
                    if grid[piece.coord[0]][0].movesTaken == 0 and grid[piece.coord[0]][1] == grid[piece.coord[0]][2] == grid[piece.coord[0]][3] == None:
                        possibleMovesFound.append((piece.coord[0], 2))
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == j == 0:
                    continue
                if not outOfBoard(piece.coord[0] + i, piece.coord[1] + j):
                    if grid[piece.coord[0] + i][piece.coord[1] + j] == None:
                        possibleMovesFound.append((piece.coord[0] + i, piece.coord[1] + j))
                    if grid[piece.coord[0] + i][piece.coord[1] + j] != None and canCapture(grid[piece.coord[0] + i][piece.coord[1] + j], grid[piece.coord[0]][piece.coord[1]]):
                        possibleMovesFound.append((piece.coord[0] + i, piece.coord[1] + j))

    #If in check, where can you move
    if not checkOverride:
        isCheckmate = False
        
        #if checkIfKingInCheck(grid, piece.color):
            #tempPossMoves = []
            #for move in possibleMovesFound:
                #if doesMoveSolveCheck(grid, piece, move):
                    #tempPossMoves.append(move)
            #possibleMovesFound = tempPossMoves.copy()

        #COPIIIIIEEEDDDD
        tempPossMoves3 = []
        for move in possibleMovesFound:
            if doesMoveSolveCheck(grid, piece, move):
                tempPossMoves3.append(move)
        possibleMovesFound = tempPossMoves3.copy()


        #remove kings
        tempPossMoves2 = []
        for move in possibleMovesFound:
            try:
                if grid[move[0]][move[1]] == None or not grid[move[0]][move[1]].typeOfPiece == "King":
                    tempPossMoves2.append(move)
            except:
                print(move)

        possibleMovesFound = tempPossMoves2

        """
        tempPossMoves3 = []
        for move in possibleMovesFound:
            if doesMoveSolveCheck(grid, piece, move):
                tempPossMoves3.append(move)
        possibleMovesFound = tempPossMoves3"""


    return possibleMovesFound

