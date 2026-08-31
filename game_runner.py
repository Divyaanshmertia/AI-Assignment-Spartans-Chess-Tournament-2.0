import time
from board import GameEngine, Move
from p22cs201 import P22CS201
from p25cs0004 import P25CS0004
from config import *

PIECE_SYMBOLS = {
    'wP': '♟', 'bP': '♙', 'wN': '♞', 'bN': '♘',
    'wB': '♝', 'bB': '♗', 'wR': '♜', 'bR': '♖', 'wK': '♚', 'bK': '♔',
    EMPTY_SQUARE: ' '
}

class PlayerClock:
    """Manages the time for a blitz game."""
    def __init__(self, white_time, black_time):
        self.white_time = white_time
        self.black_time = black_time

    def get_time_str(self, time_in_seconds):
        """Formats seconds into MM:SS format."""
        minutes = int(time_in_seconds // 60)
        seconds = int(time_in_seconds % 60)
        return f"{minutes:02d}:{seconds:02d}"

def display_board(engine, clock, white_player, black_player):
    """
    Displays the board with grid lines and the player clock.
    """
    # Generate file labels with proper spacing (each cell is 4 chars: " X │")
    file_labels = '   '.join([chr(ord('a') + i) for i in range(BOARD_WIDTH)])
    top_border = '   ' + '┌' + ''.join(['───┬' if i < BOARD_WIDTH - 1 else '───┐' for i in range(BOARD_WIDTH)])
    mid_border = '   ' + '├' + ''.join(['───┼' if i < BOARD_WIDTH - 1 else '───┤' for i in range(BOARD_WIDTH)])
    bot_border = '   ' + '└' + ''.join(['───┴' if i < BOARD_WIDTH - 1 else '───┘' for i in range(BOARD_WIDTH)])
    
    print(f"\n     {file_labels}")
    print(top_border)
    for r in range(BOARD_HEIGHT):
        rank = 8 - r
        row_str = f" {rank} │"
        for c in range(BOARD_WIDTH):
            piece = engine.board[r][c]
            symbol = PIECE_SYMBOLS.get(piece, '?')
            row_str += f" {symbol} │"
        row_str += f" {rank}"
        
        # Add player and clock display next to the board
        if r == 2:
            row_str += f"   Black ({black_player.__class__.__name__}): {clock.get_time_str(clock.black_time)}"
        if r == 5:
             row_str += f"   White ({white_player.__class__.__name__}): {clock.get_time_str(clock.white_time)}"

        print(row_str)
        if r < BOARD_HEIGHT - 1:
            print(mid_border)
    print(bot_border)
    print(f"     {file_labels}")


def run_game(white_player_type, black_player_type, total_time_seconds=60):
    white_flag, black_flag, white_points, black_points = 0, 0, 0, 0
    white_log, black_log = [], []
    
    engine = GameEngine()
    white_player = white_player_type(engine)
    black_player = black_player_type(engine)
    
    clock = PlayerClock(total_time_seconds, total_time_seconds)
    turn_counter = 0

    print(f"-"*50)
    print(f"Starting Blitz Game: {white_player.__class__.__name__} (Depth {white_player.depth}) vs {black_player.__class__.__name__} (Depth {black_player.depth})")
    print(f"-"*50)
    
    display_board(engine, clock, white_player, black_player)

    file_map = {0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e', 5: 'f', 6: 'g', 7: 'h'}
    rank_map = {i: str(8 - i) for i in range(BOARD_HEIGHT)}

    game_over = False
    while not game_over and turn_counter < 150:
        player = white_player if engine.white_to_move else black_player
        color = '<White>' if engine.white_to_move else '<Black>'
        
        game_state = engine.get_game_state()
        if game_state != "ongoing":
            game_over = True
            break

        start_think_time = time.time()
        
        move = player.get_best_move()

        time_taken = time.time() - start_think_time

        # Update clock
        if engine.white_to_move:
            clock.white_time -= time_taken
            if clock.white_time <= 0:
                print("\nBlack wins on time!")
                game_over = True
                break
        else:
            clock.black_time -= time_taken
            if clock.black_time <= 0:
                print("\nWhite wins on time!")
                game_over = True
                break

        if move:
            engine.make_move(move)
            if move.piece_captured != EMPTY_SQUARE:
                points = abs(PIECE_VALUES.get(move.piece_captured, 0))
                event = f"Captured {move.piece_captured[1]} (+{points})"
                if not engine.white_to_move:
                    white_points += points
                    white_log.append(event)
                else:
                    black_points += points
                    black_log.append(event)

            print("\n" + "-" * 20)
            start = file_map[move.start_col] + rank_map[move.start_row]
            end = file_map[move.end_col] + rank_map[move.end_row]
            move_text = f"Turn {turn_counter + 1}: {color} moves {PIECE_SYMBOLS.get(move.piece_moved)} from {start} to {end}"
            
            if move.piece_captured != EMPTY_SQUARE:
                move_text += f" capturing {PIECE_SYMBOLS.get(move.piece_captured)}"
            
            if engine.is_in_check():
                move_text += " (Check!)"
                if not engine.white_to_move:
                    white_points += 2
                    white_log.append("Gave Check (+2)")
                else:
                    black_points += 2
                    black_log.append("Gave Check (+2)")
            
            print(move_text)
            print(f"Time: {time_taken:.2f}s | Nodes: {player.nodes_expanded}")
            display_board(engine, clock, white_player, black_player)
        else:
            game_over = True

        turn_counter += 1

    print("\n" + "="*15, "GAME OVER", "="*15)
    
    final_game_state = engine.get_game_state()
    # final_score = white_player.evaluate_board(final_game_state)
    # print(f"\nFinal Score (White's perspective): {final_score:.2f}")

    if final_game_state == "checkmate":
        winner = '<Black>' if engine.white_to_move else '<White>'
        print(f"\nCheckmate! {winner} wins.")
        if engine.white_to_move:
             black_log.append("Win by Checkmate (+300)"); black_points += 300
        else:
             white_log.append("Win by Checkmate (+300)"); white_points += 300
    elif final_game_state == "stalemate":
        print("\nStalemate! It's a draw.")
    elif not game_over:
         print("\nGame ended due to turn limit.")

    print("\nPoints Summary:")
    print(f"White ({white_player.__class__.__name__}):")
    for entry in white_log: print("  -", entry)
    print(f"  Total: {white_points}")

    print(f"Black ({black_player.__class__.__name__}):")
    for entry in black_log: print("  -", entry)
    print(f"  Total: {black_points}")
    print(f"Flags: White={white_flag}, Black={black_flag}")

if __name__ == "__main__":
    run_game(white_player_type=P25CS0004, black_player_type=P22CS201, total_time_seconds=60)

## Replace by your AI agents for test purposes. Note you only have to submit one AI agent.