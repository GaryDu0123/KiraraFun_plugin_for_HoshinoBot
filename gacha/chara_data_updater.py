#!/usr/bin/env python
# -*-coding:utf-8 -*-
import os
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
            data = await rep.json()
        except Exception:
            data = json.loads(await rep.read())
        with open(f'{file_full_path}/CharacterList.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False)

sv.scheduled_job('cron', hour=23, jitter=300)(request_chara_data_from_server)

