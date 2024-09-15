
import tkinter as tk
import random
from tkinter import messagebox, simpledialog

# Board ko initialize kar rahe hain yarr yha na 9 box ka bnega 
board = [' ' for _ in range(9)]
current_player = 'X'  
difficulty = 'Easy'   # Default difficulty level

# Player ka naam enter karwane ke liye function
def get_player_name():
    name = simpledialog.askstring("Player Name", "Enter your name:")
    return name if name else "You"  # Agar naam na ho to default 'You' hoga ye optional hai 

player_name = get_player_name()

# Window ka title set karna as per player and computer
root = tk.Tk()
root.title(f"Computer vs {player_name}")

# Board ko update karne ka kaam (GUI mein dikhana)
def update_board():
    for i in range(9):
        if board[i] == 'X':
            buttons[i].config(text=board[i], fg="blue", bg="lightyellow", state=tk.DISABLED)
        elif board[i] == 'O':
            buttons[i].config(text=board[i], fg="red", bg="lightyellow", state=tk.DISABLED)
        else:
            buttons[i].config(text=board[i], fg="black", bg="white", state=tk.NORMAL)

# Check karte hain winner ko
def check_winner(player):
    win_conditions = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # rows
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # columns
        [0, 4, 8], [2, 4, 6]              # diagonals
    ]
    for condition in win_conditions:
        if board[condition[0]] == board[condition[1]] == board[condition[2]] == player:
            return True
    return False

# Board full hai ya nahi, check karte hain
def is_board_full():
    return ' ' not in board

# Player ke move ko handle karte hain
def player_move(index):
    global current_player
    if board[index] == ' ':
        board[index] = 'X'  # Player ke moves ab 'X' ke roop mein dikhenge
        update_board()

        if check_winner('X'):
            messagebox.showinfo("Game Over", f"{player_name} wins!", icon="info")
            reset_game()
            return
        if is_board_full():
            messagebox.showinfo("Game Over", "It's a tie!", icon="info")
            reset_game()
            return

        current_player = 'O'  # Ab computer ki turn hogi
        root.after(500, computer_move)

# Easy level ke liye random move
def random_move():
    available_moves = [i for i in range(9) if board[i] == ' ']
    return random.choice(available_moves)

# Medium level ke liye computer ko jeet ya rokne ka chance dena
def medium_move():
    for player in ['O', 'X']:
        for i in range(9):
            if board[i] == ' ':
                board[i] = player
                if check_winner(player):
                    board[i] = 'O'  # Agar move jeetata hai to 'O' laga dega
                    return i
                board[i] = ' '  # Move ko undo karna

    return random_move()

# Hard level ke liye minimax algorithm
def minimax(board, depth, is_maximizing):
    if check_winner('O'):
        return 1
    elif check_winner('X'):
        return -1
    elif is_board_full():
        return 0

    if is_maximizing:
        best_score = -float('inf')
        for i in range(9):
            if board[i] == ' ':
                board[i] = 'O'
                score = minimax(board, depth + 1, False)
                board[i] = ' '
                best_score = max(score, best_score)
        return best_score
    else:
        best_score = float('inf')
        for i in range(9):
            if board[i] == ' ':
                board[i] = 'X'
                score = minimax(board, depth + 1, True)
                board[i] = ' '
                best_score = min(score, best_score)
        return best_score

def hard_move():
    best_score = -float('inf')
    best_move = None
    for i in range(9):
        if board[i] == ' ':
            board[i] = 'O'
            score = minimax(board, 0, False)
            board[i] = ' '
            if score > best_score:
                best_score = score
                best_move = i
    return best_move

# Computer ke move ko handle karna
def computer_move():
    global current_player
    if difficulty == 'Easy':
        move = random_move()
    elif difficulty == 'Medium':
        move = medium_move()
    else:
        move = hard_move()

    board[move] = 'O'
    update_board()

    if check_winner('O'):
        messagebox.showinfo("Game Over", "Computer wins!", icon="info")
        reset_game()
        return
    if is_board_full():
        messagebox.showinfo("Game Over", "It's a tie!", icon="info")
        reset_game()
        return

    current_player = 'X'  # Phir se player ki turn hogi

# Game ko reset karna
def reset_game():
    global board, current_player
    board = [' ' for _ in range(9)]
    current_player = 'X'
    update_board()

# Difficulty level set karne ka function
def set_difficulty(level):
    global difficulty
    difficulty = level
    messagebox.showinfo("Difficulty Set", f"Difficulty set to {level}")

# Board ke liye buttons bana rahe hain
buttons = []
for i in range(9):
    button = tk.Button(root, text=' ', font='Arial 20 bold', height=2, width=5, 
                       bg="lightblue", command=lambda i=i: player_move(i))
    button.grid(row=i//3, column=i%3, padx=5, pady=5)
    buttons.append(button)

# Menu for difficulty level banana
menu = tk.Menu(root)
root.config(menu=menu)
options_menu = tk.Menu(menu, tearoff=0)
menu.add_cascade(label="Options", menu=options_menu)
options_menu.add_command(label="Easy", command=lambda: set_difficulty("Easy"))
options_menu.add_command(label="Medium", command=lambda: set_difficulty("Medium"))
options_menu.add_command(label="Hard", command=lambda: set_difficulty("Hard"))
options_menu.add_separator()
options_menu.add_command(label="Reset Game", command=reset_game)


root.mainloop()

#code by dev kumar
#internship with hex-software
