#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

from pyVim import connect
from pyVmomi import vim
import os
from datetime import datetime

# Set the file path
base_dir = os.path.dirname(os.path.abspath(__file__))
# base_dir = "/home/ec2-user/environment/ec2/"
file_name = os.path.join(base_dir, "vmware-{}.txt".format(datetime.now().strftime("%Y-%m-%d")))

def get_vm_info(virtual_machine, vc):
    """
    Print information for a particular virtual machine or recurse into a
    folder with depth protection
    """
    summary = virtual_machine.summary
    ins = []
    ins.append(vc)
    ins.append(summary.config.name)
    ins.append(summary.guest.ipAddress) if summary.guest.ipAddress else ins.append("unknow")
    ins.append(str(summary.config.numCpu))
    ins.append(str(summary.config.memorySizeMB))
    ins.append((summary.config.guestFullName).replace(' ', '-')) if 'Windows' in summary.config.guestFullName else ins.append('linux')
    # ins.append((summary.config.guestFullName).replace(' ', '-'))
    ins.append(summary.runtime.powerState)

    ins_str = ' '.join(ins)
    # print(ins_str)

    # Write the info into the file
    with open(file_name, 'a+') as f:
        f.write(ins_str + '\n')


def connect_vcenter(host, user, pwd, vc):
    """
    Connect to you vCenter Server
    """
    vc_ins = connect.SmartConnectNoSSL(host=host, user=user, pwd=pwd)
    content = vc_ins.content
    container = content.rootFolder # starting point to look into
    view_type = [vim.VirtualMachine] # object types to look for
    vm_view = content.viewManager.CreateContainerView(
        container, view_type, True)

    for vm in vm_view.view:
        get_vm_info(vm, vc)


if __name__ == '__main__':
    connect_vcenter('xx.xxx.xx.xx', 'xxxxx', 'xxxxx', 'TEST')

