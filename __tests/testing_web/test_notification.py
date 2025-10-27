from __tests.testing_web.context import Context
from instaui_tdesign import td
from instaui import ui
from __tests.utils.switch_utils import use_switch_controls
from __tests.utils.notification_utils import use_notify_plugin_controls


def test_base(context: Context):
    @context.register_page
    def index():
        show = ui.state(False)

        td.switch(show)
        with ui.vif(show):
            td.notification("foo")

    context.open()
    switch = use_switch_controls(context)
    switch.click()
    context.should_see("foo")


def test_duration(context: Context):
    @context.register_page
    def index():
        show = ui.state(False)

        td.switch(show)
        with ui.vif(show):
            td.notification("foo", duration=800).on_duration_end(
                ui.js_event(
                    outputs=[show],
                    code=r"s=> false",
                )
            )

    context.open()
    switch = use_switch_controls(context)
    switch.click()
    context.should_see("foo")
    context.page.wait_for_timeout(1000)
    context.should_not_see("foo")


class TestNotifyPlugin:
    def test_base(self, context: Context):
        @context.register_page
        def index():
            td.button("show").on_click(td.notify_plugin.info(content="foo"))

        context.open()
        context.find("button").click()
        context.should_see("foo")
        context.pause()

    def test_open_multiple(self, context: Context):
        @context.register_page
        def index():
            td.button("show").on_click(
                td.notify_plugin.info(content="foo", duration=0, close_btn=True)
            )

        context.open()
        np = use_notify_plugin_controls(context)
        context.find("button").click(click_count=2)
        np.should_count(2)

    def test_close_btn(self, context: Context):
        @context.register_page
        def index():
            td.button("show").on_click(
                td.notify_plugin.info(content="foo", duration=0, close_btn=True)
            )

        context.open()
        np = use_notify_plugin_controls(context)
        context.find("button").click()
        context.should_see("foo")
        np.click_close_btn()
        context.should_not_see("foo")

    def test_close_all(self, context: Context):
        @context.register_page
        def index():
            td.button("show").on_click(
                td.notify_plugin.info(content="foo", duration=0, close_btn=True)
            )

            td.button("close all").on_click(td.notify_plugin.close_all())

        context.open()
        np = use_notify_plugin_controls(context)
        context.find_by_text("show").click(click_count=2)
        np.should_count(2)
        context.find_by_text("close all").click()
        np.should_count(0)
