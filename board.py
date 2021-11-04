import pieces
from basicboard import BasicChessBoard
from typing import Union
from chess_types import WhereType

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
            pieces_list.append(pieces.Pawn(letter, "2", "white"))
            pieces_list.append(STARTING_POSITIONS[letter](letter, "8", "black"))
            pieces_list.append(pieces.Pawn(letter, "7", "black"))
        return pieces_list

    def starting_board(self):
        for letter in letters:
            for i in range(1, 9):
                piece_set = False
                for piece in self.pieces:
                    if piece.file == letter and piece.rank == str(i):
                        self.__setattr__(letter + str(i), piece)
                        piece_set = True
                if not piece_set:
                    self.__setattr__(letter + str(i), None)

    def get_pieces(
        self, where: WhereType, piece_is: pieces.ChessPiece = None
    ) -> list[pieces.ChessPiece]:
        wanted_pieces = []
        for piece in self.pieces:
            equal = piece == piece_is or (
                ((piece.colour == where["colour"]) or not where["colour"])
                and ((piece.type == where["type"]) or not where["type"])
                and ((piece.rank == where["rank"]) or not where["rank"])
                and ((piece.file == where["file"]) or not where["file"])
            )
            if equal:
                wanted_pieces.append(piece)
        return wanted_pieces
