from pathlib import Path
import shutil

PORJECT_ROOT = Path(__file__).parent.parent.resolve()
PY_PROJECT_ROOT = PORJECT_ROOT.parent

STATIC_DIR_PATH = PY_PROJECT_ROOT.joinpath("src/instaui_tdesign/static").resolve()
PY_TDESIGN_DIST = PY_PROJECT_ROOT.joinpath("tdesign-dist").resolve()

#
DIST_DIR_PATH = Path(__file__).parent.parent.joinpath("dist/instaui-dist").resolve()
JS_FILE_PATH = DIST_DIR_PATH / "instaui-tdesign.js"
CSS_FILE_PATH = DIST_DIR_PATH / "instaui-tdesign.css"

# tdesign module file
TDESIGN_MOUDLE_PATH = (
    Path(__file__).parent.parent.joinpath("dist/tdesign-dist").resolve()
)

TDESIGN_JS_FILE_PATH = TDESIGN_MOUDLE_PATH.joinpath("tdesign.min.js")
TDESIGN_CSS_FILE_PATH = TDESIGN_MOUDLE_PATH.joinpath("tdesign.min.css")


def reset_folder(folder: Path, *, parents: bool = False, exist_ok: bool = False):
    shutil.rmtree(folder, ignore_errors=True)
    folder.mkdir(parents=parents, exist_ok=exist_ok)


def copy_to_compiled():
    reset_folder(STATIC_DIR_PATH, exist_ok=True)
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

    # for cdn
    reset_folder(PY_TDESIGN_DIST, exist_ok=True)
    shutil.copyfile(
        TDESIGN_JS_FILE_PATH, PY_TDESIGN_DIST.joinpath(TDESIGN_JS_FILE_PATH.name)
    )
    shutil.copyfile(
        TDESIGN_CSS_FILE_PATH, PY_TDESIGN_DIST.joinpath(TDESIGN_CSS_FILE_PATH.name)
    )
    print(f"Copied to target folder [{STATIC_DIR_PATH}]")


if __name__ == "__main__":
    copy2py()
