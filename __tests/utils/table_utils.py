from typing import Literal, Optional
from __tests.screen import BaseContext


class use_table_controls:
    def __init__(self, context: BaseContext, *, selector: Optional[str] = None) -> None:
        self._context = context
        self._table = context.page.locator(selector or ".t-table")

    def click_sort_icon_for_column(
        self, column_key: str, *, order: Literal["asc", "desc"] = "asc"
    ):
        self._table.locator(
            f'thead th[data-colkey="{column_key}"] .t-table-sort-{order}'
        ).click()
        return self

    def click_filter_icon_for_column(self, column_key: str):
        self._table.locator(
            f'thead th[data-colkey="{column_key}"] .t-table__filter-icon'
        ).click()
        return self

    def fill_input_filter_popup(self, text: str):
        self._table.locator(".t-table__filter-pop").get_by_role("textbox").fill(text)
        return self

    def click_filter_popup(self, text: str):
        self._table.locator(".t-table__filter-pop").get_by_text(text).click()
        return self

    def click_confirm_filter_popup(self):
        self._table.locator(".t-table__filter-pop").get_by_text("Confirm").click()
        return self

    def click_reset_filter_popup(self):
        self._table.locator(".t-table__filter-pop").get_by_text("Reset").click()
        return self

    def click_filter_clear_button(self):
        self._table.locator(".t-table__row-filter-inner").get_by_text("Clear").click()
        return self

    def should_row_values(self, row_index: int, values: list[str]):
        row = self._table.locator("tbody tr").nth(row_index).locator("td")
        self._context.expect(row).to_have_text(values)

    def should_rows_count(self, count: int):
        rows = self._table.locator("tbody tr")
        self._context.expect(rows).to_have_count(count)
