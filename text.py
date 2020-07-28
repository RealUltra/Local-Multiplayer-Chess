import sys, time, random

board = {'A1': 'W.R', 'A2': 'W.P', 'A3': '   ', 'A4': '   ', 'A5': '   ', 'A6': '   ', 'A7': 'B.P', 'A8': 'B.R', 'B1': 'W.H', 'B2': 'W.P', 'B3': '   ', 'B4': '   ', 'B5': '   ', 'B6': '   ', 'B7': 'B.P', 'B8': 'B.H', 'C1': 'W.B', 'C2': 'W.P', 'C3': '   ', 'C4': '   ', 'C5': '   ', 'C6': '   ', 'C7': 'B.P', 'C8': 'B.B', 'D1': 'W.Q', 'D2': 'W.P', 'D3': '   ', 'D4': '   ', 'D5': '   ', 'D6': '   ', 'D7': 'B.P', 'D8': 'B.Q', 'E1': 'W.K', 'E2': 'W.P', 'E3': '   ', 'E4': '   ', 'E5': '   ', 'E6': '   ', 'E7': 'B.P', 'E8': 'B.K', 'F1': 'W.B', 'F2': 'W.P', 'F3': '   ', 'F4': '   ', 'F5': '   ', 'F6': '   ', 'F7': 'B.P', 'F8': 'B.B', 'G1': 'W.H', 'G2': 'W.P', 'G3': '   ', 'G4': '   ', 'G5': '   ', 'G6': '   ', 'G7': 'B.P', 'G8': 'B.H', 'H1': 'W.R', 'H2': 'W.P', 'H3': '   ', 'H4': '   ', 'H5': '   ', 'H6': '   ', 'H7': 'B.P', 'H8': 'B.R'}
player = random.choice(["White", "Black"]) 
captured = []
WK = -1
BK = -1

def printBoard(board, turn):
    print()
    if turn.lower() == "black":
        print("     ", end="")
        w = "H"
        while w != "A":
            print(w, end=" | ")
            w = chr(ord(w) - 1)
        print("A")
        for f in range(1, 9):
            print(" " + str(f) + " " + "|" + board["H" + str(f)] + "|" + board["G" + str(f)] + "|" + board["F" + str(f)] + "|" + board["E" + str(f)] + "|" + board["D" + str(f)] + "|" + board["C" + str(f)] + "|" + board["B" + str(f)] + "|" + board["A" + str(f)] + "|")

    elif turn.lower() == "white":
        print("     ", end="")
        for f2 in range(ord("A"), ord("H")):
            print(chr(f2), end=" | ")
        print("H")
        for f in range(1, 9):
            print(" " + str(9-f) + " " + "|" + board["A" + str(9-f)] + "|" + board["B" + str(9-f)] + "|" + board["C" + str(9-f)] + "|" + board["D" + str(9-f)] + "|" + board["E" + str(9-f)] + "|" + board["F" + str(9-f)] + "|" + board["G" + str(9-f)] + "|" + board["H" + str(9-f)] + "|")
    
def checkWin():
    a = []
    w = []
    b = []
    for f in board:
        a.append(board[f])
        if board[f].startswith("W"):
            w.append(board[f])
        elif board[f].startswith("B"):
            b.append(board[f])
    a.sort()
    if "W.K" not in a:
        print("\nBlack Wins!")
        time.sleep(5)
        sys.exit()
    elif "B.K" not in a:
        print("\nWhite Wins!")
        time.sleep(5)
        sys.exit()
    elif a == ["B.K", "W.K"]:
        print("\nIts A Draw!")
        time.sleep(5)
        sys.exit()
    elif w == ["W.K"]:
        WK = WK + 1
        if WK == 12:
            print("\nBlack Wins!")
            time.sleep(5)
            sys.exit()
    elif b == ["B.K"]:
        BK = BK + 1
        if BK == 12:
            print("\nWhite Wins!")
            time.sleep(5)
            sys.exit()

def move(old_pos, new_pos):
    problem = False
    while True:
        try:
            if board[old_pos].startswith("W."):
                opposingTeam = "BLACK"
            elif board[old_pos].startswith("B."):
                opposingTeam = "WHITE"

            if board[old_pos].endswith(".P"):
                if (new_pos == old_pos[0] + str(int(old_pos[1]) + 1)) and (board[new_pos] == "   ") and opposingTeam == "BLACK":
                    board[new_pos] = board[old_pos]
                    board[old_pos] = "   "
                    break
                elif (new_pos == old_pos[0] + str(int(old_pos[1]) - 1)) and (board[new_pos] == "   ") and opposingTeam == "WHITE":
                    board[new_pos] = board[old_pos]
                    board[old_pos] = "   "
                    break
                elif (new_pos == old_pos[0] + str(int(old_pos[1]) + 2)) and old_pos[1] == "2" and (board[new_pos] == "   ") and (board[old_pos[0] + str(int(old_pos[1]) + 1)] == "   ") and opposingTeam == "BLACK":
                    board[new_pos] = board[old_pos]
                    board[old_pos] = "   "
                    break
                elif (new_pos == old_pos[0] + str(int(old_pos[1]) - 2)) and old_pos[1] == "7" and (board[new_pos] == "   ") and (board[old_pos[0] + str(int(old_pos[1]) - 1)] == "   ") and opposingTeam == "WHITE":
                    board[new_pos] = board[old_pos]
                    board[old_pos] = "   "
                    break
                elif ((new_pos == chr(ord(old_pos[0])-1) + str(int(old_pos[1]) + 1)) or (new_pos == chr(ord(old_pos[0])+1) + str(int(old_pos[1]) + 1))) and (board[new_pos] == opposingTeam[0] + ".P") and opposingTeam == "BLACK":
                    captured.append(board[new_pos])
                    board[new_pos] = board[old_pos]
                    board[old_pos] = "   "
                    break

                elif ((new_pos == chr(ord(old_pos[0])+1) + str(int(old_pos[1]) - 1)) or (new_pos == chr(ord(old_pos[0])-1) + str(int(old_pos[1]) - 1))) and (board[new_pos] == opposingTeam[0] + ".P") and opposingTeam == "WHITE":
                    captured.append(board[new_pos])
                    board[new_pos] = board[old_pos]
                    board[old_pos] = "   "
                    break

            elif board[old_pos].endswith(".R"):
                if new_pos[0] == old_pos[0]:
                    if int(new_pos[1]) > int(old_pos[1]):
                        for f in range(int(old_pos[1])+1, int(new_pos[1])):
                            if board[old_pos[0] + str(f)] != "   ":
                                problem = True
                    elif int(new_pos[1]) < int(old_pos[1]):
                        w = int(old_pos[1])-1
                        while w != int(new_pos[1]):
                            if board[old_pos[0] + str(w)] != "   ":
                                problem = True
                            w = w - 1
                    if not problem:
                        if board[new_pos].startswith(opposingTeam[0]):
                            captured.append(board[new_pos])
                        if not board[new_pos].startswith(board[old_pos][:2]):
                            board[new_pos] = board[old_pos]
                            board[old_pos] = "   "
                            break
                elif new_pos[1] == old_pos[1]:
                    if ord(new_pos[0]) > ord(old_pos[0]):
                        for f in range(ord(old_pos[0])+1, ord(new_pos[0])):
                            if board[chr(f) + old_pos[1]] != "   ":
                                problem = True
                    elif ord(new_pos[0]) < ord(old_pos[0]):
                        w = ord(old_pos[0])-1
                        while w != ord(new_pos[0]):
                            if board[chr(w) + old_pos[1]] != "   ":
                                problem = True
                            w = w - 1
                    if not problem:
                        if board[new_pos].startswith(opposingTeam[0]):
                            captured.append(board[new_pos])
                        if not board[new_pos].startswith(board[old_pos][:2]):
                            board[new_pos] = board[old_pos]
                            board[old_pos] = "   "
                            return
                        
            elif board[old_pos].endswith(".H"):
                if ((((ord(new_pos[0]) == ord(old_pos[0])+1) or (ord(new_pos[0]) == ord(old_pos[0])-1)) and ((int(new_pos[1]) == int(old_pos[1])+2) or (int(new_pos[1]) == int(old_pos[1])-2)))\
                     and ((board[new_pos] == "   ") or (board[new_pos][0] == opposingTeam[0])))\
                     or (((ord(new_pos[0]) == ord(old_pos[0])+2) or (ord(new_pos[0]) == ord(old_pos[0])-2)) and ((int(new_pos[1]) == int(old_pos[1])+1) or (int(new_pos[1]) == int(old_pos[1])-1))):
                    if board[new_pos].startswith(opposingTeam[0]):
                        captured.append(board[new_pos])
                    if not board[new_pos].startswith(board[old_pos][0]):
                        board[new_pos] = board[old_pos]
                        board[old_pos] = "   "
                        return

            elif board[old_pos].endswith(".B"):
                if ((ord(new_pos[0]) - ord(old_pos[0]))*(ord(new_pos[0]) - ord(old_pos[0])) == (int(new_pos[1]) - int(old_pos[1]))*(int(new_pos[1]) - int(old_pos[1]))):
                    w = old_pos
                    while w != new_pos:
                        if board[w] != "   " and w != old_pos:
                            problem = True
                        if ord(new_pos[0]) > ord(old_pos[0]):
                            a = chr(ord(w[0])+1)
                        else:
                            a = chr(ord(w[0])-1)
                        if int(new_pos[1]) > int(old_pos[1]):
                            b = str(int(w[1])+1)
                        else:
                            b = str(int(w[1])-1)
                        w = a + b
                    if not problem:
                        if board[new_pos].startswith(opposingTeam[0]):
                            captured.append(board[new_pos])
                        if not board[new_pos].startswith(board[old_pos][0]):
                            board[new_pos] = board[old_pos]
                            board[old_pos] = "   "
                            return

            elif board[old_pos].endswith(".Q"):
                if new_pos[0] == old_pos[0] or new_pos[1] == old_pos[1]:
                    if new_pos[0] == old_pos[0]:
                        if int(new_pos[1]) > int(old_pos[1]):
                            for f in range(int(old_pos[1])+1, int(new_pos[1])):
                                if board[old_pos[0] + str(f)] != "   ":
                                    problem = True
                        elif int(new_pos[1]) < int(old_pos[1]):
                            w = int(old_pos[1])-1
                            while w != int(new_pos[1]):
                                if board[old_pos[0] + str(w)] != "   ":
                                    problem = True
                                w = w - 1
                        if not problem:
                            if board[new_pos].startswith(opposingTeam[0]):
                                captured.append(board[new_pos])
                            if not board[new_pos].startswith(board[old_pos][:2]):
                                board[new_pos] = board[old_pos]
                                board[old_pos] = "   "
                                break
                    elif new_pos[1] == old_pos[1]:
                        if ord(new_pos[0]) > ord(old_pos[0]):
                            for f in range(ord(old_pos[0])+1, ord(new_pos[0])):
                                if board[chr(f) + old_pos[1]] != "   ":
                                    problem = True
                        elif ord(new_pos[0]) < ord(old_pos[0]):
                            w = ord(old_pos[0])-1
                            while w != ord(new_pos[0]):
                                if board[chr(w) + old_pos[1]] != "   ":
                                    problem = True
                                w = w - 1
                        if not problem:
                            if board[new_pos].startswith(opposingTeam[0]):
                                captured.append(board[new_pos])
                            if not board[new_pos].startswith(board[old_pos][:2]):
                                board[new_pos] = board[old_pos]
                                board[old_pos] = "   "
                                return
                elif ((ord(new_pos[0]) - ord(old_pos[0]))*(ord(new_pos[0]) - ord(old_pos[0])) == (int(new_pos[1]) - int(old_pos[1]))*(int(new_pos[1]) - int(old_pos[1]))):
                    w = old_pos
                    while w != new_pos:
                        if board[w] != "   " and w != old_pos:
                            problem = True
                        if ord(new_pos[0]) > ord(old_pos[0]):
                            a = chr(ord(w[0])+1)
                        else:
                            a = chr(ord(w[0])-1)
                        if int(new_pos[1]) > int(old_pos[1]):
                            b = str(int(w[1])+1)
                        else:
                            b = str(int(w[1])-1)
                        w = a + b
                    if not problem:
                        if board[new_pos].startswith(opposingTeam[0]):
                            captured.append(board[new_pos])
                        if not board[new_pos].startswith(board[old_pos][0]):
                            board[new_pos] = board[old_pos]
                            board[old_pos] = "   "
                            return

            elif board[old_pos].endswith(".K"):
                if (new_pos == (old_pos[0] + str(int(old_pos[1])+1)))\
                   or (new_pos == (old_pos[0] + str(int(old_pos[1])-1)))\
                   or (new_pos == (chr(ord(old_pos[0])+1) + old_pos[1]))\
                   or (new_pos == (chr(ord(old_pos[0])-1) + old_pos[1]))\
                   or (new_pos == (chr(ord(old_pos[0])+1) + str(int(old_pos[1])+1)))\
                   or (new_pos == (chr(ord(old_pos[0])+1) + str(int(old_pos[1])-1)))\
                   or (new_pos == (chr(ord(old_pos[0])-1) + str(int(old_pos[1])-1)))\
                   or (new_pos == (chr(ord(old_pos[0])-1) + str(int(old_pos[1])+1)))\
                   and not board[new_pos].startswith(board[old_pos][:2]):
                    if board[new_pos].startswith(opposingTeam[0]):
                        captured.append(board[new_pos])
                    board[new_pos] = board[old_pos]
                    board[old_pos] = "   "
                    return

        except:
            print("That's Not Right! Try Again!")
            old_pos = input("Position Of The Piece You Want To Move\nExample: A4\n")
            new_pos = input("Position To Which You Want The Piece To Move To\nExample: A4\n")


        print("That's Not Right! Try Again!")
        old_pos = input("Position Of The Piece You Want To Move\nExample: A4\n")
        new_pos = input("Position To Which You Want The Piece To Move To\nExample: A4\n")

while True:
    multInput = input("1) Single Player\n2) Multiplayer\nType The Number Of Desired GameMode:  ")
    print()
    if multInput == "1":
        print("Sorry, This GameMode Isn't Ready Yet!")
    elif multInput == "2":
        break

while True:
    printBoard(board, "white")
    print("It's White's Turn")
    old_pos = input("Position Of The Piece You Want To Move\nExample: A4\n")
    new_pos = input("Position To Which You Want The Piece To Move To\nExample: A4\n")
    if board[old_pos].startswith("W."):
        move(old_pos, new_pos)
    else:
        continue
    checkWin()
    printBoard(board, "black")
    print("\nIt's Black's Turn")
    old_pos = input("Position Of The Piece You Want To Move\nExample: A4\n")
    new_pos = input("Position To Which You Want The Piece To Move To\nExample: A4\n")
    if board[old_pos].startswith("B."):
        move(old_pos, new_pos)
    else:
        print("That Isn't Right! Try Again!")
        continue
    checkWin()
    print()
