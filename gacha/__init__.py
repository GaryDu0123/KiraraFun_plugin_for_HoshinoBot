#!/usr/bin/env python
# -*-coding:utf-8 -*-
# !/usr/bin/env python
# -*-coding:utf-8 -*-
import base64
import os
import re
from io import BytesIO
import aiohttp

try:
    import ujson as json
except Exception:
    import json
from PIL import Image, ImageFont, ImageDraw, ImageEnhance
from .gacha import Gacha
from ..kirara import sv
from .chara_data_updater import update_gacha_pool

file_full_path = os.path.dirname(os.path.abspath(__file__))

# 初始化全局的抽卡图片
# 没抽到五星的背景
gacha_bg_without_5 = Image.open(f"{file_full_path}/../img/gacha/1.png").convert("RGBA")
# 抽到五星的背景
gacha_bg_with_5 = Image.open(f"{file_full_path}/../img/gacha/2.png").convert("RGBA")


async def open_or_download_image(path, link):
    if os.path.exists(path):
        return Image.open(path)
    else:
        async with aiohttp.request("GET", link) as rep:
            img = Image.open(BytesIO(await rep.read()))
            img.save(path)
        return img


async def draw_gacha_result(gacha_result: list):
    image_list = []
    for chara_id in gacha_result[0]:
        img = await open_or_download_image(f"{file_full_path}/../img/charaicon/charaicon_{chara_id}.png",
                                           f"https://mergedcharaicon-asset.kirafan.cn/charaicon_{chara_id}.png")
        image_list.append(img.resize((139, 139)))

    gacha_bg = gacha_bg_with_5 if gacha_result[1] > 0 else gacha_bg_without_5
    # 第一张卡的定位为 (677, 153)
    index = 0
    for i in range(2):
        for j in range(5):
            if index >= len(image_list):
                return gacha_bg
            gacha_bg.paste(image_list[index], (677 + j * (20 + 139), 153 + i * (20 + 139)))
            index += 1
    return gacha_bg


gacha = Gacha()


@sv.on_fullmatch(('kirara十连', 'kirara 十连'), only_to_me=True)
async def kirara_gacha_ten(bot, ev):
    buf = BytesIO()
    try:
        gacha_result = gacha.gacha_ten()
    except Exception as e:
        await bot.send(ev, f'抽卡出错~wwwww')
        return
    (await draw_gacha_result(gacha_result)).save(buf, format='PNG')
    base64_str = f'base64://{base64.b64encode(buf.getvalue()).decode()}'
    await bot.send(ev, f'''[CQ:image,file={base64_str}]''')


@sv.on_fullmatch(('kirara单抽', 'kirara 单抽'), only_to_me=True)
async def kirara_gacha_one(bot, ev):
    buf = BytesIO()
    try:
        gacha_result = gacha.gacha_one(gacha.up_prob, gacha.s5_prob, gacha.s4_prob)
    except Exception as e:
        await bot.send(ev, f'抽卡出错~wwwww')
        return
    (await draw_gacha_result([[gacha_result[0]], 1 if gacha_result[1] == 5 else 0])).save(buf, format='PNG')
    base64_str = f'base64://{base64.b64encode(buf.getvalue()).decode()}'
    await bot.send(ev, f'''[CQ:image,file={base64_str}]''')


@sv.on_rex(r'kirara *更新(卡池|角色)数据', only_to_me=True)
async def update_gacha_data(bot, ev):
    await bot.send(ev, '更新中...')
    try:
        await update_gacha_pool()
        await bot.send(ev, '角色数据已更新')
    except Exception:
        await bot.send(ev, '角色数据更新失败')
