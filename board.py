from typing import Union, cast
import pieces
from chess_types import FileType, RankType, WhereType, ColourType

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
a, b, c, d, e, f, g, h = cast(list[FileType], [0, 1, 2, 3, 4, 5, 6, 7])


class ChessBoard(pieces.BaseBoard):
    def __init__(self) -> None:
        self.turn: ColourType = "w"
        self.board: list[list[Union[None, pieces.ChessPiece]]] = [
            [None] * 9 for _ in range(8)
        ]
        self.pieces = self.starting_pieces()
        self.starting_board()

    def starting_pieces(self) -> list[pieces.ChessPiece]:
        pieces_list = []
        for file in range(8):
            file = cast(FileType, file)
            pieces_list.append(STARTING_POSITIONS[file](file, 1, "w", self))
            pieces_list.append(pieces.Pawn(file, 2, "w", self))
            pieces_list.append(STARTING_POSITIONS[file](file, 8, "b", self))
            pieces_list.append(pieces.Pawn(file, 7, "b", self))
        return pieces_list

    def starting_board(self):
        for file in range(8):
            for rank in range(1, 9):
                piece_set = False
                for piece in self.pieces:
                    if piece.file == file and piece.rank == rank:
                        self.board[file][rank] = piece
                        piece_set = True
                if not piece_set:
                    self.board[file][rank] = None

    def get_pieces(
        self, where: WhereType, piece_list: list[pieces.ChessPiece]
    ) -> list[pieces.ChessPiece]:
        wanted_pieces = []
        for piece in piece_list:
            equal = (
                ((piece.colour == where["colour"]) or not where["colour"])
                and ((piece.type == where["type"]) or not where["type"])
                and ((piece.rank == where["rank"]) or not where["rank"])
                and ((piece.file == where["file"]) or not where["file"])
            )
            if equal:
                wanted_pieces.append(piece)
        return wanted_pieces

    def get_piece(
        self, where: WhereType, piece_list: list[pieces.ChessPiece]
    ) -> Union[pieces.ChessPiece, None]:
        for piece in piece_list:
            equal = (
                ((piece.colour == where["colour"]) or not where["colour"])
                and ((piece.type == where["type"]) or not where["type"])
                and ((piece.rank == where["rank"]) or not where["rank"])
                and ((piece.file == where["file"]) or not where["file"])
            )
            if equal:
                return piece

    def is_check(
        self,
        colour: ColourType,
        move: Union[tuple[pieces.ChessPiece, FileType, RankType], None] = None,
    ) -> bool:
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
            self.get_piece(
                {"colour": colour, "type": "K", "rank": None, "file": None},
                other.pieces,
            ),
        )
        for piece in self.get_pieces(
            {
                "colour": "b" if colour == "w" else "w",
                "type": None,
                "rank": None,
                "file": None,
            },
            other.pieces,
        ):
            allowed = piece.allowed_moves(check=False)
            if (king.file, king.rank) in allowed:
                return True
        return False

    def copy(self):
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
