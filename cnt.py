import pandas as pd

def load_database(file_path):
    """Loads the pre-sorted CSV database."""
    return pd.read_csv(file_path)

def binary_search_positions(df):
    """
    Finds the leftmost and rightmost indices for each number of pieces (2 to 36).
    Returns a list of dictionaries with the results.
    """
    piece_counts = df["Piece_Count"].tolist()

    def find_leftmost(arr, target):
        left, right = 0, len(arr) - 1
        result = -1
        while left <= right:
            mid = (left + right) // 2
            if arr[mid] == target:
                result = mid
                right = mid - 1  
            elif arr[mid] < target:
                left = mid + 1
            else:
                right = mid - 1
        return result

    def find_rightmost(arr, target):
        left, right = 0, len(arr) - 1
        result = -1
        while left <= right:
            mid = (left + right) // 2
            if arr[mid] == target:
                result = mid
                left = mid + 1  
            elif arr[mid] < target:
                left = mid + 1
            else:
                right = mid - 1
        return result
    
    # Store results for each number of pieces
    results = []
    for num_pieces in range(2, 37):  # 2 to 36 inclusive
        left_index = find_leftmost(piece_counts, num_pieces)
        right_index = find_rightmost(piece_counts, num_pieces)
        
        # Append result as a dictionary
        results.append({
            "Num_Pieces": num_pieces,
            "Leftmost_Index": left_index if left_index != -1 else None,
            "Rightmost_Index": right_index if right_index != -1 else None
        })
        
    return results

def save_to_csv(results, output_file):
    """Saves the results to a new CSV file."""
    df = pd.DataFrame(results)
    df.to_csv(output_file, index=False)
    print(f"Data saved to {output_file}")

def main():
    # Load the database
    input_file = "updated_chessData.csv"
    try:
        db = load_database(input_file)
        
        # Calculate indices for all piece counts
        print("Calculating indices for piece counts 2 to 36...")
        results = binary_search_positions(db)
        
        # Save to a new CSV
        output_file = "piece_count_indices.csv"
        save_to_csv(results, output_file)
        
    except FileNotFoundError:
        print(f"File {input_file} not found. Ensure the database file exists.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
