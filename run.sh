#!/bin/sh
bash utils/prepare.sh configurations/ws12.ini configurations/config.ini userdata_scripts/script.mime
#python wait for completion
echo 'waiting for boot completion'
python check_instance.py

