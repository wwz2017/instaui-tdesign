import pytest
from __tests.testing_zero.context import ZeroContext as Context
from instaui import zero
from instaui.launch_collector import get_launch_collector
import instaui_tdesign as td


@pytest.fixture(scope="function")
def page_init_lifespan_setup():
    yield
    get_launch_collector().clear_page_request_lifespans()


def test_default_locale(context: Context):
    td.use()

    def index():
        td.pagination(total=6)

    context.open(zero().to_html_str(index))
    context.should_see("6 items")


def test_zh_locale(context: Context):
    td.use(locale="zh-CN")

    def index():
        td.pagination(total=6)

    context.open(zero().to_html_str(index))
    context.should_see("共 6 条数据")
