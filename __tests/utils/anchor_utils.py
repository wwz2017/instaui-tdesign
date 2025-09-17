from __tests.screen import BaseContext


def should_anchor_item_active(context: BaseContext, text: str):
    context.expect(
        context.find_by_selector(".t-anchor__item.t-is-active a")
    ).to_have_text(text)


def click_anchor_item(context: BaseContext, text: str):
    context.page.locator("css=.t-anchor__item", has_text=text).click()
