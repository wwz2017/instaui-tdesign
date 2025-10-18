from __tests.testing_web.context import Context
from instaui import ui
from instaui_tdesign import td


def test_base(context: Context):
    @context.register_page
    def index():
        with td.collapse():
            with td.collapse_panel("foo"):
                pass

    context.open()
    context.should_see("foo")


def test_default_value(context: Context):
    @context.register_page
    def index():
        with td.collapse(default_value=[0]):
            with td.collapse_panel("foo"):
                ui.text("bar")

    context.open()
    context.should_see("foo")
    context.should_see("bar")


def test_value(context: Context):
    @context.register_page
    def index():
        value = ui.state([0])

        ui.text(ui.str_format("value: {}", value))

        with td.collapse(value=value):
            with td.collapse_panel("foo1"):
                ui.text("bar1")
            with td.collapse_panel("foo2"):
                ui.text("bar2")

    context.open()
    context.should_see("foo1")
    context.should_see("bar1")
    context.should_not_see("bar2")

    context.find_by_text("foo2").click()
    context.should_see("bar2")
    context.should_see("value: 0,1")
