#     ______                   
#    / ____/___ _____ ___  ___ 
#   / / __/ __ `/ __ `__ \/ _ \
#  / /_/ / /_/ / / / / / /  __/
#  \____/\__,_/_/ /_/ /_/\___/ 


import pygame, board, ai, math, os, time, openai
from dotenv import load_dotenv
from pathlib import Path
import re


#INIT ################################################################################################################
######################################################################################################################

displaySize = 640

#Init Pygame
pygame.init()
pygame.font.init()

myfont = pygame.font.SysFont('Arial', 64)

win = pygame.display.set_mode((displaySize, displaySize))
pygame.display.set_caption("Chess")

env_path = Path.cwd() / '.env.env'
load_dotenv(dotenv_path=env_path)

openai.api_key = os.getenv('OPENAI_KEY')

chat_log ='''You are a chess grandmaster playing black against a human opponent. Respond with chess notation. Respond with a single black move, beginning with (Black).
You must only play legal moves, see the board for current board state. The game starts here: '''

regex = re.compile(r"[A-Za-z][0-9]")

#INIT 2
playGrid = board.Grid()

playGrid.initializeStandardBoard()
# -----------------------------------------------------------
isPieceHeld = False
pieceHeld = None
isHighlighted = False
highlightedCells = []

global globalCellClicked

turn = 0

isCheckmate = False
whoWon = ""


def determineHighlightedCells():
    global isHighlighted
    for y in range(8):
        for x in range(8):
            if (y, x) in board.determineMoves(playGrid.grid, playGrid.grid[pieceHeld.coord[0]][pieceHeld.coord[1]]):
                highlightedCells.append((y, x))
    isHighlighted = True

#Draw
def draw():
    pygame.draw.rect(win, (212, 173, 57), (0, 0, displaySize, displaySize))

    modNum = 1                          
    for i in range(8):
        for j in range(8):
            if j % 2 == modNum:
                pygame.draw.rect(win, (210,105,30), ((75 * j) + 20, (75 * i) + 20, 75, 75))
        modNum = abs(modNum - 1)

    if isPieceHeld:
        if not isHighlighted:
            determineHighlightedCells()
        for cell in highlightedCells:
            if cell[1] % 2 == abs((cell[0] % 2) - 1):
                pygame.draw.rect(win, (210 - 30, 105 - 30, 30 - 30), (cell[1] * 75 + 20, cell[0] * 75 + 20, 75, 75))
                pygame.draw.rect(win, (212, 255, 57), (cell[1] * 75 + 21, cell[0] * 75 + 21, 75, 75), 5)
            else:
                pygame.draw.rect(win, (212 - 30, 173 - 30, 57 - 30), (cell[1] * 75 + 20, cell[0] * 75 + 20, 75, 75))
                pygame.draw.rect(win, (212, 255, 57), (cell[1] * 75 + 21, cell[0] * 75 + 21, 75, 75), 5)

        
    for i in range(9):
        pygame.draw.line(win, (0, 0, 0), ((i*75) + 20, 20),
                         ((i*75) + 20, displaySize - 20), 2)
    for i in range(9):
        pygame.draw.line(win, (0, 0, 0), (20, (i*75) + 20),
                         (displaySize - 20, (i*75) + 20), 2)

    for row in playGrid.grid:
        for cell in row:
            if cell != None:
                if cell != pieceHeld:
                    win.blit(pygame.image.load(cell.img), (cell.coord[1] * 75 + 27.5, cell.coord[0] * 75 + 27.5))
                else:
                    win.blit(pygame.image.load(cell.img), (pygame.mouse.get_pos()[0] - 10,
                             pygame.mouse.get_pos()[1] - 10))

    pygame.display.update()


def hasBeenCheckmate(grid, color):
    allPiecesPossible = []
    for row in grid:
        for cell in row:
            if cell != None and cell.color == color and len(board.determineMoves(grid, cell)) > 0:
                allPiecesPossible.append(cell)

    if len(allPiecesPossible) == 0:
        if board.checkIfKingInCheck(grid, color):
            return "Checkmate"
        else:
            return "Draw"

#PlacePiece
def placePiece():
    global isPieceHeld, pieceHeld, isHighlighted, highlightedCells, turn, isCheckmate, numPieces, chat_log
    mouse_pos = pygame.mouse.get_pos()
    cell_over = [0, 0]
    if mouse_pos[0] <= displaySize - 20 and mouse_pos[0] >= 20:
        if mouse_pos[1] <= displaySize - 20 and mouse_pos[1] >= 20:
            cell_over[0] = math.floor((mouse_pos[0] - 20) / 75)
            cell_over[1] = math.floor((mouse_pos[1] - 20) / 75)
            if (cell_over[1], cell_over[0]) in board.determineMoves(playGrid.grid, playGrid.grid[pieceHeld.coord[0]][pieceHeld.coord[1]]):
                playGrid.movePiece(pieceHeld.coord[0], pieceHeld.coord[1], cell_over[1], cell_over[0])
                # Print standard notation
                if (playGrid.grid[pieceHeld.coord[0]][pieceHeld.coord[1]].typeOfPiece != "Knight"):
                    bodgedString = playGrid.grid[pieceHeld.coord[0]][pieceHeld.coord[1]].typeOfPiece[0].lower() + chr(globalCellClicked[0] + 97) + str(8 - globalCellClicked[1])
                    bodgedString += "-" + playGrid.grid[pieceHeld.coord[0]][pieceHeld.coord[1]].typeOfPiece[0].lower() + chr(pieceHeld.coord[1] + 97) + str(8 - pieceHeld.coord[0])
                else:
                    bodgedString = "kn" + chr(globalCellClicked[0] + 97) + str(8 - globalCellClicked[1])
                    bodgedString += "-" + "kn" + chr(pieceHeld.coord[1] + 97) + str(8 - pieceHeld.coord[0])
                chat_log += bodgedString + ","
                messageStart = [{"role": "user", "content":chat_log}]
                response = openai.ChatCompletion.create(
                model="gpt-4",
                max_tokens=20,
                temperature=1.2,
                messages = messageStart)
                textResponse = dict(response.choices[0])["message"]["content"]
                print(bodgedString)
                print(textResponse)
                gptMove = re.findall(regex, textResponse)
                chat_log += "(White): " + textResponse + "\nCurrent Board: " + playGrid.printBoard() + "\n"
                try:
                    print(str(ord(gptMove[0][0]) - 97) + " " + str(8 - int(gptMove[0][1])))
                    
                    #RANDOM AI MOVE (BREAKS IF DEPTH IS 0)
                    '''aiMove = ai.minMaxGame(playGrid.grid, abs(turn - 1), 3)'''
                    #aiMove = ai.findRandomMovePlusValues(playGrid.grid, abs(turn - 1), 3)
                    if hasBeenCheckmate(playGrid.grid, not turn) == "Checkmate":
                        isCheckmate = True
                        return "Checkmate"
                    elif hasBeenCheckmate(playGrid.grid, not turn) == "Draw":
                        isCheckmate = True
                        return "Draw"
                    #print(aiMove)
                    #playGrid.movePiece(aiMove[0].coord[0], aiMove[0].coord[1], aiMove[1][0], aiMove[1][1], True)
                    playGrid.movePiece(8 - int(gptMove[0][1]), ord(gptMove[0][0]) - 97, 8 - int(gptMove[1][1]), ord(gptMove[1][0]) - 97, True)
                except:
                    pygame.draw.rect(win, (212 + 20, 173 + 20, 57 + 20), (2 * 75 + 20, 3 * 75 + 20, 75*4, 75*2))
                    pygame.draw.rect(win, (0, 0, 0), (2 * 75 + 20, 3 * 75 + 20, 75*4, 75*2), 5)
                    textSurface = myfont.render('Aneurism!', False, (0, 0, 0))
                    win.blit(textSurface, (2 * 75 + 31, 3 * 75 + 55))
                    pygame.display.update()
                    time.sleep(2)
                if hasBeenCheckmate(playGrid.grid, turn) == "Checkmate":
                    isCheckmate = True
                    return "Checkmate"
                if hasBeenCheckmate(playGrid.grid, turn) == "Draw":
                    isCheckmate = True
                    return "Draw"
    isHighlighted = False
    highlightedCells = []
    isPieceHeld = False
    pieceHeld = None
    

#CheckForImageMove
def checkForImageMove():
    global pieceHeld, isPieceHeld, globalCellClicked
    mouse_pos = pygame.mouse.get_pos()
    cell_clicked = [0, 0]
    if mouse_pos[0] <= displaySize - 20 and mouse_pos[0] >= 20:
        if mouse_pos[1] <= displaySize - 20 and mouse_pos[1] >= 20:
            cell_clicked[0] = math.floor((mouse_pos[0] - 20) / 75)
            cell_clicked[1] = math.floor((mouse_pos[1] - 20) / 75)
            if playGrid.grid[cell_clicked[1]][cell_clicked[0]] != None and playGrid.grid[cell_clicked[1]][cell_clicked[0]].color == turn:
                pieceHeld = playGrid.grid[cell_clicked[1]][cell_clicked[0]]
                isPieceHeld = True
    globalCellClicked = cell_clicked

# MAIN LOOP ##################################################################################################
run = True

while run:
    draw()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            pygame.quit()
            break
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if not isPieceHeld:
                checkForImageMove()
        elif event.type == pygame.MOUSEBUTTONUP:
            if isPieceHeld:
                placedPieceAction = placePiece()
                #placedPieceAction = "Draw"
                #placedPieceAction = "Checkmate"
                if placedPieceAction == "Checkmate":
                    isHighlighted = False
                    highlightedCells = []
                    isPieceHeld = False
                    pieceHeld = None
                    draw()
                    print("Checkmate!")
                    pygame.draw.rect(win, (212 + 20, 173 + 20, 57 + 20), (2 * 75 + 20, 3 * 75 + 20, 75*4, 75*2))
                    pygame.draw.rect(win, (0, 0, 0), (2 * 75 + 20, 3 * 75 + 20, 75*4, 75*2), 5)
                    textSurface = myfont.render('Checkmate!', False, (0, 0, 0))
                    win.blit(textSurface, (2 * 75 + 31, 3 * 75 + 55))
                    pygame.display.update()
                    time.sleep(5)
                    run = False
                    break
                if placedPieceAction == "Draw":
                    isHighlighted = False
                    highlightedCells = []
                    isPieceHeld = False
                    pieceHeld = None
                    draw()
                    print("Draw!")
                    pygame.draw.rect(win, (212 + 20, 173 + 20, 57 + 20), (2 * 75 + 20, 3 * 75 + 20, 75*4, 75*2))
                    pygame.draw.rect(win, (0, 0, 0), (2 * 75 + 20, 3 * 75 + 20, 75*4, 75*2), 5)
                    textSurface = myfont.render('Draw!', False, (0, 0, 0))
                    win.blit(textSurface, (2 * 75 + 105, 3 * 75 + 55))
                    pygame.display.update()
                    time.sleep(5)
                    run = False
                    break
                if placedPieceAction == "Resign":
                    isHighlighted = False
                    highlightedCells = []
                    isPieceHeld = False
                    pieceHeld = None
                    draw()
                    print("The AI resigned!")
                    pygame.draw.rect(win, (212 + 20, 173 + 20, 57 + 20), (2 * 75 + 20, 3 * 75 + 20, 75*4, 75*2))
                    pygame.draw.rect(win, (0, 0, 0), (2 * 75 + 20, 3 * 75 + 20, 75*4, 75*2), 5)
                    textSurface = myfont.render('Win!!', False, (0, 0, 0))
                    win.blit(textSurface, (2 * 75 + 105, 3 * 75 + 55))
                    pygame.display.update()
                    time.sleep(5)
                    run = False
                    break

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_v:
                print(ai.findCurrentValue(playGrid.grid))
                

pygame.quit()
