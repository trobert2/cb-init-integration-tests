#!/bin/sh
if [ $# -ne 2 ]; then
    echo "Usage: $0 <input_config.ini> <vm_config.ini>"
    exit 1
fi
config_ini=$1
flavor_id=$(awk -F "=" '/flavor_id/ {print $2}' $config_ini)
image_id=$(awk -F "=" '/image_id/ {print $2}' $config_ini)
keypair=$(awk -F "=" '/keypair/ {print $2}' $config_ini)

echo "Using: "
echo "Flavor Id "$flavor_id
echo "Image Id "$image_id
echo "Keypair name "$keypair

echo "Retrieving Image size "
imageSize=`nova image-show $image_id | awk '{ if (NR==11) print $4}'`
echo "Image size "$imageSize

network_ids=()
function get_network_id  {
network_id=`quantum subnet-show $1 | awk '{if ( NR == 13 ) print $4}'`
network_ids+=($network_id)
}

function check_public_network {
public=`quantum net-show $1 | awk '{if (NR ==10) print $4}'`
if [ "$public" ==  "True" ] ; then
 return 0
else
 return 1
fi
}

subnet_ids=($(quantum subnet-list | awk '{print $2}'))

 for i in "${subnet_ids[@]:1}"
 do
    :
   get_network_id $i
   done

for i in "${network_ids[@]}"
do
  :
  if check_public_network $i ; then
    echo "Found public network with id "$i
    public_network=$i
  else
    echo "Found private network with id "$i
    private_network=$i
  fi
done

key=`nova keypair-list | grep $keypair`
if [ -z "$key" ] ; then
	echo "Creating keypair"
	nova keypair-add $keypair > $keypair".pem" 2> /dev/null
else
	echo "Using existing keypair "$keypair
fi

floatingip_id=`quantum floatingip-create $public_network | awk '{if (NR==8) print $4}'`
echo $floatingip_id

ip=`quantum floatingip-show $floatingip_id | awk '{if (NR==5) print $4}'`

echo  "[BaseVmConf]
flavor_id=$flavor_id
image_id=$image_id
floatingip_id=$floatingip_id
private_network=$private_network
" > $2

echo "[CheckList]" >> $1

grep 'keypair=[a-zA-Z0-1]+' $1
if [ $? -ne 0 ];then sed -i 's/keypair=.*/keypair=$keypair/g' $1;fi

grep 'ip=[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}' $1
if [ $? -ne 0 ];then sed -i 's/ip=.*/ip=$ip/g' $1;fi

grep 'imageSize=[0-1]+' $1
if [ $? -ne 0 ];then sed -i 's/imageSize=.*/imageSize=$imageSize/g' $1;fi

