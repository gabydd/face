import abc
from typing import Any, Union, cast

from chess_types import FileType, RankType, ColourType, WhereType


a, b, c, d, e, f, g, h = range(8)


class ChessPiece(abc.ABC):
    """Base class of the chess piece hierarchy.

    A chess piece has a file and a rank.
    These denote the column and row it is on respictively.
    """

    file: FileType
    rank: RankType
    colour: ColourType
    type: str
    board: Any

    @abc.abstractmethod
    def __init__(
        self,
        file: FileType,
        rank: RankType,
        colour: ColourType,
        board: Any,
    ) -> None:
        ...

    @abc.abstractmethod
    def allowed(self, file: FileType, rank: RankType, check: bool = True) -> bool:
        ...

    @abc.abstractmethod
    def allowed_moves(self, check: bool = True) -> list[tuple[FileType, RankType]]:
        ...

    @abc.abstractmethod
    def move(self, file: FileType, rank: RankType) -> bool:
        ...

    @abc.abstractmethod
    def copy(self) -> Any:
        ...


class BaseBoard(abc.ABC):
    turn: ColourType
    pieces: list[ChessPiece]
    board: list[list[Union[None, ChessPiece]]]

    @abc.abstractmethod
    def __init__(self) -> None:
        ...

    @abc.abstractmethod
    def starting_board(self):
        ...

    @abc.abstractmethod
    def get_pieces(
        self, where: WhereType, piece_list: list[ChessPiece]
    ) -> list[ChessPiece]:
        ...

    @abc.abstractmethod
    def get_piece(
        self, where: WhereType, piece_list: list[ChessPiece]
    ) -> Union[ChessPiece, None]:
        ...

    @abc.abstractmethod
    def is_check(
        self,
        colour: ColourType,
        move: Union[tuple[ChessPiece, FileType, RankType], None] = None,
    ) -> bool:
        ...


class Rook(ChessPiece):
    def __init__(
        self,
        file: FileType,
        rank: RankType,
        colour: ColourType,
        board: BaseBoard,
    ) -> None:
        self.file = file
        self.rank = rank
        self.colour = colour
        self.type = "R"
        self.board: BaseBoard = board

    def allowed(self, file: FileType, rank: RankType, check: bool = True) -> bool:
        ...

    def allowed_moves(self, check: bool = True) -> list[tuple[FileType, RankType]]:
        return []

    def move(self, file: FileType, rank: RankType) -> bool:
        moved = False
        return moved

    def copy(self):

        return Rook(self.file, self.rank, self.colour, self.board)


class Knight(ChessPiece):
    """The knight piece skips over any other piece when moving.
        It can move in these possible ways:
          file-1,rank+2   file+1,rank+2
                      F N F
    file-2,rank+1   F N N N F file+2,rank+1
                    N N S N N
    file-2,rank-1   F N N N F file+2,rank-1
                      F N F
          file-1,rank-2   file+1,rank-2"""

    def __init__(
        self,
        file: FileType,
        rank: RankType,
        colour: ColourType,
        board: BaseBoard,
    ) -> None:
        self.file = file
        self.rank = rank
        self.colour = colour
        self.type = "N"
        self.board: BaseBoard = board

    def allowed(self, file: int, rank: int, check: bool = True) -> bool:
        on_board = a <= file <= h and 1 <= rank <= 8
        on_square = on_board and self.board.board[file][rank]
        valid_move = False
        not_own_colour = True if not on_square else on_square.colour != self.colour
        not_check = True
        if check and on_board:
            not_check = not self.board.is_check(
                self.colour, (self, cast(FileType, file), cast(RankType, rank))
            )
        for file_mod, rank_mods in (
            (-2, (-1, 1)),
            (2, (-1, 1)),
            (-1, (-2, 2)),
            (1, (-2, 2)),
        ):
            for rank_mod in rank_mods:
                if self.file + file_mod == file and self.rank + rank_mod == rank:
                    valid_move = True
        return valid_move and on_board and not_own_colour and not_check

    def allowed_moves(self, check: bool = True) -> list[tuple[FileType, RankType]]:
        moves = []
        for file_mod, rank_mods in (
            (-2, (-1, 1)),
            (2, (-1, 1)),
            (-1, (-2, 2)),
            (1, (-2, 2)),
        ):
            for rank_mod in rank_mods:
                allowed = self.allowed(
                    self.file + file_mod, self.rank + rank_mod, check=check
                )
                if allowed:
                    moves.append((self.file + file_mod, self.rank + rank_mod))

        return cast(list[tuple[FileType, RankType]], moves)

    def move(self, file: FileType, rank: RankType) -> bool:
        moved = False
        if (file, rank) in self.allowed_moves() and self.board.turn == self.colour:
            self.board.board[self.file][self.rank] = None
            in_spot = self.board.board[file][rank]
            if type(in_spot) == ChessPiece:
                del in_spot
            self.board.board[file][rank] = self
            self.board.turn = "b" if self.colour == "w" else self.colour

        return moved

    def copy(self):
        return Knight(self.file, self.rank, self.colour, self.board)


class Bishop(ChessPiece):
    def __init__(
        self,
        file: FileType,
        rank: RankType,
        colour: ColourType,
        board: BaseBoard,
    ) -> None:
        self.file = file
        self.rank = rank
        self.colour = colour
        self.type = "B"
        self.board: BaseBoard = board

    def allowed(self, file: FileType, rank: RankType, check: bool = True) -> bool:
        ...

    def allowed_moves(self, check: bool = True) -> list[tuple[FileType, RankType]]:
        return []

    def move(self, file: FileType, rank: RankType) -> bool:
        moved = False
        return moved

    def copy(self):
        return Bishop(self.file, self.rank, self.colour, self.board)


class Queen(ChessPiece):
    def __init__(
        self,
        file: FileType,
        rank: RankType,
        colour: ColourType,
        board: BaseBoard,
    ) -> None:
        self.file = file
        self.rank = rank
        self.colour = colour
        self.type = "Q"
        self.board: BaseBoard = board

    def allowed(self, file: FileType, rank: RankType, check: bool = True) -> bool:
        ...

    def allowed_moves(self, check: bool = True) -> list[tuple[FileType, RankType]]:
        return []

    def move(self, file: FileType, rank: RankType) -> bool:
        moved = False
        return moved

    def copy(self):
        return Queen(self.file, self.rank, self.colour, self.board)


class King(ChessPiece):
    def __init__(
        self,
        file: FileType,
        rank: RankType,
        colour: ColourType,
        board: BaseBoard,
    ) -> None:
        self.file = file
        self.rank = rank
        self.colour = colour
        self.type = "K"
        self.board: BaseBoard = board

    def allowed(self, file: FileType, rank: RankType, check: bool = True) -> bool:
        ...

    def allowed_moves(self, check: bool = True) -> list[tuple[FileType, RankType]]:
        return []

    def move(self, file: FileType, rank: RankType) -> bool:
        moved = False
        return moved

    def copy(self):

        return King(self.file, self.rank, self.colour, self.board)


class Pawn(ChessPiece):
    def __init__(
        self,
        file: FileType,
        rank: RankType,
        colour: ColourType,
        board: BaseBoard,
    ) -> None:
        self.file = file
        self.rank = rank
        self.colour = colour
        self.type = "P"
        self.board: BaseBoard = board

    def allowed(self, file: FileType, rank: RankType, check: bool = True) -> bool:
        ...

    def allowed_moves(self, check: bool = True) -> list[tuple[FileType, RankType]]:
        return []

    def move(self, file: FileType, rank: RankType) -> bool:
        moved = False
        return moved

    def copy(self):
        return Pawn(self.file, self.rank, self.colour, self.board)
