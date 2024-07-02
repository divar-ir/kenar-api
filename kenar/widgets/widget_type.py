from typing import Optional, Type, Union

from kenar.widgets.description_row import DescriptionRow
from kenar.widgets.evaluation_row import EvaluationRow
from kenar.widgets.event_row import EventRow
from kenar.widgets.group_info_row import GroupInfo
from kenar.widgets.legend_title_row import LegendTitleRow
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
    LegendTitleRow,
    ScoreRow,
    SelectorRow,
    SubtitleRow,
    TitleRow,
    WideButtonBar,
]


def get_widget_class(widget_type: str) -> Optional[Type[WidgetTypesUnion]]:
    widget_type_to_class = {
        "DESCRIPTION_ROW": DescriptionRow,
        "EVALUATION_ROW": EvaluationRow,
        "EVENT_ROW": EventRow,
        "GROUP_INFO_ROW": GroupInfo,
        "LEGEND_TITLE_ROW": LegendTitleRow,
        "SCORE_ROW": ScoreRow,
        "SELECTOR_ROW": SelectorRow,
        "SUBTITLE_ROW": SubtitleRow,
        "TITLE_ROW": TitleRow,
        "WIDE_BUTTON_BAR": WideButtonBar,
    }
    widget_class = widget_type_to_class.get(widget_type)
    if not widget_class:
        raise ValueError(f"Unsupported widget_type {widget_type}")
    return widget_class
