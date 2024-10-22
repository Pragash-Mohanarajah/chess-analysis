import chess
import torch
import random
from board_tensor import board_to_tensor

class ChessEnvironment:
    def __init__(self, policy_net, index_to_uci, uci_to_index, epsilon_start=1.0, epsilon_end=0.1, epsilon_decay=1000):
        self.board = chess.Board()
        self.policy_net = policy_net  # DQN model
        self.index_to_uci = index_to_uci
        self.uci_to_index = uci_to_index
        self.epsilon_start = epsilon_start
        self.epsilon_end = epsilon_end
        self.epsilon_decay = epsilon_decay
        self.epsilon = self.epsilon_start
        self.steps_done = 0

    def reset(self):
        """Resets the chess environment to the starting position."""
        self.board.reset()
        return board_to_tensor(self.board)
    
    def get_state(self, board):
        """Converts a chess board to a tensor state."""
        return board_to_tensor(board)

    def get_legal_moves(self):
        """Return a list of all legal moves in UCI format."""
        legal_moves = [move.uci() for move in self.board.legal_moves]
        return legal_moves

    def get_best_move(self):
        """Use the DQN model to predict the best move."""
        state_tensor = board_to_tensor(self.board).view(1, -1)  # Add batch dimension
        with torch.no_grad():
            action_values = self.policy_net(state_tensor)
            # Sort predicted actions by Q-value
            sorted_actions = torch.argsort(action_values, descending=True).squeeze()

        # Iterate over the sorted action indices
        for idx in sorted_actions:
            predicted_move = self.index_to_uci[idx.item()]
            move = chess.Move.from_uci(predicted_move)
            if move in self.board.legal_moves:
                return idx.item()

        raise ValueError("No legal move found.")
    
    def select_action(self):
        """Selects an action based on the epsilon-greedy strategy."""
        self.steps_done += 1
        
        # Update epsilon based on decay
        self.epsilon = max(self.epsilon_end, 
                           self.epsilon_start - (self.epsilon_start - self.epsilon_end) * 
                           (self.steps_done / self.epsilon_decay))
        
        if random.random() < self.epsilon:
            # Exploration: choose a random action from the set of legal moves
            legal_moves = self.get_legal_moves()
            chosen_move = self.uci_to_index[random.choice(legal_moves)]
            # print("Exploration move:", self.index_to_uci[chosen_move])

            return chosen_move
        else:
            # Exploitation: choose the action from the set of legal moves with the highest Q-value
            chosen_move = self.get_best_move()
            # print("Exploitation move:", self.index_to_uci[chosen_move])

            return chosen_move

    def step(self):
        """Executes a move in UCI format and returns the board state and reward."""
        action = self.select_action()
        uci_move = self.index_to_uci[action]
        move = chess.Move.from_uci(uci_move)

        if move in self.board.legal_moves:
            self.board.push(move)
        else:
            raise ValueError(f"Illegal move: {uci_move}")

        done = self.board.is_game_over()
        reward = 0.0

        if self.board.is_checkmate():
            reward = 1.0 if self.board.turn == chess.WHITE else 0.0
        elif self.board.is_stalemate() or \
            self.board.is_insufficient_material() or \
            self.board.is_seventyfive_moves() or \
            self.board.is_fivefold_repetition():
            reward = 0.5

        return board_to_tensor(self.board), uci_move, reward, done
