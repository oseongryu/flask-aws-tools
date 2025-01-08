import os
import sys

import common.commonfunction as utils

userHomeUseYn = True
current_directory = os.getcwd()
project_name = os.path.basename(current_directory)

PYTHON_ENV_PATH_WIN = "python"
PYTHON_ENV_PATH_MAC = utils.add_user_home_path(f"/git/{project_name}/venv/bin/python3", userHomeUseYn)

SHORTS_RESOURCE_PATH = utils.add_user_home_path("/DEV/shorts", False)
SHORTS_DB_PATH = utils.add_user_home_path("/DEV/shorts/database/test.db", False)
SHORTS_PROJECT_PATH = utils.add_user_home_path(f"/git/{project_name}", userHomeUseYn)
SHORTS_TTS_SCRIPT_PATH = utils.add_user_home_path(f"/git/{project_name}/service/shorts/tts_story_gtts.py", userHomeUseYn)

AUTOMATION_POPUP_PATH = "/static/js/data/data_automation.json"
AUTOMATION_SETTING_PATH = utils.add_user_home_path("/git/python-selenium/static/fredit/setting.json", userHomeUseYn)
AUTOMATION_SCREENSHOT_PATH = utils.add_user_home_path("/git/python-selenium/app/fredit/screenshot", userHomeUseYn)
AUTOMATION_SCRIPT_PATH = utils.add_user_home_path("/git/python-selenium/selenium/service.py", userHomeUseYn)
AUTOMATION_REMOVE_SCRIPT_PATH = utils.add_user_home_path("/git/python-selenium/selenium/service_remove_screenshot.py", userHomeUseYn)
