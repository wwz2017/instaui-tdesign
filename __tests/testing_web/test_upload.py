import pytest
from playwright.sync_api import FilePayload
from __tests.testing_web.context import Context
from instaui import ui, file_io
from instaui_tdesign import td


def sim_input_file(name: str, content: str) -> FilePayload:
    return {"name": name, "mimeType": "text/plain", "buffer": content.encode()}


@pytest.mark.parametrize(
    "multiple, all_files_in_one_request",
    [
        (True, True),
        (True, False),
        (False, True),
        (False, False),
    ],
)
def test_upload_payload_structure(
    context: Context, multiple: bool, all_files_in_one_request: bool
):
    @context.register_page
    def index():
        file_type = ui.state("")

        @file_io.upload_file()
        def upload_file(file: file_io.TUploadFile) -> file_io.TUploadFileResult:
            return {
                "status": 200,
                "extra": {"input type": "list" if isinstance(file, list) else "single"},
            }

        @ui.event(inputs=[ui.event_context.e()], outputs=[file_type])
        def on_success(e):
            response = e["response"]
            response = response[0] if isinstance(response, list) else response
            return response["extra"]["input type"]

        td.upload(
            action=upload_file.url,
            multiple=multiple,
            upload_all_files_in_one_request=all_files_in_one_request,
        ).on_success(on_success)

        ui.text(file_type)

    context.open()
    file_input = context.page.locator('input[type="file"]')

    if multiple:
        file_input.set_input_files(
            [sim_input_file("1.txt", "123"), sim_input_file("2.txt", "456")]
        )
    else:
        file_input.set_input_files(sim_input_file("1.txt", "123"))

    context.should_see("single" if not multiple else "list")
