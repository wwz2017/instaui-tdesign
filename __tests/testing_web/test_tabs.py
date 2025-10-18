from __tests.testing_web.context import Context
from instaui_tdesign import td
from instaui import ui


def test_base(context: Context):
    @context.register_page
    def index():
        with td.tabs(default_value="0"):
            with td.tab_panel(label="tab1", value="0"):
                ui.text("foo")
            with td.tab_panel(label="tab2", value="1"):
                ui.text("bar")

    context.open()
    context.should_see("foo", exact=True)
    context.find_by_text("tab2").click()
    context.should_see("bar", exact=True)
