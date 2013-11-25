#!/bin/sh
bash utils/prepare.sh configurations/ws12.ini configurations/config.ini userdata_scripts/script.mime
echo 'waiting for boot completion'
python check_instance.py
bash utils/cleanup.sh

echo 'booting instance to check cmd userdata'
bash utils/prepare.sh configurations/ws12.ini configurations/config.ini userdata_scripts/script.cmd
echo 'waiting for boot completion'
python check_userdata.py
bash utils/cleanup.sh

echo 'booting instance to check ps1 userdata'
bash utils/prepare.sh configurations/ws12.ini configurations/config.ini userdata_scripts/script.ps1
echo 'waiting for boot completion'
python check_userdata.py
bash utils/cleanup.sh

