import sys

sys.path.append("./common")
import common_utils as utils

userHomeUseYn = True

SCREENSHOT_DIR = utils.add_user_home_path("/git/python-selenium/app/fredit/screenshot", userHomeUseYn)
SHORTS_DIR = utils.add_user_home_path("/DEV/shorts/", False)
BACKGROUND_DIR = utils.add_user_home_path("/DEV/shorts/background", False)
JS_DIR = utils.add_user_home_path("/git/flask-aws-tools/static/js/data", userHomeUseYn)
AUTOMATION_SETTING = utils.add_user_home_path("/git/python-selenium/static/fredit/setting.json", userHomeUseYn)
AUTOMATION_POPUP_SETTING = "/static/js/data/data_automation.json"
PYTHON_ENV_PATH_WIN = "python"
PYTHON_ENV_PATH_MAC = utils.add_user_home_path("/git/python-selenium/venv/bin/python3", userHomeUseYn)
PYTHON_SHORTS_TTS_PATH = utils.add_user_home_path("/Users/admin/git/python-selenium/shorts/tts_story_gtts.py", userHomeUseYn)
PYTHON_AUTOMATION_PATH = utils.add_user_home_path("/git/python-selenium/selenium/service.py", userHomeUseYn)
