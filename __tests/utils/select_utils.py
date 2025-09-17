from typing import Optional
from __tests.screen import BaseContext


class use_select_controls:
    def __init__(self, context: BaseContext, *, selector: Optional[str] = None) -> None:
        self._context = context
        self._select_box = context.page.locator(".t-select-input.t-select")
        self._select_input = self._select_box.locator("input")

    def should_value(self, value: str) -> None:
        self._context.expect(self._select_input).to_have_value(value)

    def _try_open_dropdown(self):
        if self._context.page.locator(".t-select__dropdown-inner").count() <= 0:
            self._select_box.click()

    def select_option(self, option: str):
        self._try_open_dropdown()
        self._context.page.locator(
            f'ul.t-select__list > li:has-text("{option}")'
        ).click()
