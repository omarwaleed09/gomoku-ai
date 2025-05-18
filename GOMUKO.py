# Constants
import tkinter as tk
from tkinter import simpledialog

BOARD_SIZE = 15
EMPTY = 0
PLAYER_1 = 1
PLAYER_2 = 2
CELL_SIZE = 40
MARGIN = 20


def check_win(board, player):
    # Horizontal
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE - 4):
            if all(board[row][col + i] == player for i in range(5)):
                return True
    # Vertical
    for col in range(BOARD_SIZE):
        for row in range(BOARD_SIZE - 4):
            if all(board[row + i][col] == player for i in range(5)):
                return True
    # Diagonal TL-BR
    for row in range(BOARD_SIZE - 4):
        for col in range(BOARD_SIZE - 4):
            if all(board[row + i][col + i] == player for i in range(5)):
                return True
    # Diagonal TR-BL
    for row in range(BOARD_SIZE - 4):
        for col in range(4, BOARD_SIZE):
            if all(board[row + i][col - i] == player for i in range(5)):
                return True
    return False


def is_valid_move(board, row, col):
    return 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE and board[row][col] == EMPTY


def is_board_full(board):
    for row in board:
        if EMPTY in row:
            return False
    return True


def generate_candidate_moves(board, radius=2):
    moves = set()
    # If board empty, start center
    if all(board[r][c] == EMPTY for r in range(BOARD_SIZE) for c in range(BOARD_SIZE)):
        center = BOARD_SIZE // 2
        return [(center, center)]
    for r in range(BOARD_SIZE):
        for c in range(BOARD_SIZE):
            if board[r][c] != EMPTY:
                for dr in range(-radius, radius + 1):
                    for dc in range(-radius, radius + 1):
                        nr, nc = r + dr, c + dc
                        if (
                            0 <= nr < BOARD_SIZE
                            and 0 <= nc < BOARD_SIZE
                            and board[nr][nc] == EMPTY
                        ):
                            moves.add((nr, nc))
    if moves:
        return list(moves)
    # Fallback: all empty cells
    return [
        (r, c)
        for r in range(BOARD_SIZE)
        for c in range(BOARD_SIZE)
        if board[r][c] == EMPTY
    ]


def count_sequence(board, player, length, is_open):
    count = 0
    # Horizontal
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE - length + 1):
            if all(board[row][col + i] == player for i in range(length)):
                left_open = col > 0 and board[row][col - 1] == EMPTY
                right_open = (
                    col + length < BOARD_SIZE and board[row][col + length] == EMPTY
                )
                if is_open and (left_open and right_open):
                    count += 1
                elif not is_open and (left_open or right_open):
                    count += 1
    # Vertical
    for col in range(BOARD_SIZE):
        for row in range(BOARD_SIZE - length + 1):
            if all(board[row + i][col] == player for i in range(length)):
                top_open = row > 0 and board[row - 1][col] == EMPTY
                bottom_open = (
                    row + length < BOARD_SIZE and board[row + length][col] == EMPTY
                )
                if is_open and (top_open and bottom_open):
                    count += 1
                elif not is_open and (top_open or bottom_open):
                    count += 1
    # Diagonal TL-BR
    for row in range(BOARD_SIZE - length + 1):
        for col in range(BOARD_SIZE - length + 1):
            if all(board[row + i][col + i] == player for i in range(length)):
                top_left_open = row > 0 and col > 0 and board[row - 1][col - 1] == EMPTY
                bottom_right_open = (
                    row + length < BOARD_SIZE
                    and col + length < BOARD_SIZE
                    and board[row + length][col + length] == EMPTY
                )
                if is_open and (top_left_open and bottom_right_open):
                    count += 1
                elif not is_open and (top_left_open or bottom_right_open):
                    count += 1
    # Diagonal TR-BL
    for row in range(BOARD_SIZE - length + 1):
        for col in range(length - 1, BOARD_SIZE):
            if all(board[row + i][col - i] == player for i in range(length)):
                top_right_open = (
                    row > 0
                    and col < BOARD_SIZE - 1
                    and board[row - 1][col + 1] == EMPTY
                )
                bottom_left_open = (
                    row + length < BOARD_SIZE
                    and col - length >= 0
                    and board[row + length][col - length] == EMPTY
                )
                if is_open and (top_right_open and bottom_left_open):
                    count += 1
                elif not is_open and (top_right_open or bottom_left_open):
                    count += 1
    return count


def evaluate_board(board):
    if check_win(board, PLAYER_1):
        return 100000
    if check_win(board, PLAYER_2):
        return -100000
    score = 0
    weights = {
        "open_4": 10000,
        "semi_open_4": 1000,
        "open_3": 500,
        "semi_open_3": 100,
        "open_2": 50,
        "semi_open_2": 10,
    }
    p1_open_4 = count_sequence(board, PLAYER_1, 4, True)
    p1_semi_open_4 = count_sequence(board, PLAYER_1, 4, False)
    p1_open_3 = count_sequence(board, PLAYER_1, 3, True)
    p1_semi_open_3 = count_sequence(board, PLAYER_1, 3, False)
    p1_open_2 = count_sequence(board, PLAYER_1, 2, True)
    p1_semi_open_2 = count_sequence(board, PLAYER_1, 2, False)
    p2_open_4 = count_sequence(board, PLAYER_2, 4, True)
    p2_semi_open_4 = count_sequence(board, PLAYER_2, 4, False)
    p2_open_3 = count_sequence(board, PLAYER_2, 3, True)
    p2_semi_open_3 = count_sequence(board, PLAYER_2, 3, False)
    p2_open_2 = count_sequence(board, PLAYER_2, 2, True)
    p2_semi_open_2 = count_sequence(board, PLAYER_2, 2, False)

    score += weights["open_4"] * p1_open_4
    score += weights["semi_open_4"] * p1_semi_open_4
    score += weights["open_3"] * p1_open_3
    score += weights["semi_open_3"] * p1_semi_open_3
    score += weights["open_2"] * p1_open_2
    score += weights["semi_open_2"] * p1_semi_open_2

    score -= weights["open_4"] * p2_open_4
    score -= weights["semi_open_4"] * p2_semi_open_4
    score -= weights["open_3"] * p2_open_3
    score -= weights["semi_open_3"] * p2_semi_open_3
    score -= weights["open_2"] * p2_open_2
    score -= weights["semi_open_2"] * p2_semi_open_2
    return score


# Pure Minimax without alpha-beta pruning
def minimax(board, depth, maximizing_player):
    if check_win(board, PLAYER_1):
        return 100000, None
    if check_win(board, PLAYER_2):
        return -100000, None
    if is_board_full(board) or depth == 0:
        return evaluate_board(board), None

    candidate_moves = generate_candidate_moves(board)
    if not candidate_moves:
        return 0, None

    if maximizing_player:
        max_eval = float("-inf")
        best_move = None
        for r, c in candidate_moves:
            board[r][c] = PLAYER_1
            eval_score, _ = minimax(board, depth - 1, False)
            board[r][c] = EMPTY
            if eval_score > max_eval:
                max_eval = eval_score
                best_move = (r, c)
        return max_eval, best_move
    else:
        min_eval = float("inf")
        best_move = None
        for r, c in candidate_moves:
            board[r][c] = PLAYER_2
            eval_score, _ = minimax(board, depth - 1, True)
            board[r][c] = EMPTY
            if eval_score < min_eval:
                min_eval = eval_score
                best_move = (r, c)
        return min_eval, best_move


# Minimax with Alpha-Beta pruning
def alphabeta(board, depth, alpha, beta, maximizing_player):
    if check_win(board, PLAYER_1):
        return 100000, None
    if check_win(board, PLAYER_2):
        return -100000, None
    if is_board_full(board) or depth == 0:
        return evaluate_board(board), None

    candidate_moves = generate_candidate_moves(board)
    if not candidate_moves:
        return 0, None

    if maximizing_player:
        max_eval = float("-inf")
        best_move = None
        for r, c in candidate_moves:
            board[r][c] = PLAYER_1
            eval_score, _ = alphabeta(board, depth - 1, alpha, beta, False)
            board[r][c] = EMPTY
            if eval_score > max_eval:
                max_eval = eval_score
                best_move = (r, c)
            alpha = max(alpha, eval_score)
            if beta <= alpha:
                break
        return max_eval, best_move
    else:
        min_eval = float("inf")
        best_move = None
        for r, c in candidate_moves:
            board[r][c] = PLAYER_2
            eval_score, _ = alphabeta(board, depth - 1, alpha, beta, True)
            board[r][c] = EMPTY
            if eval_score < min_eval:
                min_eval = eval_score
                best_move = (r, c)
            beta = min(beta, eval_score)
            if beta <= alpha:
                break
        return min_eval, best_move


def get_AI_move(board, player, algorithm="minimax", depth=2):
    if algorithm == "minimax":
        _, move = minimax(board, depth, player == PLAYER_1)
        return move
    elif algorithm == "alphabeta":
        _, move = alphabeta(
            board, depth, float("-inf"), float("inf"), player == PLAYER_1
        )
        return move
    else:
        return None


class GUI:
    def __init__(self, mode="hvsai") -> None:
        self.mode = mode
        self.board = [[0 for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        self.root = tk.Tk()
        self.root.title("Gomoku")

        self.last_click: tuple[int, int] = (0, 0)

        # Tkinter variable to pause until click
        self.click_var = tk.IntVar()

        # Calculate canvas size
        canvas_size = 2 * MARGIN + CELL_SIZE * (BOARD_SIZE - 1)
        self.canvas = tk.Canvas(
            self.root, width=canvas_size, height=canvas_size, bg="#F0D9B5"
        )
        self.canvas.pack()

        # Draw the empty board grid
        self.draw_board()

        self.canvas.bind("<Button-1>", self.handle_click)
        # Schedule game start after GUI is ready
        self.choose_mode()
        self.root.after(100, self.start_game)

    def choose_mode(self):
        """Prompt for mode: 1=Human vs AI, 2=AI vs AI. Exit on cancel."""
        while True:
            mode = simpledialog.askinteger(
                "Game Mode",
                "Select mode:\n1: Human vs AI\n2: AI vs AI",
                parent=self.root,
                minvalue=1,
                maxvalue=2,
            )
            if mode is None:
                self.root.destroy()
                return
            if mode == 1:
                self.mode = "hvsai"
                return
            elif mode == 2:
                self.mode = "aivai"
                return
            else:
                self.show_error("Invalid Mode", "Please enter 1 or 2.")

    def show_info(self, title, message):
        """Custom info dialog with styling."""
        dlg = tk.Toplevel(self.root)
        dlg.configure(bg="#B6B09F")
        dlg.title(title)
        lbl = tk.Label(
            dlg,
            text=message,
            bg="#B6B09F",
            fg="#F2F2F2",
            font=("Arial", 16, "bold"),
            wraplength=300,
        )
        lbl.pack(padx=20, pady=20)
        btn = tk.Button(
            dlg,
            text="OK",
            bg="#EAE4D5",
            font=("Arial", 12, "bold"),
            command=dlg.destroy,
        )
        btn.pack(pady=(0, 20))
        dlg.transient(self.root)
        dlg.grab_set()
        self.root.wait_window(dlg)

    def show_error(self, title, message):
        """Custom error dialog, same style as info."""
        self.show_info(title, message)

    def ask_yes_no(self, title, message):
        """Custom yes/no dialog with styling, returns True/False."""
        dlg = tk.Toplevel(self.root)
        dlg.configure(bg="#B6B09F")
        dlg.title(title)
        lbl = tk.Label(
            dlg,
            text=message,
            bg="#B6B09F",
            fg="#F2F2F2",
            font=("Arial", 16, "bold"),
            wraplength=300,
        )
        lbl.pack(padx=20, pady=20)
        result = {"value": False}
        frame = tk.Frame(dlg, bg="#B6B09F")
        frame.pack(pady=(0, 20))

        def on_yes():
            result["value"] = True
            dlg.destroy()

        def on_no():
            dlg.destroy()

        btn_yes = tk.Button(
            frame, text="Yes", bg="#EAE4D5", font=("Arial", 12, "bold"), command=on_yes
        )
        btn_no = tk.Button(
            frame, text="No", bg="#EAE4D5", font=("Arial", 12, "bold"), command=on_no
        )
        btn_yes.pack(side="left", padx=10)
        btn_no.pack(side="left", padx=10)
        dlg.transient(self.root)
        dlg.grab_set()
        self.root.wait_window(dlg)
        return result["value"]

    def reset_board(self):
        """
        Clear the board state and redraw the empty grid.
        """
        self.board = [[0 for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        self.canvas.delete("all")
        self.draw_board()

    def draw_board(self):
        """
        Draws the gomoku board grid on the canvas.
        """
        for i in range(BOARD_SIZE):
            x0 = MARGIN
            y0 = MARGIN + i * CELL_SIZE
            x1 = MARGIN + CELL_SIZE * (BOARD_SIZE - 1)
            y1 = y0
            # Horizontal line
            self.canvas.create_line(x0, y0, x1, y1)

            # Vertical line
            x0 = MARGIN + i * CELL_SIZE
            y0 = MARGIN
            x1 = x0
            y1 = MARGIN + CELL_SIZE * (BOARD_SIZE - 1)
            self.canvas.create_line(x0, y0, x1, y1)

    def draw_stone(self, row, col, color):
        # Update internal board state: 1 for black, 2 for white
        c = color.lower()
        if c == "black":
            self.board[row][col] = 1
        elif c == "white":
            self.board[row][col] = 2
        else:
            raise ValueError("Color must be 'black' or 'white'")

        # Compute pixel coordinates for the center of the cell
        x = MARGIN + col * CELL_SIZE
        y = MARGIN + row * CELL_SIZE
        radius = CELL_SIZE // 2 - 2

        # Draw the stone as a filled oval on the canvas
        self.canvas.create_oval(
            x - radius, y - radius, x + radius, y + radius, fill=c, outline=""
        )

        # Force the GUI to update now before continuing
        self.root.update()

    def pixel_to_cell(self, x, y):
        """
        Convert pixel coordinates (x, y) into board indices (row, col).
        Returns (row, col) if within bounds, otherwise (None, None).
        """
        # Translate pixel to zero-based indices
        col = round((x - MARGIN) / CELL_SIZE)
        row = round((y - MARGIN) / CELL_SIZE)
        if 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE:
            return row, col
        return None, None

    def handle_click(self, event):
        """
        Mouse click handler. Calculates the clicked cell, stores it, and unblocks waiting code.
        """
        row, col = self.pixel_to_cell(event.x, event.y)
        if row is not None and col is not None:
            self.last_click = (row, col)
            # Unblock waiting get_move() call
            self.click_var.set(1)
        else:
            # Ignore clicks outside the board
            print("Click outside the board area")

    def get_move(self) -> tuple[int, int]:
        """
        Pause execution and wait for the user to click a cell.
        Returns the (row, col) of the clicked cell.
        """
        # Reset and wait for a click event
        self.click_var.set(0)
        self.root.wait_variable(self.click_var)
        return self.last_click

    def start_game(self):
        self.reset_board()
        current = 1  # black=1, white=2
        if self.mode == "hvsai":
            human, ai = 1, 2
            while True:
                if current == human:
                    row, col = self.get_move()
                else:
                    move = get_AI_move(self.board, ai)
                    if move is None:
                        self.show_info("Game Over", "AI cannot move. You win!")
                        break
                    row, col = move
                color = "black" if current == 1 else "white"
                self.draw_stone(row, col, color)
                if check_win(self.board, current):
                    self.show_info("Game Over", f"{color.title()} wins!")
                    break
                if is_board_full(self.board):
                    self.show_info("Game Over", "Draw!")
                    break
                current = 2 if current == 1 else 1
        else:
            while True:
                color = "black" if current == 1 else "white"
                move = get_AI_move(self.board, current)
                if move is None:
                    winner = 2 if current == 1 else 1
                    win_color = "black" if winner == 1 else "white"
                    self.show_info(
                        "Game Over", f"AI {win_color.title()} wins by default!"
                    )
                    break
                row, col = move
                self.draw_stone(row, col, color)
                if check_win(self.board, current):
                    self.show_info("Game Over", f"{color.title()} wins!")
                    break
                if is_board_full(self.board):
                    self.show_info("Game Over", "Draw!")
                    break
                current = 2 if current == 1 else 1
        if self.ask_yes_no("Play Again?", "Do you want to play another game?"):
            self.choose_mode()
            self.root.after(100, self.start_game)
        else:
            self.root.destroy()

    def run(self):
        # Start the Tkinter main loop
        self.root.mainloop()


def print_board(board):  # function to print the board
    col_headers = "   " + " ".join(str(i).rjust(3) for i in range(BOARD_SIZE))
    print(col_headers)
    for i, row in enumerate(board):
        row_str = (
            str(i).rjust(2)
            + " "
            + " ".join(
                [
                    " · ".rjust(3)
                    if cell == EMPTY
                    else " X ".rjust(3)
                    if cell == PLAYER_1
                    else " O ".rjust(3)
                    for cell in row
                ]
            )
        )
        print(row_str)


# def play_game(human_vs_ai=True, ai_depth=2):
#     current_player = PLAYER_1
#     while True:
#         print_board(board)
#         if current_player == PLAYER_1 and human_vs_ai:
#             # Human move
#             while True:
#                 try:
#                     row, col = map(
#                         int,
#                         input(
#                             f"Player {current_player} (X), enter row and column (0-{BOARD_SIZE - 1}): "
#                         ).split(),
#                     )
#                     if is_valid_move(board, row, col):
#                         break
#                     else:
#                         print("Invalid move. Try again.")
#                 except ValueError:
#                     print("Invalid input. Enter two numbers separated by space.")
#         else:
#             player_symbol = "X" if current_player == PLAYER_1 else "O"
#             print(f"Player {current_player} ({player_symbol}) (AI) is thinking...")
#             row, col = get_ai_move(board, current_player, "minimax", ai_depth)
#             if row is None or col is None:
#                 print("AI couldn't find a valid move.")
#                 break
#             print(
#                 f"Player {current_player} ({player_symbol}) (AI) plays at ({row}, {col})"
#             )
#         board[row][col] = current_player
#
#         if check_win(board, current_player):
#             print_board(board)
#             player_symbol = "X" if current_player == PLAYER_1 else "O"
#             print(f"Player {current_player} ({player_symbol}) wins!")
#             break
#         if is_board_full(board):
#             print_board(board)
#             print("It's a draw!")
#             break
#
#         current_player = PLAYER_2 if current_player == PLAYER_1 else PLAYER_1


# def ai_vs_ai_game(minimax_depth=2, alpha_beta_depth=2):
#     board = create_board()
#     current_player = PLAYER_1
#     moves_count = 0
#     print("AI vs AI Game: Minimax vs Alpha-Beta Pruning")
#     print("PLAYER_1 (X): Minimax with depth", minimax_depth)
#     print("PLAYER_2 (O): Alpha-Beta with depth", alpha_beta_depth)
#     while True:
#         print_board(board)
#         if current_player == PLAYER_1:
#             print(f"Player {current_player} (X) (Minimax AI) is thinking...")
#             row, col = get_ai_move(board, current_player, "minimax", minimax_depth)
#             print(f"Player {current_player} (X) (Minimax AI) plays at ({row}, {col})")
#         else:
#             print(f"Player {current_player} (O) (Alpha-Beta AI) is thinking...")
#             row, col = get_ai_move(board, current_player, "alphabeta", alpha_beta_depth)
#             print(
#                 f"Player {current_player} (O) (Alpha-Beta AI) plays at ({row}, {col})"
#             )
#
#         if row is None or col is None:
#             print("AI couldn't find a valid move.")
#             break
#
#         board[row][col] = current_player
#         moves_count += 1
#
#         if check_win(board, current_player):
#             print_board(board)
#             player_name = (
#                 "Minimax AI" if current_player == PLAYER_1 else "Alpha-Beta AI"
#             )
#             player_symbol = "X" if current_player == PLAYER_1 else "O"
#             print(
#                 f"Player {current_player} ({player_symbol}) ({player_name}) wins in {moves_count} moves!"
#             )
#             breakw
#
#         if is_board_full(board):
#             print_board(board)
#             print("It's a draw after", moves_count, "moves!")
#             break
#
#         current_player = PLAYER_2 if current_player == PLAYER_1 else PLAYER_1


if __name__ == "__main__":
    # Choose mode: 'hvsai' or 'aivai'
    gui = GUI(mode="aivsai")
    gui.run()
