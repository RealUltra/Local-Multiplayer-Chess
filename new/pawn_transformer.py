import tkinter
import tkinter.ttk
import os

try:
    import ttkthemes
except:
    os.system('pip install ttkthemes')
    import ttkthemes

import pieces

class PawnTranformer():
    def __init__(self, pawn, pieces):
        self.window = ttkthemes.themed_tk.ThemedTk()
        self.window.title('What Should Your Pawn Turn Into?')
        self.window.resizable(0,0)
        self.window.set_theme('vista')
        self.window.attributes('-topmost', 1)

        self.pawn = pawn
        self.pieces = pieces

        buttons = ['Queen', 'Rook', 'Bishop', 'Horse']

        for button in range(len(buttons)):
            index = len(buttons) - button - 1
            tkinter.ttk.Button(self.window, text=buttons[index], width=60, command=lambda index=index: self.button_clicked(buttons[index])).pack(side=tkinter.BOTTOM)

        self.window.mainloop()

    def button_clicked(self, button):
        self.window.destroy()
        self.pieces['active'].append(eval('pieces.' + button)(self.pawn.board, self.pawn.pos, self.pawn.team))
        self.pieces['active'].remove(self.pawn)
