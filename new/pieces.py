import pygame

class Pawn():
    def __init__(self, board, pos, team):
        self.board = board
        self.pos = pos
        self.team = team
        self.type = 'P'

    def draw(self, window, team):
        x, y = self.board.positions[self.pos][team]
        window.blit(pygame.image.load('Pieces\\' + {0:'white', 1:'black'}[self.team] + "Pawn.png"), (x, y))

    def valid_moves(self):
        moveable_spots = []
        onboard_pieces_pos = [f.pos for f in self.board.pieces['active']]

        if self.team == 0:  # If Team Is White
            pos = (self.pos[0] + str(int(self.pos[1]) + 1))

            if pos not in onboard_pieces_pos:
                moveable_spots.append(pos)

            pos1 = (self.pos[0] + str(int(self.pos[1]) + 1))
            pos2 = (self.pos[0] + str(int(self.pos[1]) + 2))

            if self.pos[1] == "2" and pos1 not in onboard_pieces_pos and pos2 not in onboard_pieces_pos:
                moveable_spots.append(pos2)

            for pos in [(chr(ord(self.pos[0]) + 1) + str(int(self.pos[1]) + 1)), (chr(ord(self.pos[0]) - 1) + str(int(self.pos[1]) + 1))]:
                if pos in onboard_pieces_pos and "".join([str(f.team) if f.pos == pos else "" for f in self.board.pieces['active']]) != str(self.team):
                    moveable_spots.append(pos)

        else:
            pos = (self.pos[0] + str(int(self.pos[1]) - 1))

            if pos not in onboard_pieces_pos:
                moveable_spots.append(pos)

            pos1 = (self.pos[0] + str(int(self.pos[1]) - 1))
            pos2 = (self.pos[0] + str(int(self.pos[1]) - 2))

            if self.pos[1] == "7" and pos1 not in onboard_pieces_pos and pos2 not in onboard_pieces_pos:
                moveable_spots.append(pos2)

            for pos in [(chr(ord(self.pos[0]) + 1) + str(int(self.pos[1]) - 1)), (chr(ord(self.pos[0]) - 1) + str(int(self.pos[1]) - 1))]:
                if pos in onboard_pieces_pos and "".join([str(f.team) if f.pos == pos else "" for f in self.board.pieces['active']]) != str(self.team):
                    moveable_spots.append(pos)

        return moveable_spots

class Rook():
    def __init__(self, board, pos, team):
        self.board = board
        self.pos = pos
        self.team = team
        self.type = 'R'

    def draw(self, window, team):
        x, y = self.board.positions[self.pos][team]
        window.blit(pygame.image.load('Pieces\\' + {0:'white', 1:'black'}[self.team] + "Rook.png"), (x, y))

    def valid_moves(self):
        moveable_spots = []
        onboard_pieces_pos = [f.pos for f in self.board.pieces['active']]

        for num in range(int(self.pos[1]) + 1, 9):
            pos = self.pos[0] + str(num)

            if pos in onboard_pieces_pos:
                if "".join([str(f.team) if f.pos == pos else "" for f in self.board.pieces['active']]) != str(self.team):
                    moveable_spots.append(pos)
                break

            moveable_spots.append(pos)

        for num in range(1, int(self.pos[1])):
            pos = self.pos[0] + str(int(self.pos[1]) - num)

            if pos in onboard_pieces_pos:
                if "".join([str(f.team) if f.pos == pos else "" for f in self.board.pieces['active']]) != str(self.team):
                    moveable_spots.append(pos)
                break

            moveable_spots.append(pos)

        for letter in range(ord("A") + 1, ord(self.pos[0]) + 1):
            pos = chr(ord(self.pos[0]) - (letter - ord("A"))) + str(self.pos[1])

            if pos in onboard_pieces_pos:
                if "".join([str(f.team) if f.pos == pos else "" for f in self.board.pieces['active']]) != str(self.team):
                    moveable_spots.append(pos)
                break

            moveable_spots.append(pos)

        for letter in range(ord(self.pos[0]) + 1, ord("H") + 1):
            pos = chr(letter) + str(self.pos[1])

            if pos in onboard_pieces_pos:
                if "".join([str(f.team) if f.pos == pos else "" for f in self.board.pieces['active']]) != str(self.team):
                    moveable_spots.append(pos)
                break

            moveable_spots.append(pos)

        return moveable_spots

class Horse():
    def __init__(self, board, pos, team):
        self.board = board
        self.pos = pos
        self.team = team
        self.type = 'H'

    def draw(self, window, team):
        x, y = self.board.positions[self.pos][team]
        window.blit(pygame.image.load('Pieces\\' + {0:'white', 1:'black'}[self.team] + "Knight.png"), (x, y))

    def valid_moves(self):
        moveable_spots = []

        for pos in [(chr(ord(self.pos[0]) - 1) + str(int(self.pos[1]) + 2)),
                    (chr(ord(self.pos[0]) + 1) + str(int(self.pos[1]) + 2)),
                    (chr(ord(self.pos[0]) - 1) + str(int(self.pos[1]) - 2)),
                    (chr(ord(self.pos[0]) + 2) + str(int(self.pos[1]) + 1)),
                    (chr(ord(self.pos[0]) - 2) + str(int(self.pos[1]) + 1)),
                    (chr(ord(self.pos[0]) + 1) + str(int(self.pos[1]) - 2)),
                    (chr(ord(self.pos[0]) + 2) + str(int(self.pos[1]) - 1)),
                    (chr(ord(self.pos[0]) - 2) + str(int(self.pos[1]) - 1))]:

            onboard_pieces = "".join([str(f.team) if f.pos == pos else "" for f in self.board.pieces['active']])

            if (pos in self.board.positions) and (onboard_pieces == "" or onboard_pieces != str(self.team)):
                moveable_spots.append(pos)

        return moveable_spots

class Bishop():
    def __init__(self, board, pos, team):
        self.board = board
        self.pos = pos
        self.team = team
        self.type = 'B'

    def draw(self, window, team):
        x, y = self.board.positions[self.pos][team]
        window.blit(pygame.image.load('Pieces\\' + {0:'white', 1:'black'}[self.team] + "Bishop.png"), (x, y))

    def valid_moves(self):
        moveable_spots = []
        onboard_pieces_pos = [f.pos for f in self.board.pieces['active']]
        letter = self.pos[0]
        num = int(self.pos[1])

        while 1:  # Top-Right
            letter = chr(ord(letter) + 1)
            num += 1

            if ord(letter) > ord("H"):
                break

            if num > 8:
                break

            pos = letter + str(num)

            if pos in onboard_pieces_pos:
                if "".join([str(f.team) if f.pos == pos else '' for f in self.board.pieces['active']]) != str(self.team):
                    moveable_spots.append(pos)
                break

            moveable_spots.append(pos)

        letter = self.pos[0]
        num = int(self.pos[1])

        while 1:  # Top-Left
            letter = chr(ord(letter) - 1)
            num += 1

            if ord(letter) < ord("A"):
                break

            if num > 8:
                break

            pos = letter + str(num)

            if pos in onboard_pieces_pos:
                if "".join([str(f.team) if f.pos == pos else '' for f in self.board.pieces['active']]) != str(self.team):
                    moveable_spots.append(pos)
                break

            moveable_spots.append(pos)

        letter = self.pos[0]
        num = int(self.pos[1])

        while 1:  # Bottom-Left
            letter = chr(ord(letter) - 1)
            num -= 1

            if ord(letter) < ord("A"):
                break

            if num < 1:
                break

            pos = letter + str(num)

            if pos in onboard_pieces_pos:
                if "".join([str(f.team) if f.pos == pos else '' for f in self.board.pieces['active']]) != str(self.team):
                    moveable_spots.append(pos)
                break

            moveable_spots.append(pos)

        letter = self.pos[0]
        num = int(self.pos[1])

        while 1:  # Bottom-Right
            letter = chr(ord(letter) + 1)
            num -= 1

            if ord(letter) > ord("H"):
                break

            if num < 1:
                break

            pos = letter + str(num)

            if pos in onboard_pieces_pos:
                if "".join([str(f.team) if f.pos == pos else '' for f in self.board.pieces['active']]) != str(self.team):
                    moveable_spots.append(pos)
                break

            moveable_spots.append(pos)

        return moveable_spots

class Queen():
    def __init__(self, board, pos, team):
        self.board = board
        self.pos = pos
        self.team = team
        self.type = 'Q'

    def draw(self, window, team):
        x, y = self.board.positions[self.pos][team]
        window.blit(pygame.image.load('Pieces\\' + {0:'white', 1:'black'}[self.team] + "Queen.png"), (x, y))

    def valid_moves(self):
        moveable_spots = []
        onboard_pieces_pos = [f.pos for f in self.board.pieces['active']]

        for num in range(int(self.pos[1]) + 1, 9):
            pos = self.pos[0] + str(num)

            if pos in onboard_pieces_pos:
                if "".join([str(f.team) if f.pos == pos else "" for f in self.board.pieces['active']]) != str(self.team):
                    moveable_spots.append(pos)
                break

            moveable_spots.append(pos)

        for num in range(1, int(self.pos[1])):
            pos = self.pos[0] + str(int(self.pos[1]) - num)

            if pos in onboard_pieces_pos:
                if "".join([str(f.team) if f.pos == pos else "" for f in self.board.pieces['active']]) != str(self.team):
                    moveable_spots.append(pos)
                break

            moveable_spots.append(pos)

        for letter in range(ord("A") + 1, ord(self.pos[0]) + 1):
            pos = chr(ord(self.pos[0]) - (letter - ord("A"))) + str(self.pos[1])

            if pos in onboard_pieces_pos:
                if "".join([str(f.team) if f.pos == pos else "" for f in self.board.pieces['active']]) != str(self.team):
                    moveable_spots.append(pos)
                break

            moveable_spots.append(pos)

        for letter in range(ord(self.pos[0]) + 1, ord("H") + 1):
            pos = chr(letter) + str(self.pos[1])

            if pos in onboard_pieces_pos:
                if "".join([str(f.team) if f.pos == pos else "" for f in self.board.pieces['active']]) != str(self.team):
                    moveable_spots.append(pos)
                break

            moveable_spots.append(pos)

        letter = self.pos[0]
        num = int(self.pos[1])

        while 1:  # Top-Right
            letter = chr(ord(letter) + 1)
            num += 1

            if ord(letter) > ord("H"):
                break

            if num > 8:
                break

            pos = letter + str(num)

            if pos in onboard_pieces_pos:
                if "".join([str(f.team) if f.pos == pos else '' for f in self.board.pieces['active']]) != str(self.team):
                    moveable_spots.append(pos)
                break

            moveable_spots.append(pos)

        letter = self.pos[0]
        num = int(self.pos[1])

        while 1:  # Top-Left
            letter = chr(ord(letter) - 1)
            num += 1

            if ord(letter) < ord("A"):
                break

            if num > 8:
                break

            pos = letter + str(num)

            if pos in onboard_pieces_pos:
                if "".join([str(f.team) if f.pos == pos else '' for f in self.board.pieces['active']]) != str(self.team):
                    moveable_spots.append(pos)
                break

            moveable_spots.append(pos)

        letter = self.pos[0]
        num = int(self.pos[1])

        while 1:  # Bottom-Left
            letter = chr(ord(letter) - 1)
            num -= 1

            if ord(letter) < ord("A"):
                break

            if num < 1:
                break

            pos = letter + str(num)

            if pos in onboard_pieces_pos:
                if "".join([str(f.team) if f.pos == pos else '' for f in self.board.pieces['active']]) != str(self.team):
                    moveable_spots.append(pos)
                break

            moveable_spots.append(pos)

        letter = self.pos[0]
        num = int(self.pos[1])

        while 1:  # Bottom-Right
            letter = chr(ord(letter) + 1)
            num -= 1

            if ord(letter) > ord("H"):
                break

            if num < 1:
                break

            pos = letter + str(num)

            if pos in onboard_pieces_pos:
                if "".join([str(f.team) if f.pos == pos else '' for f in self.board.pieces['active']]) != str(self.team):
                    moveable_spots.append(pos)
                break

            moveable_spots.append(pos)

        return moveable_spots

class King():
    def __init__(self, board, pos, team):
        self.board = board
        self.pos = pos
        self.team = team
        self.type = 'K'

    def draw(self, window, team):
        x, y = self.board.positions[self.pos][team]
        window.blit(pygame.image.load('Pieces\\' + {0:'white', 1:'black'}[self.team] + "King.png"), (x, y))

    def valid_moves(self):
        moveable_spots = []

        for pos in [(self.pos[0] + str(int(self.pos[1]) + 1)),
                    (self.pos[0] + str(int(self.pos[1]) - 1)),
                    (chr(ord(self.pos[0]) - 1) + self.pos[1]),
                    (chr(ord(self.pos[0]) + 1) + self.pos[1]),
                    (chr(ord(self.pos[0]) + 1) + str(int(self.pos[1]) + 1)),
                    (chr(ord(self.pos[0]) - 1) + str(int(self.pos[1]) + 1)),
                    (chr(ord(self.pos[0]) + 1) + str(int(self.pos[1]) - 1)),
                    (chr(ord(self.pos[0]) - 1) + str(int(self.pos[1]) - 1))]:

                onboard_pieces = "".join([str(f.team) if f.pos == pos else "" for f in self.board.pieces['active']])

                if (pos in self.board.positions) and (onboard_pieces == "" or onboard_pieces != str(self.team)):
                    moveable_spots.append(pos)

        return moveable_spots