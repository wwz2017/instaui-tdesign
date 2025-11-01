from __future__ import annotations
import typing
from ._base_element import BaseElement
from typing_extensions import TypedDict, Unpack
from ._utils import handle_props


class Descriptions(BaseElement):
    def __init__(
        self,
        **kwargs: Unpack[TDescriptionsProps],
    ):
        super().__init__("t-descriptions")
        self.props(handle_props(kwargs))  # type: ignore


class DescriptionsItem(BaseElement):
    def __init__(
        self,
        content: typing.Optional[str] = None,
        **kwargs: Unpack[TDescriptionsItemProps],
    ):
        super().__init__("t-descriptions-item")
        self.props({"content": content})
        self.props(handle_props(kwargs))  # type: ignore


class TDescriptionsProps(TypedDict, total=False):
    bordered: bool
    colon: bool
    column: int
    content_style: typing.Dict
    item_layout: typing.Literal["horizontal", "vertical"]
    items: typing.List
    label_style: typing.Dict
    layout: typing.Literal["horizontal", "vertical"]
    size: typing.Literal["small", "medium", "large"]
    table_layout: typing.Literal["fixed", "auto"]
    title: str


class TDescriptionsItemProps(TypedDict, total=False):
    label: str
    span: int
