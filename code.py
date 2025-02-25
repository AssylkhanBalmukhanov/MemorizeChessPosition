import chess
from chessboard import display  # for visual chessboard
import pandas as pd
import random
import threading
import time

def load_database(file_path):
    """Loads the pre-sorted CSV database."""
    return pd.read_csv(file_path)

def display_position(fen):
    """Display the chessboard for the given FEN string."""
    game_board = display.start()
    display.update(fen, game_board)

    for _ in range(200):  # 200 iterations of 0.1 seconds = 20 seconds
        time.sleep(0.1)
        if display.check_for_quit():  # allow users to quit the display
            break

    display.terminate()


def locate_positions(indices_df, number_of_pieces):
    row = indices_df[indices_df["Num_Pieces"] == number_of_pieces]
    if row.empty:
        return None, None
    left_index = row.iloc[0]["Leftmost_Index"]
    right_index = row.iloc[0]["Rightmost_Index"]
    if pd.isna(left_index) or pd.isna(right_index):
        return None, None
    return int(left_index), int(right_index)


def display_position_non_blocking(fen):
    """Display the chessboard in a separate thread."""
    thread = threading.Thread(target=display_position, args=(fen,))
    thread.start()
    thread.join()  # optional: wait for the thread to finish


def guess_the_position(board):
    """
    Allows the user to guess the positions of pieces on the chessboard.
    Displays the actual positions at the end.
    """
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
            position, piece = guess.split()
            position = position.lower()  # check if the position is lowercase for comparison

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

    correct_guesses = 0
    for position, guessed_piece in user_guesses.items():
        actual_piece = actual_positions.get(position, None)
        if actual_piece and guessed_piece == actual_piece:
            correct_guesses += 1
            print(f"Correct: {guessed_piece} at {position}")
        else:
            print(f"Incorrect: {guessed_piece} at {position}. Actual: {actual_piece or 'Empty'}")

    
    print("\nActual positions of all pieces on the board:")
    for position, piece in sorted(actual_positions.items()):  # sort by position for easier reading
        print(f"{position}: {piece}")

    print(f"\nYou guessed {correct_guesses} out of {len(actual_positions)} pieces correctly.")


def main():
    try:
        # Load both the chess database and the pre-calculated indices
        chess_file_path = "updated_chessData.csv"
        indices_file_path = "piece_count_indices.csv"
        db = load_database(chess_file_path)
        indices_db = load_database(indices_file_path)

        total_pieces = int(input("Enter the total number of pieces on the board (2-32): "))
        if 2 <= total_pieces <= 32:  # Assuming you want 2-32, adjust to 36 if needed
            left, right = locate_positions(indices_db, total_pieces)

            if left is not None and right is not None:
                print(f"Found positions with {total_pieces} pieces between indices {left} and {right}.")

                random_index = random.randint(left, right)
                selected_fen = db.iloc[random_index]["FEN"]
                evaluation = db.iloc[random_index]["Evaluation"]
                print("Displaying the randomly selected position...")
                display_position_non_blocking(selected_fen)

                board = chess.Board(selected_fen)
                guess_the_position(board)
                print(board)
                print(f"Stockfish evaluation for this position is {evaluation}")
            else:
                print(f"No positions found with {total_pieces} pieces.")
        else:
            print("Please input a value between 2 and 32")
    except ValueError:
        print("Invalid input! Please enter an integer.")
    except FileNotFoundError as e:
        print(f"File not found: {e.filename}. Ensure the database files exist.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
