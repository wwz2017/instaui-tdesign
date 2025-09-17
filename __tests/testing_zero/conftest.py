import pytest
from playwright.sync_api import Browser
from __tests.testing_zero.context import ZeroContext


@pytest.fixture(scope="function")
def context(browser: Browser):
    page = browser.new_page()
    context = ZeroContext(page)
    yield context
    page.close()
