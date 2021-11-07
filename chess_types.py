from typing import Literal, TypedDict, Union

File = Literal[0, 1, 2, 3, 4, 5, 6, 7]
Rank = Literal[1, 2, 3, 4, 5, 6, 7, 8]
ColourString = Literal["w", "b"]
SymbolString = Literal["R", "N", "B", "Q", "K", "P"]
WhereType = TypedDict(
    "WhereType",
    {
        "colour": Union[None, ColourString],
        "symbol": Union[None, SymbolString],
        "file": Union[None, File],
        "rank": Union[None, Rank],
    },
)
