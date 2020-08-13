import pygame
import pieces

class Board():
    def __init__(self, mods={'check':True, 'checkmate':True, 'show_valid_moves':True, 'stalemate':True}):
        self.pieces = {
            'active': [
                pieces.Pawn(self, 'A2', 0),
                pieces.Pawn(self, 'B2', 0),
                pieces.Pawn(self, 'C2', 0),
                pieces.Pawn(self, 'D2', 0),
                pieces.Pawn(self, 'E2', 0),
                pieces.Pawn(self, 'F2', 0),
                pieces.Pawn(self, 'G2', 0),
                pieces.Pawn(self, 'H2', 0),

                pieces.Pawn(self, 'A7', 1),
                pieces.Pawn(self, 'B7', 1),
                pieces.Pawn(self, 'C7', 1),
                pieces.Pawn(self, 'D7', 1),
                pieces.Pawn(self, 'E7', 1),
                pieces.Pawn(self, 'F7', 1),
                pieces.Pawn(self, 'G7', 1),
                pieces.Pawn(self, 'H7', 1),

                pieces.Rook(self, 'A1', 0),
                pieces.Rook(self, 'H1', 0),
                pieces.Rook(self, 'A8', 1),
                pieces.Rook(self, 'H8', 1),

                pieces.Horse(self, 'B1', 0),
                pieces.Horse(self, 'G1', 0),
                pieces.Horse(self, 'B8', 1),
                pieces.Horse(self, 'G8', 1),

                pieces.Bishop(self, 'C1', 0),
                pieces.Bishop(self, 'F1', 0),
                pieces.Bishop(self, 'C8', 1),
                pieces.Bishop(self, 'F8', 1),

                pieces.Queen(self, 'D1', 0),
                pieces.Queen(self, 'D8', 1),

                pieces.King(self, 'E1', 0),
                pieces.King(self, 'E8', 1),

            ],

            'inactive': []
        }

        self.positions = {}
        self.turn = 0
        self.logs = []
        self.mods = mods
        self.to_draw = 0

    def draw(self, window, team):
        color = (62,66,75)

        pygame.draw.rect(window, (72, 73, 75), (0, 550,500, 50)) # Bottom Bar 2
        pygame.draw.rect(window, (34, 32, 33), (0, 50, 50, 450)) # Left Bar
        pygame.draw.rect(window, (72, 73, 75), (0, 0, 500, 50)) # Top Bar 2
        pygame.draw.rect(window, (34, 32, 33), (450, 50, 50, 500)) # Right Bar
        pygame.draw.rect(window, (34, 32, 33), (0, 50, 500, 50)) # Top Bar 1
        pygame.draw.rect(window, (34, 32, 33), (0, 500, 500, 50)) # Bottom Bar 1

        for height in range(8):

            if color == (255, 255, 255) and height != 0:
                color = (62,66,75)
            elif color == (62,66,75) and height != 0:
                color = (255, 255, 255)

            for width in range(8):
                pygame.draw.rect(window, color, (50*(width+1), 50*(height+2), 50, 50))

                if color == (255, 255, 255):
                    color = (62,66,75)
                elif color == (62,66,75):
                    color = (255, 255, 255)

                if team == 0:
                    pos = chr(width + ord("A")) + str(8 - height)
                elif team == 1:
                    pos = chr(ord("H") - width) + str(height + 1)
                data = (50 * (width + 1), 50 * (height + 2))

                if pos not in self.positions:
                    self.positions[pos] = {}
                self.positions[pos][team] = data

        font = pygame.font.Font('fonts\\helvetica.ttf', 20)

        if team == 0:
            for num in range(1, 9):
                corner = self.positions["A" + str(9 - num)][team]
                window.blit(font.render(str(9 - num), True, (255, 255, 255), (34,32,33)), (corner[0]-30, corner[1]+15))

            for letter in range(ord("A"), ord("H")+1):
                bottom = self.positions[chr(letter) + "1"][team]
                window.blit(font.render(chr(letter), True, (255, 255, 255), (34,32,33)), (bottom[0]+15, bottom[1]+65))

        elif team == 1:
            for num in range(1, 9):
                corner = self.positions["H" + str(9 - num)][team]
                window.blit(font.render(str(9 - num), True, (255, 255, 255), (34,32,33)), (corner[0]-30, corner[1]+15))

            for letter in range(ord("A"), ord("H")+1):
                bottom = self.positions[chr(ord("H") - letter + ord("A")) + "8"][team]
                window.blit(font.render(chr(ord("H") - letter + ord("A")), True, (255, 255, 255), (34,32,33)), (bottom[0]+15, bottom[1]+65))

    def move(self, initial_piece, final_pos):
        if initial_piece.type == 'P':
            self.to_draw = 0

        oldPos = initial_piece.pos
        beaten = [f if f.pos == final_pos else None for f in self.pieces['active']]

        while 1:
            if None not in beaten:
                break
            beaten.remove(None)

        beaten_piece = None

        if beaten != []:
            beaten_piece = beaten[0]
            self.pieces['inactive'].append(beaten_piece)
            self.pieces['active'].remove(beaten_piece)
            self.to_draw = 0

        initial_piece.pos = final_pos

        self.turn = {0:1, 1:0}[self.turn]

        self.logs.append([initial_piece, oldPos, final_pos, beaten_piece])

        #self.checkEvents()

    def place(self, window, team):
        yourTeam = 0
        otherTeam = 0

        for piece in self.pieces['inactive']:
            if piece.team == team:
                window.blit(pygame.image.load('Pieces\\' + {0:'white', 1:'black'}[piece.team] + {'P':'Pawn', 'R':'Rook', 'H':'Knight', 'B':'Bishop', 'Q':'Queen', 'K':'King'}[piece.type] + ".png"), ((otherTeam * 50),  0))
                otherTeam += 1

            else:
                window.blit(pygame.image.load('Pieces\\' + {0:'white', 1:'black'}[piece.team] + {'P':'Pawn', 'R':'Rook', 'H':'Knight', 'B':'Bishop', 'Q':'Queen', 'K':'King'}[piece.type] + ".png"), ((yourTeam * 50),  550))
                yourTeam += 1

        for piece in self.pieces['active']:
            piece.draw(window, team)

    def check(self, team):
        if not self.mods['check']:
            return False

        kingPos = "".join([f.pos if f.type == 'K' and f.team == team else "" for f in self.pieces['active']])

        for piece in self.pieces['active']:
            if piece.team != team and kingPos in piece.valid_moves():
                return True

        return False

    def checkEvents(self):
        for piece in self.pieces['active']:
            if piece.type == 'P':
                if (piece.team == 0 and piece.pos[1] == '8') or (piece.team == 1 and piece.pos[1] == '1'):
                    pawn_transformer.PawnTranformer(piece, self.pieces)
                    break

    def undo(self):
        data = self.logs[len(self.logs) - 1]
        piece, initial_pos, final_pos, beaten = data
        self.logs.remove(data)

        piece.pos = initial_pos
        self.turn = {0:1, 1:0}[self.turn]

        if beaten != None:
            self.pieces['inactive'].remove(beaten)
            self.pieces['active'].append(beaten)

    def checkmate(self, team):
        if not self.mods['checkmate']:
            return False

        if not self.check(team):
            return False

        for piece in self.pieces['active']:
            if piece.team == team:
                for pos in piece.valid_moves():
                    if not self.check_upon_move(piece, pos, team):
                        return False

        return True

    def init(self, window):
        self.draw(window, 0)
        self.draw(window, 1)

    def castling_validity(self, team, direction):
        if direction == 0: # Left
            letter = "A"
            middle = ['B', 'C', 'D']
        elif direction == 1: # Right
            letter = 'H'
            middle = ['G', 'F']

        if team == 0:
            num = '1'
        elif team == 1:
            num = '8'

        for piece, old_pos, new_pos, beaten_piece in self.logs:
            if (piece.type == "K" and piece.team == team) or (piece.type == 'R' and piece.team == team and old_pos == (letter + num)):
                return False

        rookExists = False
        for piece in self.pieces['active']:
            if piece.pos == (letter + num) and piece.type == 'R' and piece.team == team:
                rookExists = True

            if piece.pos[0] in middle and piece.pos[1] == num:
                return False

        if not rookExists:
            return False

        return True

    def stalemate(self, team):
        if not self.mods['stalemate']:
            return False

        if self.check(team):
            return False

        for piece in self.pieces['active']:
            if piece.team == team:
                for pos in piece.valid_moves():
                    if not self.check_upon_move(piece, pos, team):
                        return False

        return True

    def check_upon_move(self, initial_piece, final_pos, team):
        self.move(initial_piece, final_pos)

        if self.check(team):
            self.undo()
            return True

        self.undo()

        return False