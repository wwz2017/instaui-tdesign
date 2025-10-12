import pytest
from __tests.testing_web.context import Context
from instaui import ui
import instaui_tdesign as td
from __tests.utils.pagination_utils import use_pagination_controls
from __tests.utils.table_utils import use_table_controls


def test_table(context: Context):
    @context.register_page
    def index():
        cols = [
            {"colKey": "value", "label": "name"},
        ]
        data = ui.state(
            [
                {"value": "foo"},
                {"value": "bar"},
            ]
        )

        td.table(data, columns=cols, row_key="value")

    context.open()
    context.should_see("name")
    context.should_see("foo")


def test_table_displays_data_from_computed(context: Context):
    @context.register_page
    def index():
        @ui.computed()
        def computed_data():
            return [{"name": "foo"}, {"name": "bar"}]

        td.table(computed_data, row_key="name")

    context.open()
    context.should_see("foo")


def test_cell_slot(context: Context):
    @context.register_page
    def index():
        cols = [
            {"colKey": "name"},
        ]
        data = ui.state(
            [
                {"name": "foo"},
                {"name": "bar"},
            ]
        )

        with td.table(data, columns=cols, row_key="name").add_cell_slot("name") as slot:
            td.button(slot.param("row")["name"])

    context.open()
    context.expect(context.find("button", name="foo")).to_be_visible()


def test_update_data_with_cell_slot(context: Context):
    @context.register_page
    def index():
        cols = [
            {"colKey": "name"},
            {"colKey": "mid"},
            {"colKey": "new_value"},
        ]
        data = ui.state(
            [
                {"name": "value", "pre": "x", "mid": "foo"},
            ]
        )

        table = td.table(data, columns=cols, row_key="name", pagination=False)

        with table.add_cell_slot("new_value") as slot:
            ui.text(
                ui.str_format(
                    "{pre}-{mid}-{value}",
                    pre=slot.param("row")["pre"],
                    mid=slot.param("row")["mid"],
                    value=slot.param("row")["name"],
                )
            )

        with table.add_cell_slot("mid") as slot:
            td.input(slot.param("row")["mid"])

    context.open()
    context.should_see("x-foo-value")
    context.find("input").fill("bar")
    context.should_see("x-bar-value")


def test_header_slot(context: Context):
    @context.register_page
    def index():
        data = ui.state(
            [
                {"name": "foo"},
                {"name": "bar"},
            ]
        )

        with td.table(data, row_key="name").add_header_slot("name"):
            td.button("custom header")

    context.open()
    context.expect(context.find("button", name="custom header")).to_be_visible()


def test_pagination_as_bool(context: Context):
    @context.register_page
    def index():
        cols = [
            {"colKey": "name", "title": "name"},
        ]
        data = ui.state(
            [
                {
                    "name": f"row{i}",
                }
                for i in range(6)
            ]
        )

        td.table(
            data,
            columns=cols,
            row_key="name",
            pagination=True,
        )

    context.open()
    pagination = use_pagination_controls(context)
    pagination.select_page_size("5 / page")

    context.should_not_see("row5")
    pagination.click_next_page()
    context.should_see("row5")


def test_pagination_as_int(context: Context):
    @context.register_page
    def index():
        cols = [
            {"colKey": "name", "title": "name"},
        ]
        data = ui.state(
            [
                {
                    "name": f"row{i}",
                }
                for i in range(6)
            ]
        )

        td.table(
            data,
            row_key="name",
            columns=cols,
            pagination=5,
        )

    context.open()
    pagination = use_pagination_controls(context)

    pagination.should_page_size("5 / page")
    context.should_not_see("row5")
    pagination.click_next_page()
    context.should_see("row5")


def test_pagination_as_dict(context: Context):
    @context.register_page
    def index():
        cols = [
            {"colKey": "name", "title": "name"},
        ]
        data = ui.state(
            [
                {
                    "name": f"row{i}",
                }
                for i in range(6)
            ]
        )

        td.table(
            data,
            row_key="name",
            columns=cols,
            pagination={
                "pageSizeOptions": [
                    {"label": "1 / page", "value": 1},
                    {"label": "3 / page", "value": 3},
                    {"label": "5 / page", "value": 5},
                ],
                "defaultPageSize": 3,
            },
        )

    context.open()
    pagination = use_pagination_controls(context)

    pagination.should_page_size("3 / page")
    context.should_not_see("row3")

    pagination.select_page_size("1 / page")
    context.should_not_see("row1")
    context.should_see("row0")


def test_infer_columns_from_data(context: Context):
    @context.register_page
    def index():
        data = [
            {"name": "foo"},
        ]

        td.table(data, row_key="name")

    context.open()
    context.should_see("name")
    context.should_see("foo")


def test_default_sort(context: Context):
    @context.register_page
    def index():
        data = [{"name": "foo", "age": 1}, {"name": "bar", "age": 2}]
        td.table(data, row_key="name")

    context.open()
    table = use_table_controls(context)

    table.click_sort_icon_for_column("age", order="desc")
    table.should_row_values(0, ["bar", "2"])


def test_sorter_enabled_column_allows_sorting(context: Context):
    @context.register_page
    def index():
        data = [{"name": "foo", "age": 1}, {"name": "bar", "age": 2}]
        columns = [
            {
                "colKey": "name",
                "title": "name",
            },
            {
                "colKey": "age",
                "title": "age",
                "sorter": True,
            },
        ]
        td.table(data, columns=columns, row_key="name")

    context.open()
    table = use_table_controls(context)

    table.click_sort_icon_for_column("age", order="desc")
    table.should_row_values(0, ["bar", "2"])


class TestFilterBase:
    @classmethod
    def setup_class(cls):
        cls.data = [
            {"name": "foo", "cls": "a", "text": "name is foo, class is a"},
            {"name": "bar", "cls": "b", "text": "name is bar, class is b"},
        ]

        cls.columns = [
            {
                "colKey": "name",
                "sorter": True,
                "filter": {
                    "type": "multiple",
                },
            },
            {
                "colKey": "cls",
                "filter": {
                    "type": "single",
                },
            },
            {"colKey": "text", "filter": {"type": "input"}},
        ]

    def test_multiple_filter(self, context: Context):
        @context.register_page
        def index():
            td.table(self.data, columns=self.columns, row_key="name")

        context.open()
        table = use_table_controls(context)

        table.click_filter_icon_for_column("name")
        table.click_filter_popup("foo")
        table.should_row_values(1, ["foo", "a", "name is foo, class is a"])
        table.should_rows_count(2)

    def test_single_filter(self, context: Context):
        @context.register_page
        def index():
            td.table(self.data, columns=self.columns, row_key="name")

        context.open()
        table = use_table_controls(context)

        table.click_filter_icon_for_column("cls")
        table.click_filter_popup("a").click_confirm_filter_popup()

        table.should_row_values(1, ["foo", "a", "name is foo, class is a"])
        table.should_rows_count(2)

    def test_input_filter(self, context: Context):
        @context.register_page
        def index():
            td.table(self.data, columns=self.columns, row_key="name")

        context.open()
        table = use_table_controls(context)

        table.click_filter_icon_for_column("text")
        table.fill_input_filter_popup("is foo").click_confirm_filter_popup()

        table.should_row_values(1, ["foo", "a", "name is foo, class is a"])
        table.should_rows_count(2)

    def test_clear_filter(self, context: Context):
        @context.register_page
        def index():
            td.table(self.data, columns=self.columns, row_key="name")

        context.open()
        table = use_table_controls(context)

        table.click_filter_icon_for_column("name")
        table.click_filter_popup("bar")

        table.click_filter_clear_button()

        table.should_rows_count(2)
        table.should_row_values(0, ["foo", "a", "name is foo, class is a"])


@pytest.mark.skip(reason="not implemented yet")
def test_test_server_side_sorting(context: Context):
    @context.register_page
    def index():
        pass
