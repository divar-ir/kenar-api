from enum import Enum

from pydantic import BaseModel


class TextType(Enum):
    PRIMARY = 1
    SECONDARY = 2
    TERTIARY = 3


class Color(Enum):
    UNKNOWN = 0
    BRAND_PRIMARY = 1
    BRAND_SECONDARY = 2
    BRAND_HINT = 3
    BRAND_DIVIDER = 4
    SUCCESS_PRIMARY = 5
    SUCCESS_SECONDARY = 6
    WARNING_PRIMARY = 7
    WARNING_SECONDARY = 8
    ERROR_PRIMARY = 9
    MESSAGE_PRIMARY = 10
    MESSAGE_HINT = 11
    TEXT_PRIMARY = 12
    TEXT_SECONDARY = 13
    TEXT_HINT = 14
    TEXT_DIVIDER = 15
    ICON_PRIMARY = 16
    ICON_SECONDARY = 17
    ICON_HINT = 18
    ICON_DIVIDER = 19
    TRANSPARENT = 20
    GREY_50 = 21
    GREY_100 = 22
    GREY_200 = 23
    GREY_400 = 24
    GREY_700 = 25
    GREY_800 = 26
    GREY_850 = 27
    GREY_900 = 28
    WHITE_PRIMARY = 29
    WHITE_SECONDARY = 30
    WHITE_HINT = 31
    WHITE_DIVIDER = 32
    BLACK = 33
    BLACK_PRIMARY = 34
    BLACK_SECONDARY = 35
    BLACK_HINT = 36
    BLACK_DIVIDER = 37


class TitleRow(BaseModel):
    text: str
    text_type: TextType
    text_color: Color
    description: str
    subtitle: str
    subtitle_color: Color
