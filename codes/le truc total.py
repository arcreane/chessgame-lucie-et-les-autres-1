import tkinter as tk
from tkinter import messagebox

SIZE = 8
CELL = 80

LIGHT = "#cd93e4"
DARK = "#3c1875"
SELECT = "red"
MOVE = "yellow"

PIECES = {
    "K": "â™”", "Q": "â™•", "R": "â™–", "B": "â™—", "N": "â™˜", "P": "â™™",
    "k": "â™š", "q": "â™›", "r": "â™œ", "b": "â™", "n": "â™ž", "p": "â™Ÿ"
}


class MessyChess:

    def _init_(self, root):

        self.root = root
        self.root.title("SUPER CHESS 2026 DELUXE PRO MAX")

        self.board = [
            list("rnbqkbnr"),
            list("pppppppp"),
            [""] * 8,
            [""] * 8,
            [""] * 8,
            [""] * 8,
            list("PPPPPPPP"),
            list("RNBQKBNR")
        ]

        self.moved = [[False for _ in range(8)] for _ in range(8)]
        self.turn = "white"
        self.selected = None

        self.canvas = tk.Canvas(
            root,
            width=SIZE * CELL,
            height=SIZE * CELL,
            bg="#222222"
        )
        self.canvas.pack()

        self.canvas.bind("<Button-1>", self.click)

        self.draw()

    def restart(self):
        # hidden reset (no button anymore)
        self._init_(self.root)

    def draw(self):

        self.canvas.delete("all")

        for r in range(8):
            for c in range(8):

                color = LIGHT if (r + c) % 2 == 0 else DARK

                x1 = c * CELL
                y1 = r * CELL

                self.canvas.create_rectangle(
                    x1, y1,
                    x1 + CELL,
                    y1 + CELL,
                    fill=color,
                    outline="black"
                )

                piece = self.board[r][c]

                if piece:

                    self.canvas.create_text(
                        x1 + CELL // 2,
                        y1 + CELL // 2,
                        text=PIECES[piece],
                        font=("Comic Sans MS", 34, "bold"),
                        fill="black"
                    )

        # messy border (still kept)
        self.canvas.create_rectangle(
            3, 3,
            SIZE * CELL - 3,
            SIZE * CELL - 3,
            outline="magenta",
            width=6
        )

        # selection highlight
        if self.selected:

            r, c = self.selected

            self.canvas.create_rectangle(
                c * CELL,
                r * CELL,
                c * CELL + CELL,
                r * CELL + CELL,
                outline=SELECT,
                width=4
            )

            for mr, mc in self.legal_moves(r, c):

                self.canvas.create_oval(
                    mc * CELL + 30,
                    mr * CELL + 30,
                    mc * CELL + 50,
                    mr * CELL + 50,
                    fill=MOVE
                )

    def click(self, event):

        r = event.y // CELL
        c = event.x // CELL

        if r > 7 or c > 7:
            return

        piece = self.board[r][c]

        if self.selected is None:

            if piece and self.good_turn(piece):
                self.selected = (r, c)

        else:

            sr, sc = self.selected

            if (r, c) in self.legal_moves(sr, sc):
                self.move(sr, sc, r, c)

            self.selected = None

        self.draw()

    def good_turn(self, piece):

        if self.turn == "white":
            return piece.isupper()
        return piece.islower()

    def move(self, sr, sc, er, ec):

        piece = self.board[sr][sc]

        self.board[er][ec] = piece
        self.board[sr][sc] = ""

        self.moved[sr][sc] = True
        self.turn = "black" if self.turn == "white" else "white"

        self.check_kings()

    def legal_moves(self, r, c):

        piece = self.board[r][c]

        if not piece:
            return []

        moves = []

        # pawn with double move
        if piece.lower() == "p":

            direction = -1 if piece.isupper() else 1
            start_row = 6 if piece.isupper() else 1

            nr = r + direction

            if 0 <= nr < 8 and self.board[nr][c] == "":
                moves.append((nr, c))

                if r == start_row and not self.moved[r][c]:

                    nr2 = r + direction * 2

                    if 0 <= nr2 < 8 and self.board[nr2][c] == "":
                        moves.append((nr2, c))

            for dc in (-1, 1):

                nc = c + dc

                if 0 <= nc < 8 and 0 <= nr < 8:

                    t = self.board[nr][nc]

                    if t and t.isupper() != piece.isupper():
                        moves.append((nr, nc))

        elif piece.lower() == "n":

            jumps = [
                (2,1),(2,-1),(-2,1),(-2,-1),
                (1,2),(1,-2),(-1,2),(-1,-2)
            ]

            for dr, dc in jumps:

                nr, nc = r + dr, c + dc

                if 0 <= nr < 8 and 0 <= nc < 8:

                    t = self.board[nr][nc]

                    if t == "" or t.isupper() != piece.isupper():
                        moves.append((nr, nc))

        elif piece.lower() in ["r", "b", "q"]:

            dirs = []

            if piece.lower() in ["r", "q"]:
                dirs += [(1,0),(-1,0),(0,1),(0,-1)]

            if piece.lower() in ["b", "q"]:
                dirs += [(1,1),(1,-1),(-1,1),(-1,-1)]

            for dr, dc in dirs:

                nr, nc = r + dr, c + dc

                while 0 <= nr < 8 and 0 <= nc < 8:

                    t = self.board[nr][nc]

                    if t == "":
                        moves.append((nr, nc))
                    else:
                        if t.isupper() != piece.isupper():
                            moves.append((nr, nc))
                        break

                    nr += dr
                    nc += dc

        elif piece.lower() == "k":

            for dr in (-1, 0, 1):
                for dc in (-1, 0, 1):

                    if dr == 0 and dc == 0:
                        continue

                    nr, nc = r + dr, c + dc

                    if 0 <= nr < 8 and 0 <= nc < 8:

                        t = self.board[nr][nc]

                        if t == "" or t.isupper() != piece.isupper():
                            moves.append((nr, nc))

        return moves

    def check_kings(self):

        white = False
        black = False

        for row in self.board:
            for p in row:
                if p == "K":
                    white = True
                if p == "k":
                    black = True

        if not white:
            messagebox.showinfo("GAME OVER", "Black wins lol")
            self.restart()

        if not black:
            messagebox.showinfo("GAME OVER", "White wins lol")
            self.restart()


def main():
    root = tk.Tk()
    MessyChess(root)
    root.mainloop()


if __name__ == "_main_":
    main()