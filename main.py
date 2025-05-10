import tkinter as tk
from menu import GameMenu


class HomePage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.parent.title("Runner Game")
        self.parent.geometry("600x500")
        self.parent.resizable(False, False)

        self.game_menu = GameMenu(self.parent)


if __name__ == '__main__':
    root = tk.Tk()
    app = HomePage(root)
    root.mainloop()