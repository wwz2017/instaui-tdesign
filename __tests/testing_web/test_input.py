from __tests.testing_web.context import Context
from instaui_tdesign import td
from instaui import ui


def test_value(context: Context):
    @context.register_page
    def index():
        text = ui.state("foo")

        td.input(text)
        ui.text(text)

    context.open()
    input = context.find("input")
    context.expect(input).to_have_value("foo")

    input.fill("bar")
    context.should_see("bar")
