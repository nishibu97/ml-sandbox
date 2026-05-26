import argparse
import sys

# ----------------------------------------------------------------------------
# [Sample Input]
# ナンプレの初級問題（0は空きマス）
# "530070000600195000098000060800060003400803001700020006060000280000419005000080079"
# ----------------------------------------------------------------------------

def parse_board(board_str: str) -> list[list[int]]:
    """81文字の文字列を9x9の2次元配列（リスト）に変換する"""
    if len(board_str) != 81:
        raise ValueError("入力はちょうど81文字である必要があります。")
    
    board = []
    for i in range(0, 81, 9):
        row = [int(char) for char in board_str[i:i+9]]
        board.append(row)
    return board

def print_board(board: list[list[int]], title: str = "Board") -> None:
    """ナンプレの盤面を人間が見やすい形式で標準出力する"""
    print(f"--- {title} ---")
    for i, row in enumerate(board):
        if i % 3 == 0 and i != 0:
            print("- - - - - - - - - - - -")
        
        row_str = ""
        for j, val in enumerate(row):
            if j % 3 == 0 and j != 0:
                row_str += " | "
            else:
                if j != 0:
                    row_str += " "
            row_str += str(val) if val != 0 else "."
        print(row_str)
    print("\n")

def solve_sudoku(board: list[list[int]]) -> bool:
    """
    ここに深さ優先探索（バックトラック法）のコアロジックを実装する。
    ※boardを直接書き換え、解けたらTrue、解けなければFalseを返す想定。
    """
    def candidates(row: int, col: int) -> set[int]:
        used = set(board[row])
        used.update(board[r][col] for r in range(9))

        box_row = (row // 3) * 3
        box_col = (col // 3) * 3
        for r in range(box_row, box_row + 3):
            for c in range(box_col, box_col + 3):
                used.add(board[r][c])

        return set(range(1, 10)) - used

    def find_next_cell() -> tuple[int, int, set[int]] | None:
        best_cell: tuple[int, int, set[int]] | None = None

        for row in range(9):
            for col in range(9):
                if board[row][col] != 0:
                    continue

                cell_candidates = candidates(row, col)
                if not cell_candidates:
                    return row, col, cell_candidates
                if best_cell is None or len(cell_candidates) < len(best_cell[2]):
                    best_cell = row, col, cell_candidates

        return best_cell

    next_cell = find_next_cell()
    if next_cell is None:
        return True

    row, col, cell_candidates = next_cell
    for value in sorted(cell_candidates):
        board[row][col] = value
        if solve_sudoku(board):
            return True
        board[row][col] = 0

    return False

def main():
    parser = argparse.ArgumentParser(description="Sudoku Solver Core Logic")
    parser.add_argument(
        "board_str", 
        type=str, 
        help="81文字のナンプレ問題（空きマスは0）。例: 530070000..."
    )
    args = parser.parse_args()

    try:
        # 1. 入力を2次元配列にパース
        board = parse_board(args.board_str)
        print_board(board, "Input Puzzle")

        # 2. ナンプレを解く（探索木ロジック）
        success = solve_sudoku(board)

        # 3. 結果の出力
        if success:
            print_board(board, "Solved Puzzle")
        else:
            print("この問題は解けませんでした（解なし）。")

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()