import torch
import chess
from network import DQN  # Your neural network architecture
from all_moves import index_to_uci, uci_to_index
from chess_env import ChessEnvironment
import streamlit as st

class ChessEngine:
    """
    Chess engine that uses a trained DQN model to select the best move.
    
    Attributes:
    input_size (int): The input size of the neural network.
    n_actions (int): The total number of possible actions.
    policy_net (torch.nn.Module): The trained neural network for selecting moves.
    env (ChessEnvironment): The environment for the chess board.
    
    Methods:
    get_best_move(fen): Get the best move for the given chess board position.
    get_best_move_from_board(board): Get the best move for the given chess board.
    make_move(board, best_move): Make the best move on the provided board.
    
    Usage:
    engine = ChessEngine()
    board = chess.Board()  # Initialize the board to the starting position or any FEN position
    best_move = engine.get_best_move_from_board(board)
    print(f"Best move: {best_move}")
    board = engine.make_move(board, best_move)
    print("Board after making the move:")
    print(board)

    # Output
    # Best move: e2e4
    # Board after making the move:
    # r n b q k b n r
    # p p p p p p p p
    # . . . . . . . .
    # . . . . . . . .
    # . . . . P . . .
    # . . . . . . . .
    # P P P P . P P P
    # R N B Q K B N R
    """
    def __init__(self):
        self.input_size = 768 # As defined in training: 12 planes of 8x8
        self.n_actions = len(index_to_uci)  # Total number of possible actions (e.g., 4672 moves)
        self.policy_net = DQN(self.input_size, self.n_actions)
        self.policy_net.load_state_dict(torch.load("trained_chess_agent.pth"))
        self.policy_net.eval()
        self.env = ChessEnvironment(self.policy_net, index_to_uci, uci_to_index)

    def get_best_move(self, fen):
        """
        Get the best move for the given chess board using the trained policy_net.
        
        Parameters:
        fen (str): The FEN notation of the current chess board position.
        
        Returns:
        str: The best move in UCI format.
        """
        # Set up the board with the provided FEN
        self.env.board.set_fen(fen)
        
        # Get the best move from the trained model
        best_move = self.env.get_best_move()
        
        return best_move
    
    def get_best_move_from_board(self, board):
        """
        Get the best move for the given chess board using the trained policy_net.
        
        Parameters:
        board (chess.Board): The current chess board position.
        
        Returns:
        str: The best move in UCI format.
        """
        # Get the best move from the trained model
        state = self.env.get_state(board)  # Ensure this returns a tensor of shape (1, 768)
        
        # Convert state to a torch tensor (if not already)
        state_tensor = torch.tensor(state, dtype=torch.float).view(1, -1)  # Ensure (1, 768) shape

        # Pass the state through the policy network to get Q-values
        with torch.no_grad():  # No gradient calculation needed for inference
            q_values = self.policy_net(state_tensor)
        
        # Select the action with the highest Q-value
        best_action_index = torch.argmax(q_values).item()  # Get the index of the best action
        
        # Convert the index back to a UCI move
        best_move_uci = index_to_uci[best_action_index]
        
        return best_move_uci
    
    def make_move(self, board, best_move):
        """
        Make the best move on the provided board.
        
        Parameters:
        board (chess.Board): The current chess board position.
        best_move (str): The best move in UCI format.
        
        Returns:
        chess.Board: The updated board after making the move.
        """
        move = chess.Move.from_uci(best_move)
        if move in board.legal_moves:
            board.push(move)
            return board
        else:
            st.write("Move is not legal")
            return board
        
st.set_page_config(page_title='Chess Engine', page_icon='♟', layout="wide")
st.title("Chess Engine")

engine = ChessEngine()

# Fetch the FEN from the query parameter (GET request)
query_params = st.experimental_get_query_params()
fen_from_query = query_params.get("fen", [None])[0].replace("_", " ").replace("%2F", "/") if query_params.get("fen", [None])[0] else None

# Add a text input for the FEN string (as fallback or if the query param isn't available)
fen_input = st.text_input("Enter FEN:", value=fen_from_query or chess.Board().fen())

# If a FEN string is provided, create a new board from it
if fen_input:
    try:
        board = chess.Board(fen_input)
        best_move = engine.get_best_move_from_board(board)
        st.experimental_set_query_params(best_move=best_move)
        st.write(f"Best move: {best_move}")
        board = engine.make_move(board, best_move)
        st.write("Board after making the move:")
        st.write(board)
    except ValueError:
        st.error("Invalid FEN string. Please enter a valid FEN.")
else:
    st.write("Please enter a FEN string to get the best move.")
