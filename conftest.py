# -*- encoding: utf-8 -*-
"""
@File    :  conftest.py
@Time    :  2022/01/28 17:57:16
@Author  :  Kevin Wang
@Desc    :  https://stackoverflow.com/questions/42996270/change-pytest-rootdir
"""

import sys
from pathlib import Path

scripts_path = Path(__file__).parent / 'src'
sys.path.append(scripts_path.__str__())

def pytest_configure(config):
    config.project_root = Path(__file__).parent
    config.scripts_path = scripts_path
