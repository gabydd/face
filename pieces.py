from __future__ import annotations
import abc
from typing import Any, Union, cast


from chess_types import File, Rank, ColourString, WhereType, SymbolString

a, b, c, d, e, f, g, h = range(8)
KNIGHT_MOVES = (
    (-2, (-1, 1)),
    (2, (-1, 1)),
    (-1, (-2, 2)),
    (1, (-2, 2)),
)


class ChessPiece(abc.ABC):
    """Base class of the chess piece hierarchy.

    A chess piece has a file and a rank.
    These denote the column and row it is on respictively.
    """

    file: File
    rank: Rank
    colour: ColourString
    symbol: SymbolString
    board: BaseBoard

    @abc.abstractmethod
    def __init__(
        self,
        file: File,
        rank: Rank,
        colour: ColourString,
        board: Any,
    ) -> None:
        ...

    @abc.abstractmethod
    def allowed(self, file: File, rank: Rank, check: bool = True) -> bool:
        """Return if the file and rank provided is an allowed move for the piece.

        Because this method calls the ChessBoard.is_check method,
        which indirectly calls this method again.
        ChessBoard.is_check will not be called if the "check" paramater is false.
        This means moves that result in a check on your king will be allowed if "check" is false.
        """
        ...

    @abc.abstractmethod
    def allowed_moves(self, check: bool = True) -> list[tuple[File, Rank]]:
        """Return all the allowed moves for this piece in a list of tuples containing the file and rank.

        Because this method inderectly calls the ChessBoard.is_check method,
        which calls this method again.
        ChessBoard.is_check will not be called if the "check" paramater is false.
        This means moves that result in a check on your king will be added to the list if "check" is false.
        """
        ...

    @abc.abstractmethod
    def move(self, file: File, rank: Rank) -> bool:
        """Try and move this piece to a specified file and rank, return if it was moved or not.

        The piece will only be moved if it is it's turn and the move is allowed.
        If it is moved the turn attribute on it's board will be switched to the opponent.
        """
        ...

    @abc.abstractmethod
    def copy(self) -> ChessPiece:
        """Return a copy of this instance of ChessPiece.

        The board attribute on the chess piece should be changed to a copy.
        """
        ...


class BaseBoard(abc.ABC):
    turn: ColourString
    checkmate: bool
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
        colour: ColourString,
        move: Union[tuple[ChessPiece, File, Rank], None] = None,
    ) -> bool:
        ...

    @abc.abstractmethod
    def change_turn(self) -> None:
        ...


class Rook(ChessPiece):
    def __init__(
        self,
        file: File,
        rank: Rank,
        colour: ColourString,
        board: BaseBoard,
    ) -> None:
        self.file = file
        self.rank = rank
        self.colour = colour
        self.symbol = "R"
        self.board = board

    def allowed(self, file: File, rank: Rank, check: bool = True) -> bool:
        ...

    def allowed_moves(self, check: bool = True) -> list[tuple[File, Rank]]:
        return []

    def move(self, file: File, rank: Rank) -> bool:
        moved = False
        return moved

    def copy(self):

        return Rook(self.file, self.rank, self.colour, self.board)


class Knight(ChessPiece):
    """The knight piece skips over any other piece when moving.
    It can move in these possible ways:
    file-1,rank+2,
    file+1,rank+2,
    file-2,rank+1,
    file+2,rank+1,
    file-2,rank-1,
    file+2,rank-1,
    file-1,rank-2,
    file+1,rank-2"""

    def __init__(
        self,
        file: File,
        rank: Rank,
        colour: ColourString,
        board: BaseBoard,
    ) -> None:
        self.file = file
        self.rank = rank
        self.colour = colour
        self.symbol = "N"
        self.board = board

    def allowed(self, file: int, rank: int, check: bool = True) -> bool:
        on_board = a <= file <= h and 1 <= rank <= 8
        on_square = on_board and self.board.board[file][rank]
        valid_move = False
        not_own_colour = True if not on_square else on_square.colour != self.colour
        not_check = True
        for file_mod, rank_mods in KNIGHT_MOVES:
            for rank_mod in rank_mods:
                if self.file + file_mod == file and self.rank + rank_mod == rank:
                    valid_move = True
        # Make sure that check method is only called on correct moves
        if check and on_board and not_own_colour and valid_move:
            not_check = not self.board.is_check(
                self.colour, (self, cast(File, file), cast(Rank, rank))
            )
        return valid_move and on_board and not_own_colour and not_check

    def allowed_moves(self, check: bool = True) -> list[tuple[File, Rank]]:
        moves = []
        for file_mod, rank_mods in KNIGHT_MOVES:
            for rank_mod in rank_mods:
                allowed = self.allowed(
                    self.file + file_mod, self.rank + rank_mod, check=check
                )
                if allowed:
                    moves.append((self.file + file_mod, self.rank + rank_mod))

        return cast(list[tuple[File, Rank]], moves)

    def move(self, file: File, rank: Rank) -> bool:
        moved = False
        if self.allowed(file, rank) and self.board.turn == self.colour and not self.board.checkmate:
            self.board.board[self.file][self.rank] = None
            in_spot = self.board.board[file][rank]
            if type(in_spot) == ChessPiece:
                del in_spot
            self.board.board[file][rank] = self
            self.file = file
            self.rank = rank
            self.board.change_turn()

            moved = True

        return moved

    def copy(self):
        return Knight(self.file, self.rank, self.colour, self.board)


class Bishop(ChessPiece):
    def __init__(
        self,
        file: File,
        rank: Rank,
        colour: ColourString,
        board: BaseBoard,
    ) -> None:
        self.file = file
        self.rank = rank
        self.colour = colour
        self.symbol = "B"
        self.board: BaseBoard = board

    def allowed(self, file: File, rank: Rank, check: bool = True) -> bool:
        ...

    def allowed_moves(self, check: bool = True) -> list[tuple[File, Rank]]:
        return []

    def move(self, file: File, rank: Rank) -> bool:
        moved = False
        return moved

    def copy(self):
        return Bishop(self.file, self.rank, self.colour, self.board)


class Queen(ChessPiece):
    def __init__(
        self,
        file: File,
        rank: Rank,
        colour: ColourString,
        board: BaseBoard,
    ) -> None:
        self.file = file
        self.rank = rank
        self.colour = colour
        self.symbol = "Q"
        self.board = board

    def allowed(self, file: File, rank: Rank, check: bool = True) -> bool:
        ...

    def allowed_moves(self, check: bool = True) -> list[tuple[File, Rank]]:
        return []

    def move(self, file: File, rank: Rank) -> bool:
        moved = False
        return moved

    def copy(self):
        return Queen(self.file, self.rank, self.colour, self.board)


class King(ChessPiece):
    def __init__(
        self,
        file: File,
        rank: Rank,
        colour: ColourString,
        board: BaseBoard,
    ) -> None:
        self.file = file
        self.rank = rank
        self.colour = colour
        self.symbol = "K"
        self.board = board

    def allowed(self, file: File, rank: Rank, check: bool = True) -> bool:
        ...

    def allowed_moves(self, check: bool = True) -> list[tuple[File, Rank]]:
        return []

    def move(self, file: File, rank: Rank) -> bool:
        moved = False
        return moved

    def copy(self):

        return King(self.file, self.rank, self.colour, self.board)


class Pawn(ChessPiece):
    def __init__(
        self,
        file: File,
        rank: Rank,
        colour: ColourString,
        board: BaseBoard,
    ) -> None:
        self.file = file
        self.rank = rank
        self.colour = colour
        self.symbol = "P"
        self.board = board

    def allowed(self, file: File, rank: Rank, check: bool = True) -> bool:
        ...

    def allowed_moves(self, check: bool = True) -> list[tuple[File, Rank]]:
        return []

    def move(self, file: File, rank: Rank) -> bool:
        moved = False
        return moved

    def copy(self):
        return Pawn(self.file, self.rank, self.colour, self.board)
