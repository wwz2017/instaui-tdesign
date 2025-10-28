from __tests.screen import BaseContext


MESSAGE_LIST_SELECTOR = ".t-message__list"
MESSAGE_SELECTOR = ".t-message"
CLOSE_BTN_SELECTOR = ".t-message__close"


class use_message_plugin_controls:
    def __init__(self, context: BaseContext) -> None:
        self._context = context
        self._message_list = context.page.locator(MESSAGE_LIST_SELECTOR)

    def should_count(self, count: int) -> None:
        items = self._message_list.locator(MESSAGE_SELECTOR)
        self._context.expect(items).to_have_count(count)

    def click_close_btn(self, nth: int = 0):
        self._message_list.locator(MESSAGE_SELECTOR).nth(nth).locator(
            CLOSE_BTN_SELECTOR
        ).click()
