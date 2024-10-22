import chess

def generate_uci_moves():
    """
    Generate all possible UCI moves, including promotion moves and en passant captures.
    """
    all_moves = []
    
    # Generate moves between all squares (ignores if move is legal)
    for from_square in chess.SQUARES:
        for to_square in chess.SQUARES:
            # Basic move
            if from_square != to_square:
                move = chess.Move(from_square, to_square)
                all_moves.append(move.uci())

            # Promotion moves for white pawns (if applicable)
            if chess.square_rank(from_square) == 6 and chess.square_rank(to_square) == 7:
                for promotion in ['q', 'r', 'b', 'n']:  # queen, rook, bishop, knight
                    promotion_move = chess.Move(from_square, to_square, promotion=chess.Piece.from_symbol(promotion).piece_type)
                    all_moves.append(promotion_move.uci())

            # Promotion moves for black pawns (if applicable)
            if chess.square_rank(from_square) == 1 and chess.square_rank(to_square) == 0:
                for promotion in ['q', 'r', 'b', 'n']:  # queen, rook, bishop, knight
                    promotion_move = chess.Move(from_square, to_square, promotion=chess.Piece.from_symbol(promotion).piece_type)
                    all_moves.append(promotion_move.uci())

            # En passant captures for white pawns (if applicable)
            if chess.square_rank(from_square) == 4 and chess.square_rank(to_square) == 5:
                if chess.square_file(from_square) != chess.square_file(to_square):
                    en_passant_move = chess.Move(from_square, to_square)
                    all_moves.append(en_passant_move.uci())

            # En passant captures for black pawns (if applicable)
            if chess.square_rank(from_square) == 3 and chess.square_rank(to_square) == 2:
                if chess.square_file(from_square) != chess.square_file(to_square):
                    en_passant_move = chess.Move(from_square, to_square)
                    all_moves.append(en_passant_move.uci())

    # Castling moves for white and black
    castling_moves = ['e1g1', 'e1c1', 'e8g8', 'e8c8']
    all_moves.extend(castling_moves)

    return all_moves

# Generate the list of UCI moves
uci_moves = generate_uci_moves()
index_to_uci = {index: move for index, move in enumerate(uci_moves)}
uci_to_index = {move: index for index, move in index_to_uci.items()}

# print("Number of UCI moves:", len(uci_moves))