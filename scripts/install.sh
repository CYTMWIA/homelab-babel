#! /bin/bash
set -e

python -m venv venv

source venv/bin/activate
pip install -i https://mirrors.bfsu.edu.cn/pypi/web/simple -r requirements.txt
