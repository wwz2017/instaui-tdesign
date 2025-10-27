from typing import Optional
from __tests.screen import BaseContext


SWITCH_BOX_SELECTOR = ".t-switch"


class use_switch_controls:
    def __init__(self, context: BaseContext, *, selector: Optional[str] = None) -> None:
        self._context = context
        self._switch_box = context.page.locator(
            SWITCH_BOX_SELECTOR
            if selector is None
            else f"{selector} {SWITCH_BOX_SELECTOR}"
        )

    def should_value(self, value: bool) -> None:
        ep = self._context.expect(self._switch_box)
        if value:
            ep.to_have_class("t-is-checked")
        else:
            ep.not_to_have_class("t-is-checked")

    def click(self):
        self._switch_box.click()
