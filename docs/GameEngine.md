# GameEngine Documentation

## Overview
The GameEngine class implements a 4x8 Minichess variant game engine. This engine manages the game state, move generation, validation, and position tracking for a chess game with a reduced set of pieces and board size.

## Board Representation
- Board Size: 4x8 (width x height)
- Coordinate System: Zero-based indices (0,0) to (7,3)
- Piece Representation: Two-character strings
  - First character: 'w' (white) or 'b' (black)
  - Second character: 'P' (pawn), 'N' (knight), 'B' (bishop), 'K' (king)
- Empty squares: '--'

## Class Structure

### Constructor
```python
def __init__(self):
```
Initializes a new game with:
- Initial board setup
- White to move first
- Empty move log
- Position history tracking

### Core Methods

#### Board Management
```python
def get_initial_board(self):
```
Creates and returns the initial board setup:
- Back rank (white): Knight, Bishop, King, Knight
- Second rank: Four pawns
- Similar setup for black on opposite side

```python
def make_move(self, move):
```
Executes a move on the board:
- Parameters: `move` (Move object)
- Updates board position
- Logs the move
- Switches active player
- Updates position history

```python
def undo_move(self):
```
Reverses the last move made:
- Restores previous board state
- Removes move from log
- Switches back active player
- Updates position history

#### Move Generation and Validation

```python
def get_legal_moves(self):
```
Returns all legal moves for the current player:
1. Generates all possible moves
2. Filters moves that would leave/put own king in check
3. Returns filtered list of legal moves

```python
def get_game_state(self):
```
Determines the current game state:
- Returns "checkmate" if player is in check with no legal moves
- Returns "stalemate" if player has no legal moves but isn't in check
- Returns "ongoing" otherwise

#### Position Analysis

```python
def is_in_check(self):
```
Checks if the current player's king is in check:
- Returns True if king is under attack
- Returns False otherwise

```python
def get_repetition_count(self):
```
Returns how many times the current position has been repeated:
- Useful for detecting draws by repetition
- Considers board state and active player

### Helper Methods

#### Square Analysis
```python
def _is_valid(self, r, c):
```
Validates if coordinates are within board bounds:
- Parameters: row (r) and column (c)
- Returns: True if coordinates are valid, False otherwise

```python
def _is_square_attacked(self, square, friendly_color):
```
Checks if a square is under attack:
- Parameters: 
  - square: (row, col) tuple
  - friendly_color: 'w' or 'b'
- Checks attacks from all enemy piece types

#### Piece-Specific Move Generation

```python
def _get_pawn_moves(self, r, c, moves):
```
Generates possible pawn moves:
- Forward movement (if square is empty)
- Diagonal captures
- No en passant or double first move in this variant

```python
def _get_knight_moves(self, r, c, moves):
```
Generates possible knight moves:
- All eight L-shaped movements
- Checks board boundaries
- Checks for friendly piece blocking

```python
def _get_bishop_moves(self, r, c, moves):
```
Generates possible bishop moves:
- All four diagonal directions
- Continues until blocked
- Captures possible on blocking piece if enemy

```python
def _get_king_moves(self, r, c, moves):
```
Generates possible king moves:
- All eight adjacent squares
- No castling in this variant
- Checks for friendly piece blocking

## Move Class
```python
class Move:
```
Represents a chess move:
### Properties:
- start_row, start_col: Starting position
- end_row, end_col: Ending position
- piece_moved: Piece being moved
- piece_captured: Piece being captured (if any)

### Methods:
- __eq__: Compare moves for equality
- __repr__: String representation for debugging

## Usage Example
```python
# Create a new game
engine = GameEngine()

# Get legal moves for current player
legal_moves = engine.get_legal_moves()

# Make a move
if legal_moves:
    engine.make_move(legal_moves[0])

# Check game state
state = engine.get_game_state()

# Undo last move
engine.undo_move()
```

## Implementation Notes
1. The engine uses a generate-and-filter approach for move generation:
   - First generates all possible moves
   - Then filters out illegal moves that would leave/put the king in check
2. Position repetition is tracked for potential draw detection
3. Piece movement is implemented following standard chess rules with these exceptions:
   - No castling
   - No en passant
   - No pawn double-move
   - No pawn promotion
4. The board is represented as a 2D list for easy square access and modification
