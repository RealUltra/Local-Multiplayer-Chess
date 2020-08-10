import tkinter
import tkinter.scrolledtext
import messagebox

class Chat():
    def __init__(self, name, upon_new_message):
        self.window = tkinter.Tk()
        self.window.title("Chat")
        self.window.resizable(0,0)
        self.window.attributes("-topmost", True)
        self.window.protocol('WM_DELETE_WINDOW', self.quit)

        self.name = name
        self.upon_new_message = upon_new_message
        self.firstMessage = True
        self.lastMessageAuthor = None
        self.logs = []
        self.draw = self.window.update
        
        self.create()

    def create(self):
        self.console = tkinter.scrolledtext.ScrolledText(state="disabled")
        self.console.pack()

        self.entry = tkinter.scrolledtext.ScrolledText(height=0)
        self.entry.pack()

        self.console.tag_config("name", foreground="red", font=('Helvetica', 10, 'bold'))
        self.window.attributes("-topmost", False)

        self.entry.bind("<Key>", self.KeyPress)

    def quit(self):
        pass

    def KeyPress(self, event):
        a = True
        if len(self.entry.get(0.0, "end")) > 2001:
            a = messagebox.askyesno("Confirmation", "Are You Sure You Want To Send This? Only Its First 2000 Characters will be sent!")

        if "shift" not in str(event).lower() and "return" in str(event).lower() and a:
            message = (self.entry.get(0.0, "end")[:2000].strip())

            if message != '':
                self.add_message(self.name, message)

            self.entry.delete('1.0', "end")

    def add_message(self, name, message, logging=False):
        self.console.config(state='normal')

        name = name.upper()

        if self.firstMessage:
            self.firstMessage = False

            self.console.insert('1.0', name)
            self.console.insert('2.0', ("\n " + message))

            nameEnd = '1.' + str(len(name))

            self.console.tag_add("name", '1.0', nameEnd)

        elif self.lastMessageAuthor == name:
            self.console.insert('end', ("\n " + message))

        else:
            self.console.insert('end', ("\n\n" + name))
            self.console.insert('end', ("\n " + message))

            nameStart = str(int(float(self.console.index('end'))) - 3) + "." + str(len(name))
            nameEnd = str(int(float(self.console.index('end'))) - 2) + "." + str(len(name))

            self.console.tag_add("name", nameStart, nameEnd)

        self.lastMessageAuthor = name
        self.console.config(state='disabled')
        
        if not logging:
            self.logs.append([name, message])
            self.upon_new_message()

    def load_logs(self, logs):
        self.logs = logs
        self.clear()
        for name, message in self.logs:
            self.add_message(name, message, True)

    def clear(self):
        self.firstMessage = True
        self.lastMessageAuthor = None
        self.console.config(state='normal')
        self.console.delete('1.0', 'end')
        self.console.config(state='disabled')