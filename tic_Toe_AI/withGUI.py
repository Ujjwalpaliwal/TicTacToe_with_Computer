import tkinter as tk
from tkinter import messagebox

# --- Game constants ---
X = "X"
O = "O"
EMPTY = " "
TIE = "TIE"
NUM_SQUARES = 9

# --- Core game logic ---

def new_board():
    return [EMPTY] * NUM_SQUARES

def actions(board):
    return [i for i in range(NUM_SQUARES) if board[i] == EMPTY]

def winner(board):
    WAYS_TO_WIN = (
        (0,1,2), (3,4,5), (6,7,8),
        (0,3,6), (1,4,7), (2,5,8),
        (0,4,8), (2,4,6)
    )
    for a,b,c in WAYS_TO_WIN:
        if board[a] == board[b] == board[c] != EMPTY:
            return board[a]
    if EMPTY not in board:
        return TIE
    return None

def terminal(board):
    return winner(board) is not None

def player_token(board):
    # X always goes first; current player is decided by counts
    return X if board.count(X) == board.count(O) else O

def result(board, move, token):
    nb = board[:]
    nb[move] = token
    return nb

def utility(board):
    w = winner(board)
    if w == X: return 1
    if w == O: return -1
    return 0  # tie or non-terminal (should not be called on non-terminal)

def minimax(board, alpha=float("-inf"), beta=float("inf")):
    """
    Returns (best_move, best_value) for the current player on 'board'.
    X maximizes, O minimizes. Includes alpha-beta pruning.
    """
    if terminal(board):
        return None, utility(board)

    turn = player_token(board)
    is_max = (turn == X)

    best_move = None
    best_val = float("-inf") if is_max else float("inf")

    # Small ordering heuristic to speed up: center, corners, edges
    order = [4,0,2,6,8,1,3,5,7]
    for move in (m for m in order if m in actions(board)):
        nb = result(board, move, turn)
        _, val = minimax(nb, alpha, beta)

        if is_max:
            if val > best_val:
                best_val, best_move = val, move
            alpha = max(alpha, best_val)
            if beta <= alpha:
                break
        else:
            if val < best_val:
                best_val, best_move = val, move
            beta = min(beta, best_val)
            if beta <= alpha:
                break

    return best_move, best_val

# --- GUI ---

class TicTacToeGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic-Tac-Toe (Minimax)")
        self.board = new_board()

        # Who is human/computer (tokens)
        self.human = X
        self.computer = O

        # Scoreboard
        self.human_score = 0
        self.comp_score = 0
        self.tie_score = 0

        self.build_ui()
        self.start_new_game()

    def build_ui(self):
        top = tk.Frame(self.root, padx=10, pady=6)
        top.pack()

        self.status = tk.Label(top, text="Welcome!", font=("Arial", 14, "bold"))
        self.status.grid(row=0, column=0, columnspan=3, pady=(0,6))

        # Scoreboard
        self.score_lbl = tk.Label(
            top,
            font=("Arial", 12),
            text="You: 0    Computer: 0    Ties: 0"
        )
        self.score_lbl.grid(row=1, column=0, columnspan=3, pady=(0,8))

        # 3x3 board
        self.buttons = []
        grid = tk.Frame(self.root, padx=10, pady=10)
        grid.pack()
        for i in range(NUM_SQUARES):
            btn = tk.Button(
                grid, text=" ", font=("Arial", 24, "bold"),
                width=3, height=1, command=lambda i=i: self.human_move(i)
            )
            btn.grid(row=i//3, column=i%3, padx=4, pady=4)
            self.buttons.append(btn)

        # Bottom controls
        bottom = tk.Frame(self.root, pady=8)
        bottom.pack()

        tk.Button(bottom, text="New Game", command=self.start_new_game).grid(row=0, column=0, padx=6)
        tk.Button(bottom, text="Quit", command=self.root.quit).grid(row=0, column=1, padx=6)

    def update_board_ui(self):
        for i, btn in enumerate(self.buttons):
            btn.config(text=self.board[i] if self.board[i] != EMPTY else " ",
                       state=("disabled" if self.board[i] != EMPTY else "normal"))

    def set_status(self, text):
        self.status.config(text=text)

    def start_new_game(self):
        self.board = new_board()
        self.update_board_ui()

        # Ask who goes first (like your console version)
        goes_first = messagebox.askyesno("First Move", "Do you want to play first?")
        if goes_first:
            self.human, self.computer = X, O
        else:
            self.human, self.computer = O, X

        # After choosing, X always moves first—if computer is X, it moves now
        self.set_status(f"Your token: {self.human}  •  Computer: {self.computer}")
        self.update_board_ui()

        if player_token(self.board) == self.computer:
            self.disable_all()
            self.root.after(300, self.computer_turn)
        else:
            self.enable_all()

    def enable_all(self):
        for i, b in enumerate(self.buttons):
            if self.board[i] == EMPTY:
                b.config(state="normal")

    def disable_all(self):
        for b in self.buttons:
            b.config(state="disabled")

    def end_if_over(self):
        if terminal(self.board):
            w = winner(self.board)
            if w == TIE:
                self.tie_score += 1
                messagebox.showinfo("Result", "It's a tie!")
            elif w == self.human:
                self.human_score += 1
                messagebox.showinfo("Result", "You win! 🎉")
            else:
                self.comp_score += 1
                messagebox.showinfo("Result", "I win! 🤖")

            self.score_lbl.config(text=f"You: {self.human_score}    Computer: {self.comp_score}    Ties: {self.tie_score}")
            self.start_new_game()
            return True
        return False

    def human_move(self, i):
        # Only allow if it's human's turn
        if self.board[i] != EMPTY:
            return

        # Human can move only when the current token equals human token
        if player_token(self.board) != self.human:
            return  # ignore accidental clicks
        self.board[i] = self.human
        self.update_board_ui()

        # Check if finished
        if self.end_if_over():
            return

        # Computer's turn next
        self.disable_all()
        self.root.after(250, self.computer_turn)

    def computer_turn(self):
        # If somehow it's not computer's turn, return safely
        if player_token(self.board) != self.computer or terminal(self.board):
            self.enable_all()
            return

        move, _ = minimax(self.board)
        # Safety: if minimax returns None (shouldn't happen), pick first legal
        if move is None:
            legal = actions(self.board)
            move = legal[0] if legal else None

        if move is not None:
            self.board[move] = self.computer
            self.update_board_ui()

        if self.end_if_over():
            return

        self.enable_all()
        self.set_status(f"Your token: {self.human}  •  Computer: {self.computer}")

if __name__ == "__main__":
    root = tk.Tk()
    app = TicTacToeGUI(root)
    root.mainloop()
