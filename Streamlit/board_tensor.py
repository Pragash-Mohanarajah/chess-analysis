import chess
import torch

# Piece types for both sides
piece_to_index = {
    chess.PAWN: 0,
    chess.KNIGHT: 1,
    chess.BISHOP: 2,
    chess.ROOK: 3,
    chess.QUEEN: 4,
    chess.KING: 5
}

def board_to_tensor(board):
    """
    Convert the chess board to a PyTorch tensor.
    """
    tensor = torch.zeros(12, 8, 8)  # 12 channels, 8x8 board
    
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece is not None:
            row, col = divmod(square, 8)
            piece_type = piece_to_index[piece.piece_type]
            
            # White pieces occupy first 6 channels, black pieces next 6
            if piece.color == chess.WHITE:
                tensor[piece_type, row, col] = 1
            else:
                tensor[piece_type + 6, row, col] = 1
    
    return tensor

# Create a board and convert it to a tensor
board = chess.Board()
state_tensor = board_to_tensor(board)
# print("Tensor Shape: ", state_tensor.shape)  # Should be [12, 8, 8]
# print("Number of Pieces", state_tensor.sum())  # Should be 32