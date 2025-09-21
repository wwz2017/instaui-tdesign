from pathlib import Path
import shutil


STATIC_DIR_PATH = (
    Path(__file__).parent.joinpath("../../src/instaui_tdesign/static").resolve()
)

DIST_DIR_PATH = Path(__file__).parent.parent.joinpath("dist/instaui-dist").resolve()
JS_FILE_PATH = DIST_DIR_PATH / "instaui-tdesign.js"
CSS_FILE_PATH = DIST_DIR_PATH / "instaui-tdesign.css"

# tdesign module file
TDESIGN_MOUDLE_PATH = (
    Path(__file__).parent.parent.joinpath("dist/tdesign-dist").resolve()
)

TDESIGN_JS_FILE_PATH = TDESIGN_MOUDLE_PATH.joinpath("tdesign.min.js")
TDESIGN_CSS_FILE_PATH = TDESIGN_MOUDLE_PATH.joinpath("tdesign.min.css")


def copy_to_compiled():
    STATIC_DIR_PATH.mkdir(exist_ok=True)
    shutil.copyfile(JS_FILE_PATH, STATIC_DIR_PATH.joinpath(JS_FILE_PATH.name))
    shutil.copyfile(
        CSS_FILE_PATH,
        STATIC_DIR_PATH.joinpath(CSS_FILE_PATH.name),
    )
    shutil.copyfile(
        TDESIGN_JS_FILE_PATH,
        STATIC_DIR_PATH.joinpath(TDESIGN_JS_FILE_PATH.name),
    )
    shutil.copyfile(
        TDESIGN_CSS_FILE_PATH,
        STATIC_DIR_PATH.joinpath(TDESIGN_CSS_FILE_PATH.name),
    )


def copy2py():
    copy_to_compiled()
    print(f"Copied to target folder [{STATIC_DIR_PATH}]")


if __name__ == "__main__":
    copy2py()
