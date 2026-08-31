import random
import time
from board import Move

class P22CS201:
    """
    An agent that plays a random legal move after a short delay.
    This can be useful for students to visually follow the game.
    """
    def __init__(self, engine):
        self.engine = engine
        self.nodes_expanded = 0
        self.depth = 0 # This agent doesn't have a search depth

    def get_best_move(self):
        """
        Finds and returns a random legal move after a 0.2-second delay.
        """
        time.sleep(0.2) # Simulate "thinking"
        self.nodes_expanded = 1
        legal_moves = self.engine.get_legal_moves()
        
        if not legal_moves:
            return None
            
        return random.choice(legal_moves)
    
    def evaluate_board(self, game_state):
        """
        A placeholder evaluation function to serve as a template for students.
        This agent does NOT use this evaluation to pick its move; it only
        plays randomly. However, this shows the basic structure.
        """
        # Handle terminal states: checkmate (a huge loss/win) or stalemate (a draw)
        if game_state == "checkmate":
            return -99999 if self.engine.white_to_move else 99999 # high values to tell AI this state is best!
        if game_state == "stalemate":
            return 0

        # Basic evaluation function tip use config values for assessing 
        
        pass


