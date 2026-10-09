"""
=====================================================================
 TIC-TAC-TOE AI  |  Game Playing  |  Minimax + Alpha-Beta Pruning
 Course  : AI & Expert System  -  Module 4
 Runs on : Python 3.8+  (Google Colab, Jupyter, VS Code, IDLE, terminal)
 How to run : python tictactoe_ai.py          (in Colab: paste in a cell, press Run)
 Players    : HUMAN = "X" (MIN player)   |   AI = "O" (MAX player)
=====================================================================
"""

# ---------------------------------------------------------------------
# PART 1 : IMPORTS AND CONSTANTS
# ---------------------------------------------------------------------
import math                      # gives us math.inf, a value bigger than any real score
import time                      # lets us measure how long each algorithm takes

HUMAN = "X"                      # symbol used by the human player (the MIN player)
AI = "O"                         # symbol used by the computer (the MAX player)
EMPTY = " "                      # an empty cell is stored as a single space

# The board is a list of 9 cells. Index numbers are:
#     0 | 1 | 2
#     3 | 4 | 5
#     6 | 7 | 8
# These are the 8 ways to win: 3 rows, 3 columns, 2 diagonals.
WIN_LINES = [
    (0, 1, 2), (3, 4, 5), (6, 7, 8),     # the three rows
    (0, 3, 6), (1, 4, 7), (2, 5, 8),     # the three columns
    (0, 4, 8), (2, 4, 6),                # the two diagonals
]

nodes_visited = 0                # global counter: how many game states the search looked at


# ---------------------------------------------------------------------
# PART 2 : BOARD HELPER FUNCTIONS  (the "rules of the game")
# ---------------------------------------------------------------------
def new_board():                         # define a function that makes an empty board
    return [EMPTY] * 9                   # a list of 9 spaces = 9 empty cells


def print_board(board):                  # define a function that draws the board on screen
    print()                              # print a blank line for spacing
    for row in range(3):                 # loop over the 3 rows: 0, 1, 2
        a, b, c = board[row * 3: row * 3 + 3]       # take the 3 cells that belong to this row
        print(f" {a} | {b} | {c} ")                  # print the row with | separators
        if row < 2:                                  # after rows 0 and 1 (not after the last row)
            print("---+---+---")                     # print a horizontal divider line
    print()                              # print a blank line after the board


def print_guide():                       # define a function that shows the cell numbers 1-9
    print("\nCell numbers (type 1-9 to choose a cell):")   # heading text for the guide
    print(" 1 | 2 | 3 ")                 # top row numbers
    print("---+---+---")                 # divider
    print(" 4 | 5 | 6 ")                 # middle row numbers
    print("---+---+---")                 # divider
    print(" 7 | 8 | 9 ")                 # bottom row numbers


def get_winner(board):                   # returns "X", "O" or None
    for a, b, c in WIN_LINES:            # check each of the 8 winning lines one by one
        if board[a] != EMPTY and board[a] == board[b] == board[c]:   # same non-empty symbol in all 3 cells?
            return board[a]              # yes, so that symbol is the winner
    return None                          # no line is complete, so there is no winner yet


def is_full(board):                      # returns True if no empty cell is left
    return EMPTY not in board            # True when the list contains no empty cells


def is_terminal(board):                  # terminal test: is the game over?
    return get_winner(board) is not None or is_full(board)   # over if someone won OR the board is full


def available_moves(board):              # returns the list of legal moves (empty cell indexes)
    return [i for i in range(9) if board[i] == EMPTY]        # keep every index whose cell is empty


# ---------------------------------------------------------------------
# PART 3 : UTILITY (SCORE) FUNCTION
# ---------------------------------------------------------------------
def evaluate(board, depth):              # gives a score to a finished game; depth = moves made in the search
    winner = get_winner(board)           # find out who (if anyone) has won
    if winner == AI:                     # the AI (MAX) won
        return 10 - depth                # positive score; a faster win gives a higher score
    if winner == HUMAN:                  # the human (MIN) won
        return depth - 10                # negative score; a slower loss is less bad
    return 0                             # draw = neutral score


# ---------------------------------------------------------------------
# PART 4 : MINIMAX ALGORITHM
# ---------------------------------------------------------------------
def minimax(board, depth, is_maximizing):          # is_maximizing True = AI's turn, False = human's turn
    global nodes_visited                 # we want to change the global counter, not a local copy
    nodes_visited += 1                   # count this game state as "visited"

    if is_terminal(board):               # BASE CASE: has the game ended?
        return evaluate(board, depth)    # yes, so return its score and stop recursing

    if is_maximizing:                    # AI's turn: the AI wants the HIGHEST score
        best = -math.inf                 # start lower than any real score
        for move in available_moves(board):          # try every legal move
            board[move] = AI                         # 1. make the move on the board
            score = minimax(board, depth + 1, False) # 2. ask: how good is this for us? (human moves next)
            board[move] = EMPTY                      # 3. undo the move (backtracking)
            best = max(best, score)                  # keep the highest score seen so far
        return best                      # report the best score to the caller
    else:                                # human's turn: the human wants the LOWEST score
        best = math.inf                  # start higher than any real score
        for move in available_moves(board):          # try every legal move
            board[move] = HUMAN                      # 1. make the move on the board
            score = minimax(board, depth + 1, True)  # 2. ask: how good is this? (AI moves next)
            board[move] = EMPTY                      # 3. undo the move (backtracking)
            best = min(best, score)                  # keep the lowest score seen so far
        return best                      # report the best (lowest) score to the caller


# ---------------------------------------------------------------------
# PART 5 : MINIMAX WITH ALPHA-BETA PRUNING
# ---------------------------------------------------------------------
# alpha = best score MAX can already guarantee  (starts at -infinity)
# beta  = best score MIN can already guarantee  (starts at +infinity)
def alphabeta(board, depth, alpha, beta, is_maximizing):
    global nodes_visited                 # use the shared counter
    nodes_visited += 1                   # count this game state

    if is_terminal(board):               # BASE CASE: game over?
        return evaluate(board, depth)    # return the score of the finished game

    if is_maximizing:                    # AI's turn (MAX)
        best = -math.inf                 # start with the worst possible value for MAX
        for move in available_moves(board):                          # try every legal move
            board[move] = AI                                         # make the move
            score = alphabeta(board, depth + 1, alpha, beta, False)  # evaluate it (human moves next)
            board[move] = EMPTY                                      # undo the move
            best = max(best, score)      # update the best score found so far
            alpha = max(alpha, best)     # MAX can now guarantee at least this much
            if beta <= alpha:            # MIN already has a better option elsewhere...
                break                    # ...so PRUNE: skip all remaining moves here
        return best                      # return the best score for MAX
    else:                                # human's turn (MIN)
        best = math.inf                  # start with the worst possible value for MIN
        for move in available_moves(board):                          # try every legal move
            board[move] = HUMAN                                      # make the move
            score = alphabeta(board, depth + 1, alpha, beta, True)   # evaluate it (AI moves next)
            board[move] = EMPTY                                      # undo the move
            best = min(best, score)      # update the best (lowest) score found so far
            beta = min(beta, best)       # MIN can now guarantee at most this much
            if beta <= alpha:            # MAX already has a better option elsewhere...
                break                    # ...so PRUNE: skip all remaining moves here
        return best                      # return the best score for MIN


# ---------------------------------------------------------------------
# PART 6 : CHOOSING THE AI'S MOVE
# ---------------------------------------------------------------------
def best_move(board, use_alphabeta=True):          # returns the move, the scores, node count and time
    global nodes_visited                 # we will reset the shared counter
    nodes_visited = 0                    # reset the counter before each search
    start = time.perf_counter()          # note the start time (in seconds)

    best_score = -math.inf               # best score found so far for the AI
    chosen = None                        # the move that gives best_score
    scores = {}                          # dictionary: cell number (1-9) -> score, used for display

    for move in available_moves(board):  # the AI tries each legal move at the top level
        board[move] = AI                 # play the move
        if use_alphabeta:                # which algorithm did the caller ask for?
            score = alphabeta(board, 1, -math.inf, math.inf, False)   # alpha-beta; human replies next
        else:                            # otherwise use plain minimax
            score = minimax(board, 1, False)                          # minimax; human replies next
        board[move] = EMPTY              # undo the move
        scores[move + 1] = score         # remember the score (+1 so it matches the 1-9 numbering)
        if score > best_score:           # is this the best move so far?
            best_score = score           # yes, store its score
            chosen = move                # and store the move itself

    elapsed = time.perf_counter() - start      # total time taken = end time - start time
    return chosen, scores, nodes_visited, elapsed   # give everything back to the caller


# ---------------------------------------------------------------------
# PART 7 : HUMAN INPUT
# ---------------------------------------------------------------------
def get_human_move(board):               # keeps asking until the human enters a valid move
    while True:                          # loop forever until we return a valid move
        text = input("Your move (1-9): ").strip()    # read the keyboard input and trim spaces
        if not text.isdigit():           # is the input not a number?
            print("Please type a number from 1 to 9.")   # tell the user what went wrong
            continue                     # go back to the start of the loop
        cell = int(text) - 1             # convert text to number; minus 1 gives list index 0-8
        if cell < 0 or cell > 8:         # is the number outside 1-9?
            print("Number must be between 1 and 9.")     # explain the problem
            continue                     # ask again
        if board[cell] != EMPTY:         # is that cell already taken?
            print("That cell is already taken. Try another.")   # explain the problem
            continue                     # ask again
        return cell                      # the move is valid, so return it


# ---------------------------------------------------------------------
# PART 8 : THE GAME LOOP (Human vs AI)
# ---------------------------------------------------------------------
def play_game(use_alphabeta=True):       # plays one full game against the AI
    name = "Alpha-Beta" if use_alphabeta else "Minimax"       # text label for the chosen algorithm
    print(f"\n=== You are X, the AI is O  (AI algorithm: {name}) ===")   # show who is who
    board = new_board()                  # start with an empty board
    answer = input("Do you want to play first? (y/n): ").strip().lower()  # ask who starts
    human_turn = (answer != "n")         # human starts unless the user typed n
    print_guide()                        # show the 1-9 cell numbers

    while not is_terminal(board):        # keep playing until the game is over
        print_board(board)               # draw the current board
        if human_turn:                   # ---- the human's turn ----
            move = get_human_move(board)         # get a valid move from the keyboard
            board[move] = HUMAN                  # place X on the board
        else:                            # ---- the AI's turn ----
            print("AI is thinking ...")          # tell the user the AI is searching
            move, scores, nodes, secs = best_move(board, use_alphabeta)   # run the search
            board[move] = AI                     # place O on the board
            print(f"Scores for each cell: {scores}")   # show the score the AI computed per cell
            print(f"AI plays cell {move + 1}  |  nodes searched: {nodes}  |  time: {secs:.4f} s")  # stats
        human_turn = not human_turn      # switch turns: True becomes False and vice versa

    print_board(board)                   # draw the final board
    winner = get_winner(board)           # find out how the game ended
    if winner == HUMAN:                  # the human won
        print("You win! (This should be impossible if the AI is perfect.)")   # congratulate
    elif winner == AI:                   # the AI won
        print("The AI wins!")            # announce the AI victory
    else:                                # nobody won
        print("It's a draw. Well played!")   # announce a draw


# ---------------------------------------------------------------------
# PART 9 : COMPARING MINIMAX AND ALPHA-BETA
# ---------------------------------------------------------------------
def compare_algorithms():                # runs both algorithms on the same boards and prints a table
    # Each test case is (description, board). The AI (O) is to move in every case.
    tests = [                            # list of test positions
        ("Empty board (AI moves first)", new_board()),            # the biggest possible search
        ("X took the centre", [EMPTY] * 4 + [HUMAN] + [EMPTY] * 4),   # one X in the middle (cell 5)
        ("X in corner, O in centre, X in opposite corner",       # a position with 3 pieces placed
         [HUMAN, EMPTY, EMPTY, EMPTY, AI, EMPTY, EMPTY, EMPTY, HUMAN]),
    ]
    print("\n{:<48}{:<13}{:>10}{:>11}{:>6}".format(        # print the table header with fixed widths
        "Position", "Algorithm", "Nodes", "Time (s)", "Move"))
    print("-" * 88)                      # print a line of 88 dashes under the header

    for title, board in tests:           # go through each test position
        for use_ab in (False, True):     # run minimax first (False), then alpha-beta (True)
            move, scores, nodes, secs = best_move(board[:], use_ab)   # board[:] passes a copy, keeping original safe
            label = "Alpha-Beta" if use_ab else "Minimax"             # name for the table
            print("{:<48}{:<13}{:>10,}{:>11.4f}{:>6}".format(          # print one result row
                title if not use_ab else "", label, nodes, secs, move + 1))
    print("\nBoth algorithms choose the SAME move; alpha-beta just searches far fewer nodes.")  # key lesson


# ---------------------------------------------------------------------
# PART 10 : MAIN MENU
# ---------------------------------------------------------------------
def main():                              # the program's starting point
    while True:                          # show the menu again and again until the user quits
        print("\n==== TIC-TAC-TOE AI  (Module 4: Game Playing) ====")   # menu title
        print("1. Play against AI  (Alpha-Beta Pruning)")               # option 1
        print("2. Play against AI  (Minimax)")                           # option 2
        print("3. Compare Minimax vs Alpha-Beta (nodes & time)")         # option 3
        print("4. Quit")                                                 # option 4
        choice = input("Choose 1-4: ").strip()   # read the user's choice

        if choice == "1":                # user chose alpha-beta play
            play_game(use_alphabeta=True)        # start a game with alpha-beta
        elif choice == "2":              # user chose minimax play
            play_game(use_alphabeta=False)       # start a game with plain minimax
        elif choice == "3":              # user chose the comparison
            compare_algorithms()                 # run the comparison table
        elif choice == "4":              # user chose to quit
            print("Goodbye!")                    # polite message
            break                                # leave the while loop, ending the program
        else:                            # anything else is invalid
            print("Invalid choice. Please type 1, 2, 3 or 4.")   # ask again


# This guard means: run main() only when the file is executed directly,
# not when it is imported as a module into another program.
if __name__ == "__main__":
    main()                               # start the program
