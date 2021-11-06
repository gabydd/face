from typing import Union, cast
import copy

import pieces
from chess_types import BoardList, FileType, RankType, WhereType, ColourType

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
letters = ("a", "b", "c", "d", "e", "f", "g", "h")
a, b, c, d, e, f, g, h = range(8)

class ChessBoard:
    def __init__(self) -> None:
        self.turn: ColourType = "w"
        self.board: BoardList = [[None] * 9 for _ in range(8)]
        self.pieces = self.starting_pieces()
        self.starting_board()

    def starting_pieces(self) -> list[pieces.ChessPiece]:
        pieces_list = []
        for file in range(9):
            file = cast(FileType, file)
            pieces_list.append(STARTING_POSITIONS[file](file, 1, "w", self))
            pieces_list.append(pieces.Pawn(file, 2, "w", self))
            pieces_list.append(STARTING_POSITIONS[file](file, 8, "b", self))
            pieces_list.append(pieces.Pawn(file, 7, "b", self))
        return pieces_list

    def starting_board(self):
        for file in range(9):
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
    ):
        if move:
            board = self.board.copy()
            board[move[0].file][move[0].rank] = None
            piece = copy.deepcopy(move[0])
            piece.file = move[1]
            piece.rank = move[2]
            board[move[1]][move[2]] = piece
            pieces_ = copy.deepcopy(self.pieces)
            for p in pieces_:
                if p.file == move[0].file and p.rank == move[0].rank:
                    pieces_[pieces_.index(p)] = piece

        else:
            board = self.board.copy()
            pieces_ = copy.deepcopy(self.pieces)
        king = cast(
            pieces.King,
            self.get_piece(
                {"colour": colour, "type": "K", "rank": None, "file": None}, pieces_
            ),
        )
        for piece in self.get_pieces(
            {
                "colour": colour if colour == "w" else "b",
                "type": None,
                "rank": None,
                "file": None,
            },
            pieces_,
        ):
            if (king.rank, king.file) in piece.allowed_moves(check=False):
                return True


board = ChessBoard()
piece = board.board[a][3]
if piece:
    board.board[a][4] = piece
    board.board[piece.file][piece.rank] = None
    piece.rank = 4
