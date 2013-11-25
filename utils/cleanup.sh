#!/bin/sh
if [ $# -ne 1 ]; then
    echo "Usage: $0 <input_config.ini>"
    exit 1
fi

config_ini=$1
keypair=$(awk -F "=" '/keypair/ {print $2}' $config_ini)
vm_id=$(awk -F "=" '/vm_id/ {print $2}' $config_ini)

echo "cleaning up"
nova delete $vm_id
