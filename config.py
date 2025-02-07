import os
import platform
import posixpath
import sys

import common.commonfunction as utils

rootUserHomeUseYn = False
gitUserHomeUseYn = True if platform.system() == "Windows" else False

current_directory = os.getcwd()
project_name = os.path.basename(current_directory)

GPT_HTML_PATH = utils.add_user_home_path("/Downloads/temp.html", True)

ROOT_PATH = utils.add_user_home_path("/app", rootUserHomeUseYn)
FREDIT_PATH = "fredit"

PRJ_LOG_PATH = posixpath.join(ROOT_PATH, FREDIT_PATH, "logs")
PRJ_SCREENSHOT_PATH = posixpath.join(ROOT_PATH, FREDIT_PATH, "screenshot")
AUTO_STATIC_IMG_PATH = posixpath.join(ROOT_PATH, FREDIT_PATH, "static/fredit/img")
AUTO_STATIC_SETTING_PATH = posixpath.join(ROOT_PATH, FREDIT_PATH, "static/fredit/setting.json")
AUTO_POPUP_JSON_PATH = "/static/js/data/data_automation.json"

SHORTS_PATH = utils.add_user_home_path("/app/shorts", rootUserHomeUseYn)
SHORTS_DB_PATH = utils.add_user_home_path("/app/shorts/database/test.db", rootUserHomeUseYn)


PYTHON_ENV_PATH_WIN = "python"
PYTHON_ENV_PATH_MAC = utils.add_user_home_path(f"/git/{project_name}/venv/bin/python3", gitUserHomeUseYn)
SHORTS_PROJECT_PATH = utils.add_user_home_path(f"/git/{project_name}", gitUserHomeUseYn)
SHORTS_TTS_SCRIPT_PATH = utils.add_user_home_path(f"/git/{project_name}/service/shorts/tts_story_gtts.py", gitUserHomeUseYn)
AUTOMATION_SCRIPT_PATH = utils.add_user_home_path(f"/git/{project_name}/service/automation/automation.py", gitUserHomeUseYn)
AUTOMATION_REMOVE_SCRIPT_PATH = utils.add_user_home_path(f"/git/{project_name}/service/automation/automation_remove_screenshot.py", gitUserHomeUseYn)
