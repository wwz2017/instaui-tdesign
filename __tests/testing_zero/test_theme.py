from __tests.testing_zero.context import ZeroContext as Context
from instaui import ui, html, zero
import instaui_tdesign as td
from __tests.utils.style_testing_utils import update_style, use_computed_style


def target_box():
    html.div().classes("target").style(
        "width:1rem ; height:1rem ; background-color:var(--td-brand-color)"
    )


def test_base(context: Context):
    def index():
        td.use(theme="violet")
        info = use_computed_style("background-color", target_selector=".target")
        info.create_button()

        ui.text(info.value)
        target_box()

    context.open(zero().to_html_str(index))

    update_style(context)
    context.should_see("rgb(142, 81, 255)")


def test_dark(context: Context):
    def index():
        td.use(theme="violet")
        info = use_computed_style("background-color", target_selector=".target")
        info.create_button()
        dark = ui.use_dark()

        td.checkbox(dark)
        ui.text(info.value)
        target_box()

    context.open(zero().to_html_str(index))

    checkbox = context.find("checkbox")
    checkbox.set_checked(True, force=True)

    update_style(context)
    context.should_see("rgb(167, 120, 255")

    checkbox.set_checked(False, force=True)

    update_style(context)
    context.should_see("rgb(142, 81, 255)")
