import chess #generate chess board
import random
from chessboard import display # for visual chessboard
import time
import threading


def generate_position(number_of_pieces):
    """
    Generates a chessboard with exactly `number_of_pieces`, including both kings.
    """
    board = chess.Board()
    board.clear_board()

    if number_of_pieces < 2 or number_of_pieces > 32:
        print("Invalid number of pieces. Must be between 2 and 32.")
        return None

    # define pieces and colors
    colours = [chess.WHITE, chess.BLACK]
    all_pieces = [chess.PAWN, chess.KNIGHT, chess.BISHOP, chess.ROOK, chess.QUEEN]

    # place the kings first with valid placement
    placed_kings = {chess.WHITE: False, chess.BLACK: False}
    king_positions = []

    for color in colours:
        while True:
            square = random.choice(list(chess.SQUARES))
            
            # make sure that square is empty and kings are not adjacent
            if board.piece_at(square) or any(chess.square_distance(square, pos) <= 1 for pos in king_positions):
                continue

            board.set_piece_at(square, chess.Piece(chess.KING, color))
            placed_kings[color] = True
            king_positions.append(square)
            break

    # place the remaining `number_of_pieces - 2` pieces
    remaining_pieces = number_of_pieces - 2
    for _ in range(remaining_pieces):
        piece = random.choice(all_pieces)
        color = random.choice(colours)
        square = random.choice(list(chess.SQUARES))

        # make sure that pawns are not placed on the first or eighth rank
        while board.piece_at(square) or (piece == chess.PAWN and chess.square_rank(square) in {0, 7}):
            square = random.choice(list(chess.SQUARES))

        board.set_piece_at(square, chess.Piece(piece, color))

    # check if kings are not in check
    for color in colours:
        king_square = board.king(color)
        if board.is_attacked_by(not color, king_square):
            print("Generated position has a king in check. Regenerating...")
            return generate_position(number_of_pieces)  # regenerate the board if invalid

    return board



#function to display the position.
def display_position(fen):
    valid_fen = fen
    game_board = display.start()
    display.update(valid_fen, game_board)
    
    for _ in range(200):  # 200 iterations of 0.1 seconds = 20 seconds
        time.sleep(0.1)  
        if display.check_for_quit():  # allow users to quit the display
            break
    
    display.terminate()

def guess_the_position(board):
    """
    Allows the user to guess the positions of pieces on the chessboard.
    Displays the actual positions at the end.
    """
    # get the actual piece positions from the board as a dictionary
    actual_positions = {}
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece:
            actual_positions[chess.square_name(square)] = piece.symbol()

    print("\nStart guessing the positions of the pieces!")
    print("Use standard chess notation (e.g., 'e4', 'h7') and capital letters for white pieces.")
    print("Type 'done' when you are finished.\n")

    user_guesses = {}
    while True:
        guess = input("Enter your guess (e.g., 'e4 N' for a white knight on e4): ").strip()
        
        if guess.lower() == "done":
            break

        try:
            # parse the guess
            position, piece = guess.split()
            position = position.lower()  # ensure the position is lowercase for comparison
            
            # validate the input format
            if position not in chess.SQUARE_NAMES:
                print("Invalid position! Please use standard chess notation (e.g., 'e4').")
                continue
            if len(piece) != 1 or not piece.isalpha():
                print("Invalid piece format! Use single letters (e.g., 'N' for knight).")
                continue

            # Record the guess
            user_guesses[position] = piece
        except ValueError:
            print("Invalid input format! Use 'position piece' (e.g., 'e4 N').")

    # compare guesses with the actual board
    correct_guesses = 0
    for position, guessed_piece in user_guesses.items():
        actual_piece = actual_positions.get(position, None)
        if actual_piece and guessed_piece == actual_piece:
            correct_guesses += 1
            print(f"Correct: {guessed_piece} at {position}")
        else:
            print(f"Incorrect: {guessed_piece} at {position}. Actual: {actual_piece or 'Empty'}")

    # print actual positions of all pieces
    print("\nActual positions of all pieces on the board:")
    for position, piece in sorted(actual_positions.items()):  # Sort by position for easier reading
        print(f"{position}: {piece}")

    # Calculate the total correct guesses
    print(f"\nYou guessed {correct_guesses} out of {len(actual_positions)} pieces correctly.")


def display_position_non_blocking(fen):
    """Display the board in a separate thread."""
    thread = threading.Thread(target=display_position, args=(fen,))
    thread.start()
    thread.join()  # Wait for the thread to finish (optional, can be omitted for true non-blocking behavior)


def main():
    try:
        total_pieces = int(input("Enter the total number of pieces on the board (2-32): "))
        random_board = generate_position(total_pieces)
        if random_board:
            display_position_non_blocking(random_board.fen())  
            guess_the_position(random_board)  
            print("\nGenerated Chess Position:\n")
            print(random_board)
    except ValueError:
        print("Invalid input! Please enter an integer.")



main()

