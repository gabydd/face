from typing import Union, cast
import pieces
from chess_types import File, Rank, WhereType, ColourString

STARTING_POSITIONS = (
    pieces.Rook,
    pieces.Knight,
    pieces.Bishop,
    pieces.Queen,
    pieces.King,
    pieces.Bishop,
    pieces.Knight,
    pieces.Rook,
)
a, b, c, d, e, f, g, h = cast(list[File], [0, 1, 2, 3, 4, 5, 6, 7])


class ChessBoard(pieces.BaseBoard):
    """Representation of the board of a game of chess.


    A chess board has a list "pieces" of ChessPiece's.

    As well as a nested list "board" representing the squares on board.
    The first index of the array represents the file(column).
    The second index represents the rank(row).
    The value on each square is either a ChessPiece or None.

    The "turn" attribute keeps track of which colour's turn it is.
    """

    def __init__(self) -> None:
        self.turn: ColourString = "w"
        self.checkmate = False

        #
        self.board: list[list[Union[None, pieces.ChessPiece]]] = [
            [None] * 9 for _ in range(8)
        ]
        self.pieces = self.starting_pieces()
        self.starting_board()

    def starting_pieces(self) -> list[pieces.ChessPiece]:
        """Generate a list of ChessPiece's in their starting positions."""

        pieces_list = []
        for file in range(8):
            file = cast(File, file)
            pieces_list.append(STARTING_POSITIONS[file](file, 1, "w", self))
            pieces_list.append(pieces.Pawn(file, 2, "w", self))
            pieces_list.append(STARTING_POSITIONS[file](file, 8, "b", self))
            pieces_list.append(pieces.Pawn(file, 7, "b", self))
        return pieces_list

    def starting_board(self):
        """Add all the starting pieces onto the board."""
        for file in range(8):
            for rank in range(1, 9):
                piece_set = False
                for piece in self.pieces:
                    if piece.file == file and piece.rank == rank:
                        self.board[file][rank] = piece
                        piece_set = True
                if not piece_set:
                    self.board[file][rank] = None

    def get_pieces(self, where: WhereType) -> list[pieces.ChessPiece]:
        """Return a list of pieces that have the certain attributes in the "where" dict.

        The "where" dict must have the key value pairs of:
        "colour" which is either "w", "b" or None,
        "symbol" which is a SymbolString or None,
        "file" which is a int of type File or None,
        "rank" which is a int of type Rank or None,
        """

        wanted_pieces = []
        for piece in self.pieces:
            equal = (
                ((piece.colour == where["colour"]) or not where["colour"])
                and ((piece.symbol == where["symbol"]) or not where["symbol"])
                and ((piece.file == where["file"]) or not where["file"])
                and ((piece.rank == where["rank"]) or not where["rank"])
            )
            if equal:
                wanted_pieces.append(piece)
        return wanted_pieces

    def get_piece(self, where: WhereType) -> Union[pieces.ChessPiece, None]:
        """Return a the first piece that has the certain attributes in the "where" dict.

        The "where" dict must have the key value pairs of:
        "colour" which is either "w", "b" or None,
        "symbol" which is a SymbolString or None,
        "file" which is a int of type File or None,
        "rank" which is a int of type Rank or None,
        """

        for piece in self.pieces:
            equal = (
                ((piece.colour == where["colour"]) or not where["colour"])
                and ((piece.symbol == where["symbol"]) or not where["symbol"])
                and ((piece.rank == where["rank"]) or not where["rank"])
                and ((piece.file == where["file"]) or not where["file"])
            )
            if equal:
                return piece

    def is_check(
        self,
        colour: ColourString,
        move: Union[tuple[pieces.ChessPiece, File, Rank], None] = None,
    ) -> bool:
        """Return if either the current position is check for a certain colour
        or if position is check for a specific move and colour.
        """

        other = self.copy()

        if move:
            other.board[move[0].file][move[0].rank] = None
            piece = move[0].copy()
            piece.board = other
            piece.file = move[1]
            piece.rank = move[2]
            other.board[move[1]][move[2]] = piece
            for p in other.pieces:
                if p.file == move[0].file and p.rank == move[0].rank:
                    other.pieces[other.pieces.index(p)] = piece

        king = cast(
            pieces.King,
            other.get_piece(
                {"colour": colour, "symbol": "K", "rank": None, "file": None}
            ),
        )

        opposite_pieces = other.get_pieces(
            {
                "colour": "b" if colour == "w" else "w",
                "symbol": None,
                "rank": None,
                "file": None,
            }
        )

        for piece in opposite_pieces:
            allowed = piece.allowed_moves(check=False)
            if (king.file, king.rank) in allowed:
                return True
        return False
    
    def change_turn(self) -> None:
        self.turn = "b" if self.turn == "w" else "w"
        in_check = self.is_check(self.turn)
        if in_check:
            self.checkmate = True
            for piece in self.get_pieces({"colour": self.turn, "file": None, "rank": None, "symbol": None}):
                for move in piece.allowed_moves():
                    if not self.is_check(self.turn, (piece, *move)):
                        self.checkmate = False

    def copy(self):
        """Return a copy of this instance of ChessBoard.

        Values can be changed without affecting the board it was copied from.
        """
        copy_board = ChessBoard()
        copy_board.board = [[None] * 9 for _ in range(8)]
        for piece in self.pieces:
            new_piece = piece.copy()
            new_piece.board = copy_board
            copy_board.pieces.append(new_piece)
        for piece in copy_board.pieces:
            copy_board.board[piece.file][piece.rank] = piece
        copy_board.turn = self.turn
        return copy_board

board = ChessBoard()
board.board[a][2].rank = 4
board.board[a][4] = board.board[a][2]
board.board[a][2] = None
board.board[b][1].move(*board.board[b][1].allowed_moves()[0])
board.change_turn()
print(board.board[a][1].move(b, 1))