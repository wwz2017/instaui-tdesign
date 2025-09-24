from typing import Optional, Union, Literal
from instaui import ui
from instaui_tdesign.types import TLocale, TCustomizeLocale
from instaui_tdesign._settings import configure
from instaui_tdesign import consts


def use(
    *,
    locale: Optional[Union[TLocale, TCustomizeLocale]] = None,
    theme: Optional[Literal["default", "green", "violet"]] = None,
):
    """Use tdesign ui.

    Args:
        locale (ui.TMaybeRef[Union[TLocale, TCustomizeLocale]], optional): The locale of tdesign ui.

    Examples:
    .. code-block:: python
        from instaui import ui
        import instaui_tdesign as td

        td.use(theme="violet", locale="en-US")

        @ui.page("/")
        def index_page():
            td.input(placeholder="input")
    """

    if locale:
        configure(locale=locale)
    if theme:
        ui.add_css_link(consts.THEME_CSS_DIR / f"theme-{theme}.css")
