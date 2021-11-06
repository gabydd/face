from typing import Literal, TypedDict, Union

FileType = Literal[0, 1, 2, 3, 4, 5, 6, 7]
RankType = Literal[1, 2, 3, 4, 5, 6, 7, 8]
ColourType = Literal["w", "b"]
WhereType = TypedDict(
    "WhereType",
    {
        "colour": Union[None, ColourType],
        "type": Union[None, str],
        "rank": Union[None, FileType],
        "file": Union[None, FileType],
    },
)
