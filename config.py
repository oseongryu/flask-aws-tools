import os
import platform
import posixpath
import sys

import common.commonfunction as cmmfun

rootUserHomeUseYn = False
gitUserHomeUseYn = True if platform.system() == "Windows" else False

current_directory = os.getcwd()
project_name = os.path.basename(current_directory)


ROOT_PATH = cmmfun.add_user_home_path("/app", rootUserHomeUseYn)
AUTO_ROOT = "automation"

PRJ_AUTO_PATH = posixpath.join(ROOT_PATH, AUTO_ROOT)
PRJ_AUTO_LOG_PATH = posixpath.join(ROOT_PATH, AUTO_ROOT, "logs")
PRJ_SCREENSHOT_PATH = posixpath.join(ROOT_PATH, AUTO_ROOT, "screenshot")
AUTO_STATIC_IMG_PATH = posixpath.join(ROOT_PATH, AUTO_ROOT, "static/fredit/img")
AUTO_STATIC_SETTING_PATH = posixpath.join(ROOT_PATH, AUTO_ROOT, "static/fredit/setting.json")
AUTO_POPUP_JSON_PATH = "/static/js/data/data_automation.json"

SHORTS_PATH = cmmfun.add_user_home_path("/app/shorts", rootUserHomeUseYn)
SHORTS_DB_PATH = cmmfun.add_user_home_path("/app/shorts/database/test.db", rootUserHomeUseYn)


PYTHON_ENV_PATH_WIN = "python"
PYTHON_ENV_PATH_MAC = cmmfun.add_user_home_path(f"/git/{project_name}/venv/bin/python3", gitUserHomeUseYn)
SHORTS_PROJECT_PATH = cmmfun.add_user_home_path(f"/git/{project_name}", gitUserHomeUseYn)
SHORTS_TTS_SCRIPT_PATH = cmmfun.add_user_home_path(f"/git/{project_name}/service/shorts/tts_story_gtts.py", gitUserHomeUseYn)
AUTOMATION_SCRIPT_PATH = cmmfun.add_user_home_path(f"/git/{project_name}/service/automation/automation.py", gitUserHomeUseYn)
AUTOMATION_REMOVE_SCRIPT_PATH = cmmfun.add_user_home_path(f"/git/{project_name}/service/automation/automation_remove_screenshot.py", gitUserHomeUseYn)
