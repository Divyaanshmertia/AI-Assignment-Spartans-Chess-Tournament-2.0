import random
from board import Move
from config import *

class P25CS0004:
    """
    An agent that plays a random legal move instantly.
    It does not use any adversarial search or evaluation function.
    """
    def __init__(self, engine):
        self.engine = engine
        self.nodes_expanded = 0
        self.depth = 0 # This agent doesn't have a search depth


    def get_best_move(self):
        """
        Finds and returns a random legal move.
        """
        self.nodes_expanded = 1 # It "considers" all moves at once and picks one
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
