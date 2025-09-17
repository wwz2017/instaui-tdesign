from __tests.testing_web.context import Context
import instaui_tdesign as td


def test_base(context: Context):
    @context.register_page
    def index():
        with td.affix():
            td.button("Affix top")

        for i in range(3):
            td.card(f"Card {i}").style("height: 100vh;")

    context.open()
    context.find_by_text("Card 2").scroll_into_view_if_needed()
    context.expect(context.find_by_text("Affix top")).to_be_in_viewport()
