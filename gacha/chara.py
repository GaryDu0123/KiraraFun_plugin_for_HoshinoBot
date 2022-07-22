#!/usr/bin/env python
# -*-coding:utf-8 -*-
import json
import os


file_full_path = os.path.dirname(os.path.abspath(__file__))


class Roster:
    def __init__(self):
        try:
            with open(f"{file_full_path}/chara_data.json", "r", encoding="utf-8") as f:
                self.chara_list = json.load(f)
        except FileNotFoundError:
            self.chara_list = {"5": {}, "4": {}, "3": {}}
            print("无法找到chara_data.json文件，请检查文件路径")
        except Exception:
            # todo 打印错误信息
            self.chara_list = {"5": {}, "4": {}, "3": {}}
            print("卡池载入错误, 请手动更新卡池数据")


roster = Roster()
