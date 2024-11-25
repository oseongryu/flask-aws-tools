import sys

sys.path.append("./common")
import common_utils as utils

userHomeUseYn = False

SCREENSHOT_DIR = utils.add_user_home_path("/git/python-selenium/app/fredit/screenshot", userHomeUseYn)
SHORTS_DIR = utils.add_user_home_path("/DEV/shorts/", userHomeUseYn)
BACKGROUND_DIR = utils.add_user_home_path("/DEV/shorts/background", userHomeUseYn)
IMAGE_DIR = utils.add_user_home_path("/git/python-selenium/app/fredit/screenshot/41_simple_card_basic/20241121_012025", userHomeUseYn)
JS_DIR = utils.add_user_home_path("/git/flask-aws-tools/static/js/data", userHomeUseYn)
AUTOMATION_POPUP_SETTING = utils.add_user_home_path("/js/data/data_automation.json", userHomeUseYn)
DYNAMO_POPUP_SETTING = utils.add_user_home_path("/js/data/data_dynamo.json", userHomeUseYn)
AUTOMATION_SETTING = utils.add_user_home_path("/git/python-selenium/static/fredit/setting.json", userHomeUseYn)
