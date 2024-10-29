from typing import List, Type, Union


from kenar.widgets.description_row import DescriptionRow
from kenar.widgets.evaluation_row import EvaluationRow
from kenar.widgets.event_row import EventRow
from kenar.widgets.group_info_row import GroupInfo
from kenar.widgets.image_carousel_row import ImageCarouselRow
from kenar.widgets.score_row import ScoreRow
from kenar.widgets.selector_row import SelectorRow
from kenar.widgets.subtitle_row import SubtitleRow
from kenar.widgets.title_row import TitleRow
from kenar.widgets.wide_button_bar import WideButtonBar

WidgetTypesUnion = Union[
    DescriptionRow,
    EvaluationRow,
    EventRow,
    GroupInfo,
    ImageCarouselRow,
    ScoreRow,
    SelectorRow,
    SubtitleRow,
    TitleRow,
    WideButtonBar,
]


def get_widget_class(keys: List[str]) -> Type[WidgetTypesUnion]:
    widget_type_to_class = {
        "description_row": DescriptionRow,
        "evaluation_row": EvaluationRow,
        "event_row": EventRow,
        "group_info_row": GroupInfo,
        "score_row": ScoreRow,
        "selector_row": SelectorRow,
        "subtitle_row": SubtitleRow,
        "title_row": TitleRow,
        "button_bar": WideButtonBar,
        "image_carousel_row": ImageCarouselRow,
    }

    for  k in keys:
        if k in widget_type_to_class:
            return widget_type_to_class[k]
    raise ValueError("Unsupported widget")
