import pieces
from basicboard import BasicChessBoard

STARTING_POSITIONS = {
    "a": pieces.Rook,
    "b": pieces.Knight,
    "c": pieces.Bishop,
    "d": pieces.Queen,
    "e": pieces.King,
    "f": pieces.Bishop,
    "g": pieces.Knight,
    "h": pieces.Rook,
}
letters = ["a", "b", "c", "d", "e", "f", "g", "h"]


class ChessBoard(BasicChessBoard):
    def __init__(self) -> None:
        self.pieces = self.starting_pieces()
        self.starting_board()

    def starting_pieces(self) -> list[pieces.ChessPiece]:
        pieces_list = []
        for letter in letters:
            pieces_list.append(STARTING_POSITIONS[letter](letter, "1", "white"))
            pieces_list.append(STARTING_POSITIONS[letter](letter, "8", "black"))
        return pieces_list
    def starting_board(self):
        for letter in letters:
            for i in range(1,9):
                piece_set = False
                for piece in self.pieces:
                    if piece.file == letter and piece.rank == str(i):
                        self.__setattr__(letter + str(i), piece)
                        piece_set = True
                if not piece_set:
                    self.__setattr__(letter + str(i), None)