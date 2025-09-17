from typing import Optional
from __tests.screen import BaseContext


class use_pagination_controls:
    def __init__(
        self, context: BaseContext, *, container_selector: Optional[str] = None
    ) -> None:
        self.context = context
        self.container_locator = context.page.locator(
            f"css={container_selector or ''} .t-table__pagination-wrap"
        )

        self._page_size_locator = self.container_locator.locator("css=.t-select-input")

    def select_page_size(self, item: str) -> None:
        self._page_size_locator.click()
        self.context.find("listitem", name=item).click()

    def click_next_page(self):
        self.container_locator.locator("css=.t-pagination__btn-next").click()

    def click_prev_page(self):
        self.container_locator.locator("css=.t-pagination__btn-prev").click()

    def should_page_size(self, value: str):
        input = self._page_size_locator.locator("css=input")
        self.context.expect(input).to_have_value(value)
