import os
import platform
import posixpath
import sys

import common.commonfunction as cmmfun

if platform.system() == "Windows":
    rootUserHomeUseYn = False
    gitUserHomeUseYn = True
elif platform.system() == "Darwin":
    rootUserHomeUseYn = True
    gitUserHomeUseYn = True
else:
    rootUserHomeUseYn = True
    gitUserHomeUseYn = False

current_directory = os.getcwd()
project_name = os.path.basename(current_directory)

from enum import Enum


class TemplateFolder(Enum):
    VIEWS = "views"
    DIST = "dist"


class EnumDB(Enum):
    SQLITE = "sqlite"
    MARIADB = "mariadb"


ROOT_PATH = cmmfun.add_user_home_path("/app", rootUserHomeUseYn)
AUTO_ROOT = "automation"

routes_items = os.getenv("ROUTES_ITEM", "").split(",")
for routes_item in routes_items:
    if "db" in routes_item:
        SQLITE_DB_PATH = posixpath.join(ROOT_PATH, "tcinet.db")
    if "shorts" in routes_item:

        PRJ_AUTO_PATH = posixpath.join(ROOT_PATH, AUTO_ROOT)
        PRJ_AUTO_LOG_PATH = posixpath.join(ROOT_PATH, AUTO_ROOT, "logs")
        PRJ_SCREENSHOT_PATH = posixpath.join(ROOT_PATH, AUTO_ROOT, "screenshot")
        AUTO_STATIC_IMG_PATH = posixpath.join(ROOT_PATH, AUTO_ROOT, "static/fredit/img")
        AUTO_STATIC_SETTING_PATH = posixpath.join(ROOT_PATH, AUTO_ROOT, "static/fredit/setting.json")
        AUTO_POPUP_JSON_PATH = "/static/js/data/data_automation.json"

        SHORTS_PATH = cmmfun.add_user_home_path("/app/shorts", rootUserHomeUseYn)

        PYTHON_ENV_PATH_WIN = "python"
        PYTHON_ENV_PATH_MAC = cmmfun.add_user_home_path(f"/git/{project_name}/venv/bin/python3", gitUserHomeUseYn)
        SHORTS_PROJECT_PATH = cmmfun.add_user_home_path(f"/git/{project_name}", gitUserHomeUseYn)
        SHORTS_TTS_SCRIPT_PATH = cmmfun.add_user_home_path(f"/git/{project_name}/module_shorts/shorts/tts_story_gtts.py", gitUserHomeUseYn)
        AUTOMATION_SCRIPT_PATH = cmmfun.add_user_home_path(f"/git/{project_name}/module_shorts/automation.py", gitUserHomeUseYn)
        AUTOMATION_REMOVE_SCRIPT_PATH = cmmfun.add_user_home_path(f"/git/{project_name}/module_shorts/automation_remove_screenshot.py", gitUserHomeUseYn)
