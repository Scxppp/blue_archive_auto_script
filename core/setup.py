import json
import time

from core import STATIC_CONFIG_PATH
from core.utils import kmp
from gui.util.config_set import ConfigSet


class Setup:
    def __init__(self):
        basic_config = {}
        with open(STATIC_CONFIG_PATH, 'r', encoding='utf-8') as f:
            basic_config = json.load(f).get('basic')
        self.base_time = time.time()
        self.pos = []
        self.ocr = None
        self.config = ConfigSet()

        self.click_time = 0.0

        self.schedule_pri = self.config.get('schedulePriority')  # ** 可设置参数，日程区域优先级  1 2 3 4 5 分别表示 已经出的五个区域
        self.latest_img_array = None

        # Load static config
        self.main_activity = basic_config['activity_list']
        self.main_activity_label = basic_config['activity_label_list']
        self.keyword = basic_config['keyword']
        self.schedule_lo_y = basic_config['schedule_point_list']
        self.to_page = basic_config['to_page']
        self.location_recognition_list = basic_config['location_recognition_list']

        self.keyword_apper_time_dictionary = {i: 0 for i in self.keyword}

    def return_location(self):
        for item_location in self.location_recognition_list:
            for index_recognition in range(0, len(item_location['name_list'])):
                if self.pd(item_location['name_list'][index_recognition],
                           item_location['count_list'][index_recognition]):
                    return item_location['result']
        return "UNKNOWN UI PAGE"

    def get_keyword_appear_time(self, string):      # 用于统计关键字出现的次数
        for i in range(0, len(self.keyword)):
            self.keyword_apper_time_dictionary[self.keyword[i]] = kmp(self.keyword[i], string)

    def img_ocr(self, img):                         # 用于文字识别
        time.time()
        out = self.ocr.ocr(img)
        res = ""
        for i in range(0, len(out)):
            if out[i]["score"] > 0.4:
                res = res + out[i]["text"]
        return res

    def set_click_time(self):                       # 用于计算点击时间，如果截图时间后于点击时间，则该图片会被判断为无效
        self.click_time = time.time() - self.base_time

    def pd(self, list1, list2):                     # 用于判断关键字出现的次数是否满足要求
        for i in range(0, len(list1)):
            if self.keyword_apper_time_dictionary[list1[i]] < list2[i]:
                return False
        return True
