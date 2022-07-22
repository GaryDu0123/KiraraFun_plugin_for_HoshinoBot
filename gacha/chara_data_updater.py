#!/usr/bin/env python
# -*-coding:utf-8 -*-
import os
from .chara import roster
import aiohttp

try:
    import ujson as json
except Exception:
    import json
from hoshino import Service, priv

sv = Service("kirara-data-updater", use_priv=priv.SU, manage_priv=priv.SU, visible=False)
file_full_path = os.path.dirname(os.path.abspath(__file__))


async def request_chara_data_from_server():
    async with aiohttp.request("GET", "https://database.kirafan.cn/database/CharacterList.json") as rep:
        try:
            return await rep.json()
        except Exception:
            return json.loads(await rep.read())


async def update_gacha_pool():
    character_list = await request_chara_data_from_server()
    # wiki的中间数据
    # with open(f"{file_full_path}/CharacterList.json", "w", encoding="utf-8") as f:
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
    with open(f"{file_full_path}/chara_data.json", "w", encoding="utf-8") as f:
        json.dump(chara_list, f, ensure_ascii=False, indent=4)
    roster.chara_list = chara_list


sv.scheduled_job('cron', hour=23, jitter=300)(update_gacha_pool)
