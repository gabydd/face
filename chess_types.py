from typing import Literal, TypedDict, Union


WhereType = TypedDict(
    "WhereType",
    {
        "colour": Union[None, Literal["white", "black"]],
        "type": Union[None, str],
        "rank": Union[None, str],
        "file": Union[None, str],
    },
)
