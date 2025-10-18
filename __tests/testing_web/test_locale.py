from __tests.testing_web.context import Context
from instaui_tdesign import td
from instaui_tdesign import locales
from __tests.utils.select_utils import use_select_controls
from __tests.utils.input_utils import use_input_controls


def test_use_locale_dict(context: Context):
    @context.register_page
    def index():
        locale_dict, lang = locales.use_locale_dict()

        td.select(["en_US", "zh_CN"], lang)

        with td.config_provider(global_config=locale_dict):
            td.input().classes("target")

    context.open()
    select = use_select_controls(context)
    input = use_input_controls(context, selector=".target")

    input.should_placeholder("please enter")

    select.select_option("zh_CN")
    input.should_placeholder("请输入")
