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
