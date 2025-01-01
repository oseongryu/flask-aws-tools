import sys

sys.path.append("./common")
import common_utils as utils

userHomeUseYn = True

SHORTS_DIR = utils.add_user_home_path("/DEV/shorts/", True)
BACKGROUND_DIR = utils.add_user_home_path("/DEV/shorts/background", True)
PYTHON_ENV_PATH_WIN = "python"
PYTHON_ENV_PATH_MAC = utils.add_user_home_path("/git/flask-aws-tools/venv/bin/python3", userHomeUseYn)
PYTHON_SHORTS_TTS_PATH = utils.add_user_home_path("/git/flask-aws-tools/common/tts_story_gtts.py", userHomeUseYn)

AUTOMATION_SETTING_PATH = utils.add_user_home_path("/git/python-selenium/static/fredit/setting.json", userHomeUseYn)
AUTOMATION_POPUP_PATH = "/static/js/data/data_automation.json"
AUTOMATION_SCREENSHOT_PATH = utils.add_user_home_path("/git/python-selenium/app/fredit/screenshot", userHomeUseYn)
PYTHON_AUTOMATION_PATH = utils.add_user_home_path("/git/python-selenium/selenium/service.py", userHomeUseYn)
