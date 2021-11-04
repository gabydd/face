from typing import Literal


class ChessPiece:
    """Base class of the chess piece hierarchy.

    A chess piece has a file and a rank.
    These denote the column and row it is on respictively.
    """

    def __init__(
        self, file: str, rank: str, colour: Literal["white", "black"], type: str
    ) -> None:
        self.file = file
        self.rank = rank
        self.colour = colour
        self.type = type


class Rook(ChessPiece):
    def __init__(self, file: str, rank: str, colour: Literal["white", "black"]) -> None:
        super().__init__(file, rank, colour, "R")


class Knight(ChessPiece):
    def __init__(self, file: str, rank: str, colour: Literal["white", "black"]) -> None:
        super().__init__(file, rank, colour, "N")


class Bishop(ChessPiece):
    def __init__(self, file: str, rank: str, colour: Literal["white", "black"]) -> None:
        super().__init__(file, rank, colour, "B")


class Queen(ChessPiece):
    def __init__(self, file: str, rank: str, colour: Literal["white", "black"]) -> None:
        super().__init__(file, rank, colour, "Q")


class King(ChessPiece):
    def __init__(self, file: str, rank: str, colour: Literal["white", "black"]) -> None:
        super().__init__(file, rank, colour, "K")


class Pawn(ChessPiece):
    def __init__(self, file: str, rank: str, colour: Literal["white", "black"]) -> None:
        super().__init__(file, rank, colour, "P")
