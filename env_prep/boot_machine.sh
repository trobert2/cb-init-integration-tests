#!/bin/sh
if [ $# -lt 7 ]; then
    echo "Usage: $0 <vm_conf> <flavor_id> <image_id> <keypair> <private_network> <floatingip_id> <vm_name> <optional:userdata> "
    exit 1
fi

flavor_id=$2
image_id=$3
keypair=$4
private_network=$5
floatingip_id=$6
vm_name=$7
userdata=$8

if [ -z "$8" ]
 then
	echo "No userdata..."
        vm_id=`nova boot --flavor $flavor_id --image $image_id --key-name $keypair --nic net-id=$private_network $vm_name --poll | awk '{if (NR==15) print $4}'`

else
	echo "Userdata "$userdata
	vm_id=`nova boot --flavor $flavor_id --image $image_id --key-name $keypair --nic net-id=$private_network --user-data $userdata $vm_name --poll | awk '{if (NR==15) print $4}'`
fi
echo "Vm created with id "$vm_id

vmdevice_id=`quantum port-list --fields id --device_id $vm_id | awk '{if (NR == 4) print $2}'`
echo "Vm device id is "$vmdevice_id

quantum floatingip-associate $floatingip_id $vmdevice_id
tenant_id=`nova show $vm_id | awk '{if (NR==20) print $4}'`
ip_tenant_id=""
while [ "$ip_tenant_id" != "$tenant_id" ]; do
       echo "waiting for floating ip to attach.."
       ip_tenant_id=`quantum floatingip-show $floatingip_id | awk '{if (NR==10) print $4}'`
done

password=`nova get-password $vm_id $keypair.pem`

echo "
password=$password" >> $1

