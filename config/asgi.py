#!/usr/bin/python3
# -*- coding:utf-8 -*-
# __author__ = '__Miles__'

import os
import sys
import django
from channels.routing import get_default_application
from pathlib import Path

# application加入查找路径中  从wsgi.py中复制
app_path = Path(__file__).parents[1].resolve()
sys.path.append(str(app_path / "zanhu"))

# channles 介绍中复制
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")
django.setup()
application = get_default_application()
