from __future__ import annotations
import typing
from instaui.vars.types import TMaybeRef
from instaui.components.element import Element
from instaui.components.content import Content
from instaui.event.event_mixin import EventMixin


class Button(Element):
    def __init__(
        self,
        label: typing.Optional[TMaybeRef[str]] = None,
    ):
        """Create a button element.

        Args:
            text (Optional[TMaybeRef[str]], optional): _description_. Defaults to None.
        """

        super().__init__("t-button")

        if label is not None:
            with self:
                Content(label)

    def on_click(
        self,
        handler: EventMixin,
        *,
        extends: typing.Optional[typing.List] = None,
    ):
        self.on(
            "click",
            handler,
            extends=extends,
        )
        return self
