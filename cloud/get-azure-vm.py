#!/usr/bin/env python3

from azure.mgmt.compute import ComputeManagementClient
from azure.identity import ClientSecretCredential
from azure.mgmt.network import NetworkManagementClient
import os
from datetime import datetime

# Load your credentials, you need create app in AAD
Subscription_Id = "48c1cfaa-7022-231e-a0f7-b85b2effce48"
Tenant_Id = "605ba532-d495-2131-8df0-e4f271b13940"
Client_Id = "76a5d8a2-96e9-232e-a2b7-62fb77d83378"
Secret = "xFIO9U0P1231Vxeoy_s0.QJD.sx_9X1_o2"

credential = ClientSecretCredential(
        client_id=Client_Id,
        client_secret=Secret,
        tenant_id=Tenant_Id
    )
    
# Set the file path and file name
base_dir = "/home/ec2-user/environment/ec2/"
file_name = os.path.join(base_dir, "azure-%s.txt" % (datetime.now().strftime("%Y-%m-%d")))

# Create the API Client
compute_client = ComputeManagementClient(credential, Subscription_Id)
network_client = NetworkManagementClient(credential, Subscription_Id)

for vm in compute_client.virtual_machines.list_all():
    resource_group = vm.id.split('/')[4]
    ins = []
    # Collect the attributes that we need from the vm information
    ins.append("Azure")
    ins.append(vm.name)
    ins.append(vm.hardware_profile.vm_size)
    ins.append(vm.location)

    # Get the private ip throuth the nic
    for nic in vm.network_profile.network_interfaces:
        name = nic.id.split('/')[-1]
        rgroup = nic.id.split('/')[4]
        ips = network_client.network_interfaces.get(rgroup, name).ip_configurations
        for x in ips:
            ins.insert(1, x.private_ip_address)
    # Get the OS running information
    ins_view = compute_client.virtual_machines.instance_view(resource_group, vm.name)
    ins.append('unknow') if ins_view.os_name is None else ins.append((ins_view.os_name).replace(' ', '-'))
    ins.append((ins_view.statuses[1].display_status).split(' ')[-1])
    
    ins_str = ' '.join(ins)

    # Write the  vm info into file
    with open(file_name, 'a+') as f:
        f.write(ins_str)
        f.write('\n')

network_client.close()
compute_client.close()
