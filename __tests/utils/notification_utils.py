from __tests.screen import BaseContext


NOTIFICATION_LIST_SELECTOR = ".t-notification-list__show"
NOTIFICATION_SELECTOR = ".t-notification"
CLOSE_BTN_SELECTOR = ".t-message__close"


class use_notify_plugin_controls:
    def __init__(self, context: BaseContext) -> None:
        self._context = context
        self._notification_list = context.page.locator(NOTIFICATION_LIST_SELECTOR)

    def should_count(self, count: int) -> None:
        items = self._notification_list.locator(NOTIFICATION_SELECTOR)
        self._context.expect(items).to_have_count(count)

    def click_close_btn(self, nth: int = 0):
        self._notification_list.locator(NOTIFICATION_SELECTOR).nth(nth).locator(
            CLOSE_BTN_SELECTOR
        ).click()
