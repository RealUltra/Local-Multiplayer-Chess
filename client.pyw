import os

try:
    import pygame
except:
    os.system("pip install pygame")
    import pygame

try:
    import pyperclip
except:
    os.system("pip install pyperclip")
    import pyperclip

import sys
import ctypes
import threading
import network

class Piece():
    def __init__(self, piece, pos):
        self.piece = piece
        self.pos = pos

class Chess():
    def __init__(self):
        pygame.init()

        self.client = network.Client(self.handle_message, "192.168.100.14", 5555, 4096) # In the blank string, Put In The IP Address Shown By The Server

        self.HEIGHT = 650
        self.WIDTH = 500

        self.window = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Chess")
        self.run = True
        self.mode = "MainMenu"

        self.ALL_PIECES = {"W.K":pygame.image.load("Pieces\\whiteKing.png"),
                           "B.K":pygame.image.load("Pieces\\blackKing.png"),
                           "W.P":pygame.image.load("Pieces\\whitePawn.png"),
                           "B.P":pygame.image.load("Pieces\\blackPawn.png"),
                           "W.R":pygame.image.load("Pieces\\whiteRook.png"),
                           "B.R":pygame.image.load("Pieces\\blackRook.png"),
                           "W.H":pygame.image.load("Pieces\\whiteKnight.png"),
                           "B.H":pygame.image.load("Pieces\\blackKnight.png"),
                           "W.B":pygame.image.load("Pieces\\whiteBishop.png"),
                           "B.B":pygame.image.load("Pieces\\blackBishop.png"),
                           "W.Q":pygame.image.load("Pieces\\whiteQueen.png"),
                           "B.Q":pygame.image.load("Pieces\\blackQueen.png")}

        self.teams = {0:"White", 1:"Black"}
        self.clock = pygame.time.Clock()
        self.FPS = 60

        self.mainloop()

    def reset_game(self):
        self.onboard_pieces = [Piece("W.P", "A2"), Piece("W.P", "B2"), Piece("W.P", "C2"), Piece("W.P", "D2"), Piece("W.P", "E2"), Piece("W.P", "F2"), Piece("W.P", "G2"), Piece("W.P", "H2"),
                       Piece("B.P", "A7"), Piece("B.P", "B7"), Piece("B.P", "C7"), Piece("B.P", "D7"), Piece("B.P", "E7"), Piece("B.P", "F7"), Piece("B.P", "G7"), Piece("B.P", "H7"),
                       Piece("W.R", "A1"), Piece("W.R", "H1"), Piece("B.R", "A8"), Piece("B.R", "H8"), Piece("W.H", "B1"), Piece("W.H", "G1"), Piece("B.H", "B8"), Piece("B.H", "G8"),
                       Piece("W.B", "C1"), Piece("W.B", "F1"), Piece("B.B", "C8"), Piece("B.B", "F8"), Piece("W.Q", "D1"), Piece("W.K", "E1"), Piece("B.Q", "D8"), Piece("B.K", "E8")]

        self.beaten_pieces = []
        self.boardPos = {}
        self.selected_piece_pos = None
        self.opponent_just_moved = False
        self.opponent_just_moved_iter = 0

        if self.team == 0:
            self.opponent_move = True

        elif self.team == 1:
            self.opponent_move = None

    def handle_message(self, message):
        if message.startswith("[MOVE]"):
            old, new = message.replace("[MOVE]", "").split("|")
            self.opponent_move = [old.strip(), new.strip()]
            self.move(old.strip(), new.strip())
            self.opponent_just_moved = [old.strip(), new.strip()]
            self.opponent_just_moved_iter = 0

        if message.strip() == "[JOIN WITH CODE FAILED]":
            ctypes.windll.user32.MessageBoxW(0, "Invalid Code", "Failed To Join", 48)

        if message.strip() == "[JOIN WILL CODE FULL]":
            ctypes.windll.user32.MessageBoxW(0, "Game Full!", "Failed To Join", 48)

        if message.startswith("[WAITING]"):
            self.mode = "Wait|" + message.replace("[WAITING]", "").strip()

        if message.startswith("[STARTED]"):
            ctypes.windll.user32.MessageBoxW(0, "Game Started!", "Get Ready", 48)
            self.team = int(message.replace("[STARTED]", "").strip())
            self.reset_game()
            self.mode = "Game"

        if message.strip() == "[OPPONENT LEFT]":
            ctypes.windll.user32.MessageBoxW(0, "Your Opponent Just Left! You Win By Default!", "Failed To Join", 48)
            self.mode = "MainMenu"

    def waitingScreen(self, code):
        self.window.fill((0, 0, 0))

        font = pygame.font.Font('fonts\\cpgb.ttf', 60)
        self.window.blit(font.render("Waiting For", True, (255, 215, 0), (0, 0, 0)), (50, 0, 500, 100))
        self.window.blit(font.render("A Player", True, (255, 215, 0), (0, 0, 0)), (95, 70, 500, 100))
        self.window.blit(font.render("To Join", True, (255, 215, 0), (0, 0, 0)), (140, 140, 500, 100))

        font = pygame.font.Font('fonts\\cpgb.ttf', 40)
        pygame.draw.rect(self.window, (255,255,153), (0, 300, 500, 100))
        self.window.blit(font.render(code, True, (255, 0, 0), (255,255,153)), (0, 325, 500, 100))

        font = pygame.font.Font('fonts\\cpgb.ttf', 70)
        pygame.draw.rect(self.window, (34, 32, 33), (0, 500, 500, 100))
        self.window.blit(font.render("Exit", True, (255, 0, 0), (34, 32, 33)), (170, 510, 500, 100))

    def MainMenu(self):
        self.window.fill((0, 0, 0))

        font = pygame.font.Font('fonts\\cpgb.ttf', 60)
        self.window.blit(font.render("Chess", True, (255, 215, 0), (0, 0, 0)), (150, 0, 500, 100))

        font = pygame.font.Font('fonts\\cpgb.ttf', 45)
        pygame.draw.rect(self.window, (34, 32, 33), (0, 200, 500, 100))
        self.window.blit(font.render("Join Random Game", True, (255, 0, 0), (34, 32, 33)), (15, 225, 500, 100))

        font = pygame.font.Font('fonts\\cpgb.ttf', 40)
        pygame.draw.rect(self.window, (34, 32, 33), (0, 350, 500, 100))
        self.window.blit(font.render("Join Game With Code", True, (255, 0, 0), (34, 32, 33)), (15, 375, 500, 100))

    def joinRandomGame(self):
        self.client.send("[JOIN RANDOM]")

    def joinGameWithCode(self):
        self.window.fill((0, 0, 0))
        font = pygame.font.Font('fonts\\cpgb.ttf', 60)
        self.window.blit(font.render("Join", True, (255, 215, 0), (0, 0, 0)), (50, 0, 500, 100))
        self.window.blit(font.render("A Game", True, (255, 215, 0), (0, 0, 0)), (95, 70, 500, 100))
        self.window.blit(font.render("With Code", True, (255, 215, 0), (0, 0, 0)), (140, 140, 500, 100))

        font = pygame.font.Font('fonts\\helvetica.ttf', 33)
        pygame.draw.rect(self.window, (152,251,152), (0, 300, 500, 100))
        self.window.blit(font.render("Join With Code In Your Clipboard", True, (255, 0, 0), (152,251,152)), (5, 335, 500, 100))

        font = pygame.font.Font('fonts\\cpgb.ttf', 70)
        pygame.draw.rect(self.window, (34, 32, 33), (0, 500, 500, 100))
        self.window.blit(font.render("Exit", True, (255, 0, 0), (34, 32, 33)), (170, 510, 500, 100))

    def mainloop(self):
        while self.run:
            self.clock.tick(self.FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False
                    break

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    m_x, m_y = pygame.mouse.get_pos()
                    self.upon_mouse_click(m_x, m_y)

            if not self.run:
                break

            self.window.fill((255,255,255))

            if self.mode == "Game":
                if self.opponent_move == None:
                    if self.team == 0:
                        self.window.fill((0,0,0))
                    else:
                        self.window.fill((255, 255, 255))

                else:
                    if self.team == 0:
                        self.window.fill((255, 255, 255))
                    else:
                        self.window.fill((0,0,0))

                self.createBoard(self.team)

                if self.selected_piece_pos != None:
                    for coords in self.get_available_spots(self.selected_piece_pos):
                        pygame.draw.rect(self.window, (0, 255, 0), (self.boardPos[coords] + (50, 50)))
                        pygame.draw.rect(self.window, (0, 0, 0), (self.boardPos[coords] + (50, 50)), 5)

                self.placePieces()
                self.checkEvents()

                print(self.check(self.team))

                if self.opponent_just_moved != False:
                    old, new = self.opponent_just_moved

                    pygame.draw.rect(self.window, (255, 0, 0), (self.boardPos[old] + (50, 50)), 5)
                    pygame.draw.rect(self.window, (255, 0, 0), (self.boardPos[new] + (50, 50)), 5)

                    self.opponent_just_moved_iter += 1

                    if self.opponent_just_moved_iter == 100:
                        self.opponent_just_moved = False
                        self.opponent_just_moved_iter = 0

                if self.selected_piece_pos != None:
                    pygame.draw.rect(self.window, (0, 0, 255), (self.boardPos[self.selected_piece_pos] + (50, 50)), 5)

            elif self.mode == "MainMenu":
                self.MainMenu()

            elif self.mode.startswith("Wait|"):
                self.waitingScreen(self.mode.split("|")[1].strip())

            elif self.mode == "JoinWithCode":
                self.joinGameWithCode()

            pygame.display.update()

        pygame.quit()
        self.client.send("[QUIT]")
        self.client.close()
        sys.exit()

    def checkEvents(self):
        a = [f.piece for f in self.onboard_pieces]
        b = ["W.K", "B.K"]

        a.sort()
        b.sort()

        if "W.K" not in [f.piece for f in self.onboard_pieces]:
            ctypes.windll.user32.MessageBoxW(0, "Black Won!", "Game Over", 48)
            self.client.send("[GAME OVER]")
            self.mode = "MainMenu"

        elif "B.K" not in [f.piece for f in self.onboard_pieces]:
            ctypes.windll.user32.MessageBoxW(0, "White Won!", "Game Over", 48)
            self.client.send("[GAME OVER]")
            self.mode = "MainMenu"

        elif a == b:
            ctypes.windll.user32.MessageBoxW(0, "It Is A Tie!", "Game Over", 48)
            self.client.send("[GAME OVER]")
            self.mode = "MainMenu"

        if "W.P" in [f.piece if f.pos[1] == "8" else "" for f in self.onboard_pieces]:
            self.onboard_pieces[[f.piece if f.pos[1] == "8" else "" for f in self.onboard_pieces].index("W.P")].piece = "W.Q"

        if "B.P" in [f.piece if f.pos[1] == "1" else "" for f in self.onboard_pieces]:
            self.onboard_pieces[[f.piece if f.pos[1] == "1" else "" for f in self.onboard_pieces].index("B.P")].piece = "B.Q"

    def upon_mouse_click(self, m_x, m_y):
        if self.mode == "Game":
            a = [coord if m_x > pos_x and m_y > pos_y and m_y < pos_y + 50 and m_x < pos_x + 50 else None for coord, (pos_x, pos_y) in self.boardPos.items()]

            while 1:
                if None in a:
                    a.remove(None)
                else:
                    break

            try:
                self.posPressed(a[len(a) - 1])
            except:
                pass

        elif self.mode == "MainMenu":
            if m_y > 350 and m_y < 450:
                self.mode = "JoinWithCode"
            elif m_y > 200 and m_y < 300:
                self.joinRandomGame()

        elif self.mode.startswith("Wait|"):
            if m_y > 500 and m_y < 600:
                self.client.send("[LEAVING WAIT]")
                self.mode = "MainMenu"
            elif m_y > 300 and m_y < 400:
                pyperclip.copy(self.mode.split("|")[1].strip())
                ctypes.windll.user32.MessageBoxW(0, "The Join Code Has Been Copied To Your Clipboard!", "Code Copied", 48)

        elif self.mode == "JoinWithCode":
            if m_y > 500 and m_y < 600:
                self.mode = "MainMenu"

            elif m_y > 300 and m_y < 400:
                ctypes.windll.user32.MessageBoxW(0, "Now Joining With The Code In Your Clipboard...", "Joining With Code", 48)
                self.client.send("[JOIN] " + pyperclip.paste().strip())

    def move(self, initial_pos, final_pos):
        for piece in self.onboard_pieces:
            if piece.pos == final_pos:
                self.onboard_pieces.remove(piece)
                self.beaten_pieces.append(piece.piece)

            if piece.pos == initial_pos:
                piece.pos = final_pos

    def posPressed(self, pos):
        found = False
        for piece in self.onboard_pieces:
            if piece.pos == pos and piece.piece.startswith(self.teams[self.team][0].upper() + "."):
                found = True
                break

        if found:
            self.selected_piece_pos = pos

        else:
            if not self.valid_move(self.selected_piece_pos, pos):
                ctypes.windll.user32.MessageBoxW(0, "That Is Not A Valid Move!", "Invalid Move", 48)

            elif self.opponent_move == None:
                ctypes.windll.user32.MessageBoxW(0, "It Is Not Your Turn, Please Let The Other Player Move!", "Not Your Turn", 48)

            elif self.selected_piece_pos != None:
                self.move(self.selected_piece_pos, pos)
                self.client.send("[MOVE] " + self.selected_piece_pos + "|" + pos)
                self.opponent_move = None

            self.selected_piece_pos = None

    def placePieces(self):
        yourTeam = 0
        otherTeam = 0

        for piece in self.beaten_pieces:
            if piece.startswith(self.teams[self.team][0].upper() + "."):
                a, b = 50, 100
                self.window.blit(self.ALL_PIECES[piece], ((otherTeam * 50),  0))
                otherTeam += 1

            else:
                self.window.blit(self.ALL_PIECES[piece], ((yourTeam * 50),  550))
                yourTeam += 1

        for piece in self.onboard_pieces:
            self.window.blit(self.ALL_PIECES[piece.piece], self.boardPos[piece.pos])

    def createBoard(self, board):
        color = (62,66,75)

        pygame.draw.rect(self.window, (72, 73, 75), (0, 550,500, 50)) # Bottom Bar 2
        pygame.draw.rect(self.window, (34, 32, 33), (0, 50, 50, 450)) # Left Bar
        pygame.draw.rect(self.window, (72, 73, 75), (0, 0, 500, 50)) # Top Bar 2
        pygame.draw.rect(self.window, (34, 32, 33), (450, 50, 50, 500)) # Right Bar
        pygame.draw.rect(self.window, (34, 32, 33), (0, 50, 500, 50)) # Top Bar 1
        pygame.draw.rect(self.window, (34, 32, 33), (0, 500, 500, 50)) # Bottom Bar 1

        for height in range(8):

            if color == (255, 255, 255) and height != 0:
                color = (62,66,75)
            elif color == (62,66,75) and height != 0:
                color = (255, 255, 255)

            for width in range(8):
                pygame.draw.rect(self.window, color, (50*(width+1), 50*(height+2), 50, 50))

                if color == (255, 255, 255):
                    color = (62,66,75)
                elif color == (62,66,75):
                    color = (255, 255, 255)

                if board == 0:
                    self.boardPos[chr(width + ord("A")) + str(8 - height)] = (50*(width+1), 50*(height+2))
                elif board == 1:
                    self.boardPos[chr(ord("H") - width) + str(height + 1)] = (50*(width+1), 50*(height+2))

        font = pygame.font.Font('fonts\\helvetica.ttf', 20)

        if board == 0:
            for num in range(1, 9):
                corner = self.boardPos["A" + str(9 - num)]
                self.window.blit(font.render(str(9 - num), True, (255, 255, 255), (34,32,33)), (corner[0]-30, corner[1]+15))

            for letter in range(ord("A"), ord("H")+1):
                bottom = self.boardPos[chr(letter) + "1"]
                self.window.blit(font.render(chr(letter), True, (255, 255, 255), (34,32,33)), (bottom[0]+15, bottom[1]+65))

        elif board == 1:
            for num in range(1, 9):
                corner = self.boardPos["H" + str(9 - num)]
                self.window.blit(font.render(str(9 - num), True, (255, 255, 255), (34,32,33)), (corner[0]-30, corner[1]+15))

            for letter in range(ord("A"), ord("H")+1):
                bottom = self.boardPos[chr(ord("H") - letter + ord("A")) + "8"]
                self.window.blit(font.render(chr(ord("H") - letter + ord("A")), True, (255, 255, 255), (34,32,33)), (bottom[0]+15, bottom[1]+65))

    def valid_move(self, initial_pos, final_pos):
        return final_pos in self.get_available_spots(initial_pos)

    def check(self, team):
        starter = self.teams[{0:1, 1:0}[team]][0].upper() + "."
        kingPos = self.teams[team][0].upper() + ".K"

        return True in [True if f.piece.startswith(starter) and kingPos in self.get_available_spots(f.pos) else False for f in self.onboard_pieces]

    def get_available_spots(self, piece_pos):
        moveable_spots = []

        piece = "".join([f.piece if f.pos == piece_pos else "" for f in self.onboard_pieces])
        piece_type = piece.split('.')[1].upper()
        onboard_pieces_pos = [f.pos for f in self.onboard_pieces]
        team = {"W":0, "B":1}[piece.split('.')[0].upper()]

        if piece_type == "P":
            if team == 0: # If Team Is White
                if (piece_pos[0] + str(int(piece_pos[1]) + 1)) not in onboard_pieces_pos:
                    moveable_spots.append(piece_pos[0] + str(int(piece_pos[1]) + 1))

                if piece_pos[1] == "2" and (piece_pos[0] + str(int(piece_pos[1]) + 1)) not in onboard_pieces_pos and (piece_pos[0] + str(int(piece_pos[1]) + 2)) not in onboard_pieces_pos:
                    moveable_spots.append(piece_pos[0] + str(int(piece_pos[1]) + 2))

                if (chr(ord(piece_pos[0]) + 1) + str(int(piece_pos[1]) + 1)) in onboard_pieces_pos \
                        and not "".join([f.piece if f.pos == (chr(ord(piece_pos[0]) + 1) + str(int(piece_pos[1]) + 1))  else "" for f in self.onboard_pieces]).startswith(self.teams[team].upper()[0] + "."):
                    moveable_spots.append(chr(ord(piece_pos[0]) + 1) + str(int(piece_pos[1]) + 1))

                if (chr(ord(piece_pos[0]) - 1) + str(int(piece_pos[1]) + 1)) in onboard_pieces_pos \
                        and not "".join([f.piece if f.pos == (chr(ord(piece_pos[0]) - 1) + str(int(piece_pos[1]) + 1))  else "" for f in self.onboard_pieces]).startswith(self.teams[team].upper()[0] + "."):
                    moveable_spots.append(chr(ord(piece_pos[0]) - 1) + str(int(piece_pos[1]) + 1))

            else:
                if (piece_pos[0] + str(int(piece_pos[1]) - 1)) not in onboard_pieces_pos:
                    moveable_spots.append(piece_pos[0] + str(int(piece_pos[1]) - 1))

                if piece_pos[1] == "7" and (piece_pos[0] + str(int(piece_pos[1]) - 1)) not in onboard_pieces_pos and (piece_pos[0] + str(int(piece_pos[1]) - 2)) not in onboard_pieces_pos:
                    moveable_spots.append(piece_pos[0] + str(int(piece_pos[1]) - 2))

                if (chr(ord(piece_pos[0]) + 1) + str(int(piece_pos[1]) - 1)) in onboard_pieces_pos \
                        and not "".join([f.piece if f.pos == (chr(ord(piece_pos[0]) + 1) + str(int(piece_pos[1]) - 1))  else "" for f in self.onboard_pieces]).startswith(self.teams[team].upper()[0] + "."):
                    moveable_spots.append(chr(ord(piece_pos[0]) + 1) + str(int(piece_pos[1]) - 1))

                if (chr(ord(piece_pos[0]) - 1) + str(int(piece_pos[1]) - 1)) in onboard_pieces_pos \
                        and not "".join([f.piece if f.pos == (chr(ord(piece_pos[0]) - 1) + str(int(piece_pos[1]) - 1))  else "" for f in self.onboard_pieces]).startswith(self.teams[team].upper()[0] + "."):
                    moveable_spots.append(chr(ord(piece_pos[0]) - 1) + str(int(piece_pos[1]) - 1))

        if piece_type == "R" or piece_type == "Q":
            for num in range(int(piece_pos[1])+1, 9):
                pos = piece_pos[0] + str(num)

                if pos in onboard_pieces_pos:
                    if "".join([f.piece[0] if f.pos == pos else "" for f in self.onboard_pieces]) != self.teams[team][0].upper():
                        moveable_spots.append(pos)
                    break

                moveable_spots.append(pos)

            for num in range(1, int(piece_pos[1])):
                pos = piece_pos[0] + str(int(piece_pos[1]) - num)

                if pos in onboard_pieces_pos:
                    if "".join([f.piece[0] if f.pos == pos else "" for f in self.onboard_pieces]) != self.teams[team][0].upper():
                        moveable_spots.append(pos)
                    break

                moveable_spots.append(pos)

            for letter in range(ord("A") + 1, ord(piece_pos[0]) + 1):
                pos = chr(ord(piece_pos[0]) - (letter - ord("A"))) + str(piece_pos[1])

                if pos in onboard_pieces_pos:
                    if "".join([f.piece[0] if f.pos == pos else "" for f in self.onboard_pieces]) != self.teams[team][0].upper():
                        moveable_spots.append(pos)
                    break

                moveable_spots.append(pos)

            for letter in range(ord(piece_pos[0]) + 1, ord("H") + 1):
                pos = chr(letter) + str(piece_pos[1])

                if pos in onboard_pieces_pos:
                    if "".join([f.piece[0] if f.pos == pos else "" for f in self.onboard_pieces]) != self.teams[team][0].upper():
                        moveable_spots.append(pos)
                    break

                moveable_spots.append(pos)


        if piece_type == "H":
            if (chr(ord(piece_pos[0]) - 1) + str(int(piece_pos[1]) + 2) in self.boardPos) and ("".join([f.piece[0] if f.pos == (chr(ord(piece_pos[0]) - 1) + str(int(piece_pos[1]) + 2)) else "" for f in self.onboard_pieces]) == "" or "".join([f.piece[0] if f.pos == (chr(ord(piece_pos[0]) - 1) + str(int(piece_pos[1]) + 2)) else "" for f in self.onboard_pieces]) != self.teams[team][0].upper()):
                moveable_spots.append(chr(ord(piece_pos[0]) - 1) + str(int(piece_pos[1]) + 2))

            if (chr(ord(piece_pos[0]) + 1) + str(int(piece_pos[1]) + 2) in self.boardPos) and ("".join([f.piece[0] if f.pos == (chr(ord(piece_pos[0]) + 1) + str(int(piece_pos[1]) + 2)) else "" for f in self.onboard_pieces]) == "" or "".join([f.piece[0] if f.pos == (chr(ord(piece_pos[0]) + 1) + str(int(piece_pos[1]) + 2)) else "" for f in self.onboard_pieces]) != self.teams[team][0].upper()):
                moveable_spots.append(chr(ord(piece_pos[0]) + 1) + str(int(piece_pos[1]) + 2))

            if (chr(ord(piece_pos[0]) - 1) + str(int(piece_pos[1]) - 2) in self.boardPos) and ("".join([f.piece[0] if f.pos == (chr(ord(piece_pos[0]) - 1) + str(int(piece_pos[1]) - 2)) else "" for f in self.onboard_pieces]) == "" or "".join([f.piece[0] if f.pos == (chr(ord(piece_pos[0]) - 1) + str(int(piece_pos[1]) - 2)) else "" for f in self.onboard_pieces]) != self.teams[team][0].upper()):
                moveable_spots.append(chr(ord(piece_pos[0]) - 1) + str(int(piece_pos[1]) - 2))

            if (chr(ord(piece_pos[0]) + 2) + str(int(piece_pos[1]) + 1) in self.boardPos) and ("".join([f.piece[0] if f.pos == (chr(ord(piece_pos[0]) + 2) + str(int(piece_pos[1]) + 1)) else "" for f in self.onboard_pieces]) == "" or "".join([f.piece[0] if f.pos == (chr(ord(piece_pos[0]) + 2) + str(int(piece_pos[1]) + 1)) else "" for f in self.onboard_pieces]) != self.teams[team][0].upper()):
                moveable_spots.append(chr(ord(piece_pos[0]) + 2) + str(int(piece_pos[1]) + 1))

            if (chr(ord(piece_pos[0]) - 2) + str(int(piece_pos[1]) + 1) in self.boardPos) and ("".join([f.piece[0] if f.pos == (chr(ord(piece_pos[0]) - 2) + str(int(piece_pos[1]) + 1)) else "" for f in self.onboard_pieces]) == "" or "".join([f.piece[0] if f.pos == (chr(ord(piece_pos[0]) - 2) + str(int(piece_pos[1]) + 1)) else "" for f in self.onboard_pieces]) != self.teams[team][0].upper()):
                moveable_spots.append(chr(ord(piece_pos[0]) - 2) + str(int(piece_pos[1]) + 1))

            if (chr(ord(piece_pos[0]) + 1) + str(int(piece_pos[1]) - 2) in self.boardPos) and ("".join([f.piece[0] if f.pos == (chr(ord(piece_pos[0]) + 1) + str(int(piece_pos[1]) - 2)) else "" for f in self.onboard_pieces]) == "" or "".join([f.piece[0] if f.pos == (chr(ord(piece_pos[0]) + 1) + str(int(piece_pos[1]) - 2)) else "" for f in self.onboard_pieces]) != self.teams[team][0].upper()):
                moveable_spots.append(chr(ord(piece_pos[0]) + 1) + str(int(piece_pos[1]) - 2))

            if (chr(ord(piece_pos[0]) + 2) + str(int(piece_pos[1]) - 1) in self.boardPos) and ("".join([f.piece[0] if f.pos == (chr(ord(piece_pos[0]) + 2) + str(int(piece_pos[1]) - 1)) else "" for f in self.onboard_pieces]) == "" or "".join([f.piece[0] if f.pos == (chr(ord(piece_pos[0]) + 2) + str(int(piece_pos[1]) - 1)) else "" for f in self.onboard_pieces]) != self.teams[team][0].upper()):
                moveable_spots.append(chr(ord(piece_pos[0]) + 2) + str(int(piece_pos[1]) - 1))

            if (chr(ord(piece_pos[0]) - 2) + str(int(piece_pos[1]) - 1) in self.boardPos) and ("".join([f.piece[0] if f.pos == (chr(ord(piece_pos[0]) - 2) + str(int(piece_pos[1]) - 1)) else "" for f in self.onboard_pieces]) == "" or "".join([f.piece[0] if f.pos == (chr(ord(piece_pos[0]) - 2) + str(int(piece_pos[1]) - 1)) else "" for f in self.onboard_pieces]) != self.teams[team][0].upper()):
                moveable_spots.append(chr(ord(piece_pos[0]) - 2) + str(int(piece_pos[1]) - 1))

        if piece_type == "B" or piece_type == "Q":
            letter = piece_pos[0]
            num = int(piece_pos[1])

            while 1:  # Top-Right
                letter = chr(ord(letter) + 1)
                num += 1

                if ord(letter) > ord("H"):
                    break

                if num > 8:
                    break

                pos = letter + str(num)

                if pos in [f.pos for f in self.onboard_pieces]:
                    if "".join([f.piece[0] if f.pos == pos else '' for f in self.onboard_pieces]) != self.teams[team][0].upper():
                        moveable_spots.append(pos)
                    break

                moveable_spots.append(pos)

            letter = piece_pos[0]
            num = int(piece_pos[1])

            while 1:  # Top-Left
                letter = chr(ord(letter) - 1)
                num += 1

                if ord(letter) < ord("A"):
                    break

                if num > 8:
                    break

                pos = letter + str(num)

                if pos in [f.pos for f in self.onboard_pieces]:
                    if "".join([f.piece[0] if f.pos == pos else '' for f in self.onboard_pieces]) != self.teams[team][0].upper():
                        moveable_spots.append(pos)
                    break

                moveable_spots.append(pos)

            letter = piece_pos[0]
            num = int(piece_pos[1])

            while 1:  # Bottom-Left
                letter = chr(ord(letter) - 1)
                num -= 1

                if ord(letter) < ord("A"):
                    break

                if num < 1:
                    break

                pos = letter + str(num)

                if pos in [f.pos for f in self.onboard_pieces]:
                    if "".join([f.piece[0] if f.pos == pos else '' for f in self.onboard_pieces]) != self.teams[team][0].upper():
                        moveable_spots.append(pos)
                    break

                moveable_spots.append(pos)

            letter = piece_pos[0]
            num = int(piece_pos[1])

            while 1:  # Bottom-Right
                letter = chr(ord(letter) + 1)
                num -= 1

                if ord(letter) > ord("H"):
                    break

                if num < 1:
                    break

                pos = letter + str(num)

                if pos in [f.pos for f in self.onboard_pieces]:
                    if "".join([f.piece[0] if f.pos == pos else '' for f in self.onboard_pieces]) != self.teams[team][0].upper():
                        moveable_spots.append(pos)
                    break

                moveable_spots.append(pos)

        if piece_type == "K":
            if ((piece_pos[0] + str(int(piece_pos[1]) + 1)) in self.boardPos) and ("".join([f.piece[0] if f.pos == (piece_pos[0] + str(int(piece_pos[1]) + 1)) else "" for f in self.onboard_pieces]) == "" or "".join([f.piece[0] if f.pos == (piece_pos[0] + str(int(piece_pos[1]) + 1)) else "" for f in self.onboard_pieces]) != self.teams[team][0].upper()):
                moveable_spots.append(piece_pos[0] + str(int(piece_pos[1]) + 1))

            if ((piece_pos[0] + str(int(piece_pos[1]) - 1)) in self.boardPos) and ("".join([f.piece[0] if f.pos == (piece_pos[0] + str(int(piece_pos[1]) - 1)) else "" for f in self.onboard_pieces]) == "" or "".join([f.piece[0] if f.pos == (piece_pos[0] + str(int(piece_pos[1]) - 1)) else "" for f in self.onboard_pieces]) != self.teams[team][0].upper()):
                moveable_spots.append(piece_pos[0] + str(int(piece_pos[1]) - 1))

            if ((chr(ord(piece_pos[0]) - 1) + piece_pos[1]) in self.boardPos) and ("".join([f.piece[0] if f.pos == (chr(ord(piece_pos[0]) - 1) + piece_pos[1]) else "" for f in self.onboard_pieces]) == "" or "".join([f.piece[0] if f.pos == (chr(ord(piece_pos[0]) - 1) + piece_pos[1]) else "" for f in self.onboard_pieces]) != self.teams[team][0].upper()):
                moveable_spots.append(chr(ord(piece_pos[0]) - 1) + piece_pos[1])

            if ((chr(ord(piece_pos[0]) + 1) + piece_pos[1]) in self.boardPos) and ("".join([f.piece[0] if f.pos == (chr(ord(piece_pos[0]) + 1) + piece_pos[1]) else "" for f in self.onboard_pieces]) == "" or "".join([f.piece[0] if f.pos == (chr(ord(piece_pos[0]) + 1) + piece_pos[1]) else "" for f in self.onboard_pieces]) != self.teams[team][0].upper()):
                moveable_spots.append(chr(ord(piece_pos[0]) + 1) + piece_pos[1])

            if ((chr(ord(piece_pos[0]) + 1) + str(int(piece_pos[1]) + 1)) in self.boardPos) and ("".join([f.piece[0] if f.pos == (chr(ord(piece_pos[0]) + 1) + str(int(piece_pos[1]) + 1)) else "" for f in self.onboard_pieces]) == "" or "".join([f.piece[0] if f.pos == (chr(ord(piece_pos[0]) + 1) + str(int(piece_pos[1]) + 1)) else "" for f in self.onboard_pieces]) != self.teams[team][0].upper()):
                moveable_spots.append(chr(ord(piece_pos[0]) + 1) + str(int(piece_pos[1]) + 1))

            if ((chr(ord(piece_pos[0]) - 1) + str(int(piece_pos[1]) + 1)) in self.boardPos) and ("".join([f.piece[0] if f.pos == (chr(ord(piece_pos[0]) - 1) + str(int(piece_pos[1]) + 1)) else "" for f in self.onboard_pieces]) == "" or "".join([f.piece[0] if f.pos == (chr(ord(piece_pos[0]) - 1) + str(int(piece_pos[1]) + 1)) else "" for f in self.onboard_pieces]) != self.teams[team][0].upper()):
                moveable_spots.append(chr(ord(piece_pos[0]) - 1) + str(int(piece_pos[1]) + 1))

            if ((chr(ord(piece_pos[0]) + 1) + str(int(piece_pos[1]) - 1)) in self.boardPos) and ("".join([f.piece[0] if f.pos == (chr(ord(piece_pos[0]) + 1) + str(int(piece_pos[1]) - 1)) else "" for f in self.onboard_pieces]) == "" or "".join([f.piece[0] if f.pos == (chr(ord(piece_pos[0]) + 1) + str(int(piece_pos[1]) - 1)) else "" for f in self.onboard_pieces]) != self.teams[team][0].upper()):
                moveable_spots.append(chr(ord(piece_pos[0]) + 1) + str(int(piece_pos[1]) - 1))

            if ((chr(ord(piece_pos[0]) - 1) + str(int(piece_pos[1]) - 1)) in self.boardPos) and ("".join([f.piece[0] if f.pos == (chr(ord(piece_pos[0]) - 1) + str(int(piece_pos[1]) - 1)) else "" for f in self.onboard_pieces]) == "" or "".join([f.piece[0] if f.pos == (chr(ord(piece_pos[0]) - 1) + str(int(piece_pos[1]) - 1)) else "" for f in self.onboard_pieces]) != self.teams[team][0].upper()):
                moveable_spots.append(chr(ord(piece_pos[0]) - 1) + str(int(piece_pos[1]) - 1))

        return moveable_spots

Chess()
