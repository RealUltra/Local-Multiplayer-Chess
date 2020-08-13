import os
import sys

try:
    import pygame
except:
    os.system("pip install pygame")
    import pygame

try:
    import pyperclip
except:
    os.system('pip install pyperclip')
    import pyperclip

import messagebox
import board
import network
import pawn_transformer

class Chess():
    def __init__(self):
        pygame.init()

        try:
            self.client = network.Client(self.handle_message, '172.104.169.112', 5555)
        except:
            messagebox.showinfo('Server Powered Off', "The Server Is Inactive so you cannot use this App right now!")
            sys.exit()

        self.HEIGHT = 650
        self.WIDTH = 500

        self.window = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption('Chess')

        self.FPS = 25
        self.clock = pygame.time.Clock()
        self.run = True
        self.mode = 'MainMenu'

        self.mainloop()

    def mainloop(self):
        while self.run:
            self.clock.tick(self.FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False
                    break
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.upon_mouse_click(pygame.mouse.get_pos())

            if not self.run:
                break

            if self.mode == 'Game':
                self.window.fill({0:(255, 255, 255), 1:(0, 0, 0)}[self.board.turn])
                self.board.draw(self.window, self.team)

                if self.selected != None:
                    x, y = self.board.positions[self.selected.pos][self.team]
                    pygame.draw.rect(self.window, (0, 0, 255), (x, y, 50, 50), 5)

                    if self.board.mods['show_valid_moves']:
                        for pos in self.selected.valid_moves():
                            x, y = self.board.positions[pos][self.team]
                            pygame.draw.rect(self.window, (0, 255, 0), (x, y, 50, 50))
                            pygame.draw.rect(self.window, (0, 0, 0), (x, y, 50, 50), 5)

                        if self.selected.type == 'K':
                            for f in range(2):
                                if self.board.castling_validity(self.team, f):
                                    x, y = self.board.positions[{0:"C", 1:'G'}[f] + {0:"1", 1:"8"}[self.team]][self.team]
                                    pygame.draw.rect(self.window, (255,255,0), (x, y, 50, 50))
                                    pygame.draw.rect(self.window, (0, 0, 0), (x, y, 50, 50), 5)

                self.board.place(self.window, self.team)

                if self.opponent_just_moved and self.board.logs != []:
                    _, old, new, _ = self.board.logs[len(self.board.logs) - 1]

                    if "".join([str(f.team) if f.pos == new else "" for f in self.board.pieces['active']]) != str(self.team):
                        pygame.draw.rect(self.window, (255, 0, 0), (self.board.positions[old][self.team] + (50, 50)), 5)
                        pygame.draw.rect(self.window, (255, 0, 0), (self.board.positions[new][self.team] + (50, 50)), 5)

                        self.opponent_just_moved_iter += 1

                        if self.opponent_just_moved_iter == 100:
                            self.opponent_just_moved = False
                            self.opponent_just_moved_iter = 0

                    else:
                        self.opponent_just_moved = False
                        self.opponent_just_moved_iter = 0

            elif self.mode == "MainMenu":
                self.MainMenu()

            elif self.mode.startswith("Wait|"):
                self.waitingScreen(self.mode.split("|")[1].strip())

            elif self.mode == "JoinWithCode":
                self.joinGameWithCode()

            pygame.display.update()

            if self.mode == 'Game':
                self.checkEvents()

        self.client.send(['QUIT'])
        self.client.close()
        pygame.quit()

    def upon_mouse_click(self, m_pos):
        m_x, m_y = m_pos

        if self.mode == 'Game':
            for piece in self.board.pieces['active']:
                x, y = self.board.positions[piece.pos][self.team]
                if m_x > x and m_y > y and m_x < (x + 50) and m_y < (y + 50) and piece.team == self.team:
                    self.selected = piece
                    return

            if self.selected != None:
                if self.board.turn == self.team:
                    for pos in self.board.positions:
                        x, y = self.board.positions[pos][self.team]
                        if m_x > x and m_y > y and m_x < (x + 50) and m_y < (y + 50):
                            if pos in self.selected.valid_moves():
                                if not self.board.check_upon_move(self.selected, pos, self.team):
                                    self.board.move(self.selected, pos)
                                    self.checkEvents()
                                    self.client.send(['BOARD', self.board])
                                else:
                                    messagebox.showerror("Invalid Move", "It will be a Check if you Move There!")

                                if self.board.checkmate({0:1, 1:0}[self.team]):
                                    messagebox.showinfo('Game Over', "Its A Checkmate For The Other Team!")
                                    self.client.send(["GAME OVER"])
                                    self.mode = "MainMenu"

                                elif self.board.check({0:1, 1:0}[self.team]) and {0:1, 1:0}[self.board.turn] == self.team:
                                    messagebox.showwarning('Check', "It Is a Check For The Other Team!")

                                elif self.board.stalemate({0:1, 1:0}[self.team]):
                                    messagebox.showinfo('Game Over', "Its A Stalemate For The Other Team!")
                                    self.client.send(["GAME OVER"])
                                    self.mode = "MainMenu"

                                break

                            if self.selected.type == 'K' and not self.board.check(self.team):
                                for f in range(2):
                                    num = {0:"1", 1:"8"}[self.team]
                                    if self.board.castling_validity(self.team, f):
                                        if pos == ({0:"C", 1:'G'}[f] + num):
                                            self.board.move(self.selected, pos)

                                            for piece in self.board.pieces['active']:
                                                if piece.type == 'R' and piece.team == self.team and piece.pos == ({0:"A", 1:'H'}[f] + num):
                                                    self.board.move(piece, {0:"D", 1:"F"}[f] + num)
                                                    break

                                            self.board.turn = {0:1, 1:0}[self.board.turn]

                                            if self.board.check(self.team):
                                                self.board.undo()
                                                messagebox.showerror("Invalid Move", "It will be a check if you move there!")
                                            else:
                                                self.checkEvents()
                                                self.client.send(['BOARD', self.board])

                                                if self.board.checkmate({0:1, 1:0}[self.team]):
                                                    messagebox.showinfo('Game Over', "Its A Checkmate For The Other Team!")
                                                    self.client.send(["GAME OVER"])
                                                    self.mode = "MainMenu"

                                                elif self.board.check({0:1, 1:0}[self.team]) and {0:1, 1:0}[self.board.turn] == self.team:
                                                    messagebox.showwarning('Check', "It Is a Check For The Other Team!")

                                                elif self.board.stalemate({0:1, 1:0}[self.team]):
                                                    messagebox.showinfo('Game Over', "Its A Stalemate For The Other Team!")
                                                    self.client.send(["GAME OVER"])
                                                    self.mode = "MainMenu"

                                            break


                else:
                    messagebox.showerror("Its Not Your Turn", "Please Let The Other Player Move!")

            self.selected = None

        elif self.mode == "MainMenu":
            if m_y > 350 and m_y < 450:
                self.mode = "JoinWithCode"
            elif m_y > 200 and m_y < 300:
                self.joinRandomGame()

        elif self.mode.startswith("Wait|"):
            if m_y > 500 and m_y < 600:
                self.client.send(["LEAVING WAIT"])
                self.mode = "MainMenu"
            elif m_y > 300 and m_y < 400:
                pyperclip.copy(self.mode.split("|")[1].strip())
                messagebox.showinfo("Code Copied", "The Join Code Has Been Copied To Your Clipboard!")

        elif self.mode == "JoinWithCode":
            if m_y > 500 and m_y < 600:
                self.mode = "MainMenu"
            elif m_y > 300 and m_y < 400:
                messagebox.showinfo("Joining With Code", "Now Joining With The Code In Your Clipboard...")
                self.client.send(["JOIN", pyperclip.paste().strip()])

    def checkEvents(self):
        whiteKingPos = "".join([f.pos if f.type == 'K' and f.team == 0 else "" for f in self.board.pieces['active']])
        blackKingPos = "".join([f.pos if f.type == 'K' and f.team == 1 else "" for f in self.board.pieces['active']])
        onboard_pieces_pos = [f.pos for f in self.board.pieces['active']]
        white_pieces = [f if f.team == 0 else None for f in self.board.pieces['active']]
        black_pieces = [f if f.team == 1 else None for f in self.board.pieces['active']]

        onboard_pieces_pos.sort()

        kings = [whiteKingPos, blackKingPos]
        kings.sort()

        while 1:
            if None in white_pieces:
                white_pieces.remove(None)

            if None in black_pieces:
                black_pieces.remove(None)

            if None not in black_pieces and None not in white_pieces:
                break

        if whiteKingPos == '':
            messagebox.showinfo("Game Over", "White Won!")
            self.client.send(["GAME OVER"])
            self.mode = "MainMenu"

        elif blackKingPos == '':
            messagebox.showinfo("Game Over", "Black Won!")
            self.client.send(["GAME OVER"])
            self.mode = "MainMenu"

        elif onboard_pieces_pos == kings or self.board.to_draw == 50:
            messagebox.showinfo("Game Over", "Its A Tie!")
            self.client.send(["GAME OVER"])
            self.mode = "MainMenu"

        for piece in self.board.pieces['active']:
            if piece.type == 'P':
                if (piece.team == 0 and piece.pos[1] == '8' and self.team == 0) or (piece.team == 1 and piece.pos[1] == '1' and self.team == 1):
                    pawn_transformer.PawnTranformer(piece, self.board.pieces)
                    break

    def handle_message(self, message):
        if message[0] == "BOARD":
            self.board = message[1]
            self.board.init(self.window)
            self.opponent_just_moved = True
            self.opponent_just_moved_iter = 0
            self.selected = None

            if self.board.logs == []:
                messagebox.showinfo('Mods', "\n".join([(a + "; " + str(b)) for a,b in self.board.mods.items()]))

            else:
                if self.board.checkmate(self.team):
                    messagebox.showinfo("Game Over", "Its a Checkmate for Your Team!")
                    self.client.send(["GAME OVER"])
                    self.mode = "MainMenu"

                elif self.board.check(self.team):
                    messagebox.showwarning("Check", "Its a Check For Your Team")

                elif self.board.stalemate(self.team):
                    messagebox.showinfo("Game Over", "Its a Stalemate for Your Team!")
                    self.client.send(["GAME OVER"])
                    self.mode = "MainMenu"

        if message[0] == "JOIN WITH CODE FAILED":
            messagebox.showerror("Failed To Join", "Invalid Code!")

        if message[0] == "JOIN WILL CODE FULL":
            messagebox.showerror("Failed To Join", "Game Full!")

        if message[0] == "WAITING":
            self.mode = "Wait|" + message[1]

        if message[0] == "STARTED":
            messagebox.showinfo('Get Ready', "Game Started!")
            self.team = message[1]
            self.reset_game()
            self.mode = "Game"

            if self.team == 0:
                self.client.send(["MODS", self.get_mods()])

        if message[0] == "OPPONENT LEFT":
            messagebox.showinfo("You Won", "Your Opponent Just Left! You Win By Default!")
            self.mode = "MainMenu"

    def reset_game(self):
        self.selected = None
        self.opponent_just_moved = False
        self.opponent_just_moved_iter = 0

        self.board = board.Board()
        self.board.init(self.window)

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
        self.client.send(["JOIN RANDOM"])

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

    def get_mods(self):
        mods = {'check':True, 'checkmate':True, 'show_valid_moves':True, 'stalemate':True}

        if not os.path.exists('mods.txt'):
            with open('mods.txt', 'w') as w:
                w.write("\n".join([(a + "; " + b) for a, b in mods.items()]))
            return mods

        with open('mods.txt', 'r') as w:
            for data in w.read().split('\n'):
                mod, ret = data.split('; ')

                if ret.lower().strip() != "false" and ret.lower().strip() != 'true':
                    mods[mod] = True
                    continue

                mods[mod] = {'false':False, 'true':True}[ret.lower().strip()]

        return mods

if __name__ == '__main__':
    Chess()
