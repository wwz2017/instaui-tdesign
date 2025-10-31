from __tests.testing_web.context import Context
from instaui_tdesign import td
from instaui import ui
from __tests.utils.radio_group_utils import use_radio_group_controls


def test_list_options(context: Context):
    @context.register_page
    def index():
        value = ui.state("foo")

        td.radio_group(["foo", "bar"], value=value)
        ui.text(ui.str_format(r"value:{}", value), as_="p")

    context.open()
    rg = use_radio_group_controls(context)
    rg.should_checked("foo")
    rg.click("bar")
    context.should_see("value:bar")


def test_dict_options(context: Context):
    @context.register_page
    def index():
        options = [
            {"label": "foo", "value": "value:foo"},
            {"label": "bar", "value": "value:bar"},
        ]
        value = ui.state("")

        td.radio_group(options, value=value)
        ui.text(value)

    context.open()
    rg = use_radio_group_controls(context)
    rg.should_nothing_checked()

    rg.click("foo")
    context.should_see("value:foo")

    rg.click("bar")
    context.should_see("value:bar")
