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


async def update_gacha_pool():
    with open('CharacterList.json', 'r', encoding='utf-8') as f:
        character_list = json.load(f)
    # character_list = await request_chara_data_from_server()
    # with open("CharacterList.json", "w", encoding="utf-8") as f:
    #     json.dump(character_list, f, ensure_ascii=False)

    # 创建角色的星池
    chara_list = {"5": {}, "4": {}, "3": {}}

    for chara in character_list:
        # 排除进化后的卡面, 只对四星或五星有效(你游三星不能进化), 看起来最后一位代表着是否是进化的卡
        if str(chara['m_CharaID'])[-1] == "1":
            continue
        if chara["m_Rare"] == 4:
            chara_list["5"][chara["m_Name"]] = chara['m_CharaID']
        elif chara["m_Rare"] == 3:
            chara_list["4"][chara["m_Name"]] = chara['m_CharaID']
        elif chara["m_Rare"] == 2:
            chara_list["3"][chara["m_Name"]] = chara['m_CharaID']
        else:
            raise Exception("Error: Unknown character rarity")
    with open("chara_data.json", "w", encoding="utf-8") as f:
        json.dump(chara_list, f, ensure_ascii=False, indent=4)
    return chara_list


roster = Roster()
