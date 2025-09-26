from typing import Literal, Optional
from __tests.screen import BaseContext


class use_table_controls:
    def __init__(self, context: BaseContext, *, selector: Optional[str] = None) -> None:
        self._context = context
        self._table = (
            context.page.get_by_role("table")
            if selector is None
            else context.page.locator(selector)
        )

    def click_sort_icon_for_column(
        self, column_key: str, *, order: Literal["asc", "desc"] = "asc"
    ):
        self._table.locator(
            f'thead th[data-colkey="{column_key}"] .t-table-sort-{order}'
        ).click()

    def should_row_values(self, row_index: int, values: list[str]):
        row = self._table.locator("tbody tr").nth(row_index).locator("td")
        self._context.expect(row).to_have_text(values)
