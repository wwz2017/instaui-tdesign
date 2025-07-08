"""
Easy to use TDesign UI components for InstaUI.

Examples:
.. code-block:: python
    from instaui import ui
    import instaui_tdesign as td

    td.use()

    @ui.page("/")
    def index_page():
        td.input(placeholder="input")
"""

__all__ = [
    "use",
    "button",
    "date_picker",
]


from .setup import use
from .components.button import Button as button
from .components.date_picker import DatePicker as date_picker
