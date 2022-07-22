#!/usr/bin/env python
# -*-coding:utf-8 -*-
import os
from hoshino import Service


sv = Service('kirara', help_='''

'''.strip())

file_full_path = os.path.dirname(os.path.abspath(__file__))

