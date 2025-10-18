from typing import Optional
from __tests.screen import BaseContext


class use_input_controls:
    def __init__(self, context: BaseContext, *, selector: Optional[str] = None) -> None:
        self._context = context
        selector = selector or ".t-input__wrap"
        self._input_box = context.page.locator(rf"{selector} .t-input")
        self._input = self._input_box.locator("input")

    def should_placeholder(self, text: str) -> None:
        self._context.expect(self._input).to_have_attribute("placeholder", text)
