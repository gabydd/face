import abc
from typing import Literal, cast

import board
from chess_types import FileType, RankType, ColourType


a, b, c, d, e, f, g, h = range(8)

class ChessPiece(abc.ABC):
    """Base class of the chess piece hierarchy.

    A chess piece has a file and a rank.
    These denote the column and row it is on respictively.
    """

    def __init__(
        self,
        file: FileType,
        rank: RankType,
        colour: ColourType,
        type: str,
        board: board.ChessBoard,
    ) -> None:
        self.file = file
        self.rank = rank
        self.colour = colour
        self.type = type
        self.board = board

    @abc.abstractmethod
    def allowed(self, file: FileType, rank: RankType, check: bool = True) -> bool:
        ...

    @abc.abstractmethod
    def allowed_moves(self, check: bool = True) -> list[tuple[FileType, RankType]]:
        ...

    @abc.abstractmethod
    def move(self, file: FileType, rank: RankType) -> bool:
        ...


class Rook(ChessPiece):
    def __init__(
        self,
        file: FileType,
        rank: RankType,
        colour: ColourType,
        board: board.ChessBoard,
    ) -> None:
        super().__init__(file, rank, colour, "R", board)
    def allowed(self, file: FileType, rank: RankType, check: bool = True) -> bool:
        ...

    def allowed_moves(self, check: bool = True) -> list[tuple[FileType, RankType]]:
        return []

    def move(self, file: FileType, rank: RankType) -> bool:
        moved = False
        return moved


class Knight(ChessPiece):
    def __init__(
        self,
        file: FileType,
        rank: RankType,
        colour: ColourType,
        board: board.ChessBoard,
    ) -> None:
        super().__init__(file, rank, colour, "N", board)
    def allowed(self, file: FileType, rank: RankType, check: bool = True) -> bool:
        on_square = self.board.board[file][rank]
        valid_move = True
        on_board = a <= file <= h and 1 <= rank <= rank
        not_own_colour = True if not on_square else on_square.colour != self.colour
        not_check = True
        if check:
            self.board.is_check(cast(ColourType, self.colour), (self,file, rank))
        return valid_move and on_board and not_own_colour and not_check

    def allowed_moves(self, check: bool = True) -> list[tuple[FileType, RankType]]:
        return []

    def move(self, file: FileType, rank: RankType) -> bool:
        moved = False
        if (file, rank) in self.allowed_moves():
            self.board.board[self.file][self.rank] = None
            in_spot = self.board.board[file][rank]
            if type(in_spot) == ChessPiece:
                del in_spot
            self.board.board[file][rank] = self

        return moved


class Bishop(ChessPiece):
    def __init__(
        self,
        file: FileType,
        rank: RankType,
        colour: ColourType,
        board: board.ChessBoard,
    ) -> None:
        super().__init__(file, rank, colour, "B", board)
    def allowed(self, file: FileType, rank: RankType, check: bool = True) -> bool:
        ...

    def allowed_moves(self, check: bool = True) -> list[tuple[FileType, RankType]]:
        return []

    def move(self, file: FileType, rank: RankType) -> bool:
        moved = False
        return moved


class Queen(ChessPiece):
    def __init__(
        self,
        file: FileType,
        rank: RankType,
        colour: ColourType,
        board: board.ChessBoard,
    ) -> None:
        super().__init__(file, rank, colour, "Q", board)
    def allowed(self, file: FileType, rank: RankType, check: bool = True) -> bool:
        ...

    def allowed_moves(self, check: bool = True) -> list[tuple[FileType, RankType]]:
        return []

    def move(self, file: FileType, rank: RankType) -> bool:
        moved = False
        return moved


class King(ChessPiece):
    def __init__(
        self,
        file: FileType,
        rank: RankType,
        colour: ColourType,
        board: board.ChessBoard,
    ) -> None:
        super().__init__(file, rank, colour, "K", board)
    def allowed(self, file: FileType, rank: RankType, check: bool = True) -> bool:
        ...

    def allowed_moves(self, check: bool = True) -> list[tuple[FileType, RankType]]:
        return []

    def move(self, file: FileType, rank: RankType) -> bool:
        moved = False
        return moved


class Pawn(ChessPiece):
    def __init__(
        self,
        file: FileType,
        rank: RankType,
        colour: ColourType,
        board: board.ChessBoard,
    ) -> None:
        super().__init__(file, rank, colour, "P", board)
    def allowed(self, file: FileType, rank: RankType, check: bool = True) -> bool:
        ...

    def allowed_moves(self, check: bool = True) -> list[tuple[FileType, RankType]]:
        return []

    def move(self, file: FileType, rank: RankType) -> bool:
        moved = False
        return moved
