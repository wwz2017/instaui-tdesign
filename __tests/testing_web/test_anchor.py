from __tests.testing_web.context import Context
from instaui import ui
import instaui_tdesign as td
from __tests.utils.anchor_utils import should_anchor_item_active, click_anchor_item


def test_base(context: Context):
    @context.register_page
    def index():
        with td.card().style("position: fixed;  right: 2rem;"), td.anchor():
            td.anchor_item(href="#page1", title="Page 1")
            td.anchor_item(href="#page2", title="Page 2")
            td.anchor_item(href="#page3", title="Page 3")

        with td.card().style("height: 100vh"):
            ui.heading("Page1").props({"id": "page1"})
            ui.text("Content1")

        with ui.column().style("height: 100vh"):
            ui.heading("Page2").props({"id": "page2"})
            ui.text("Content2")

        with ui.column().style("height: 100vh"):
            ui.heading("Page3").props({"id": "page3"})
            ui.text("Content3")

    context.open()
    context.find_by_text("Content3").scroll_into_view_if_needed()

    should_anchor_item_active(context, "Page 2")
    click_anchor_item(context, "Page 1")

    context.should_see("Content1")
