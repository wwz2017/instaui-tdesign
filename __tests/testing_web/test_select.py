from __tests.testing_web.context import Context
from instaui_tdesign import td
from instaui import ui
from __tests.utils.select_utils import use_select_controls


def test_value(context: Context):
    @context.register_page
    def index():
        value = ui.state("foo")

        td.select(["foo", "bar"], value=value)
        ui.text(ui.str_format(r"value:{}", value))

    context.open()
    select = use_select_controls(context)
    select.should_value("foo")

    select.select_option("bar")
    context.should_see("value:bar")


def test_dict_option(context: Context):
    @context.register_page
    def index():
        options = [
            {"label": "foo", "value": "value:foo"},
            {"label": "bar", "value": "value:bar"},
        ]
        value = ui.state("")

        td.select(options, value=value)
        ui.text(value)

    context.open()
    select = use_select_controls(context)
    select.select_option("foo")
    context.should_see("value:foo")


def test_value_sync_ref_with_dict_options(context: Context):
    @context.register_page
    def index():
        options = [
            {"label": "foo", "value": "x"},
            {"label": "bar", "value": "y"},
        ]
        value = ui.state("x")
        change_y = ui.js_event(outputs=[value], code="()=>`y`")

        td.button("change to y").on_click(change_y)
        td.select(options, value=value)
        ui.text(value)

    context.open()
    select = use_select_controls(context)
    select.should_value("foo")

    context.find_by_text("change to y").click()
    select.should_value("bar")
