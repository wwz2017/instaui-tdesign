import re
from typing import Optional
from __tests.screen import BaseContext


GRAIO_GROUP_SELECTOR = ".t-radio-group"


class use_radio_group_controls:
    def __init__(self, context: BaseContext, *, selector: Optional[str] = None) -> None:
        self._context = context
        selector = (
            f"{GRAIO_GROUP_SELECTOR}{selector}" if selector else GRAIO_GROUP_SELECTOR
        )
        self._radio_group = context.page.locator(selector)

    def should_checked(self, value: str) -> None:
        item = self._radio_group.locator("label.t-is-checked input")

        self._context.expect(item).to_have_value(re.compile(f"^{value}$"))

    def should_nothing_checked(self) -> None:
        item = self._radio_group.locator("label.t-is-checked input")
        self._context.expect(item).to_have_count(0)

    def click(self, value: str):
        self._radio_group.locator(
            "label.t-radio", has_text=re.compile(f"^{value}$")
        ).click()
