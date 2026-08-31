import sys
import copy
import time
from config import *
from board import Board

class AIPlayer:
    """
    Base class for an AI player. Defines the common interface that all AI
    implementations must follow.
    """
    def __init__(self, board):
        self.engine = engine
        self.nodes_expanded = 0
        self.depth = 1 ## set depth as you see fit and use it further for your works. 

    def get_best_move(self):
        """
        Calculates and returns the best move for the current board state.
        This method must be implemented.
        """
        raise NotImplementedError("Subclasses must implement the get_best_move method.")

    def evaluate_board(self):
        """
        Returns a heuristic score for the current board state.
        This method must be implemented basically the evaluation function for algorithms.
        """
        raise NotImplementedError("Subclasses must implement the evaluate_board method.")

############################################################################



## Feel free to add any additional helper methods or properties you need.



#############################################################################