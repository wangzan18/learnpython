
#加载虚拟机清单
$VMsList = Import-Csv C:\Users\zan.wang\Desktop\blog\Powershell\vm_create.csv  -Encoding Default
$date = Get-date -Format yyyy-MM-dd

foreach($vms in $VMsList)
{
    $vcip = $vms.vcip
    $vmName=$vms.name #虚拟机名称
    $vmDatastore=$vms.datastore #创建虚拟机目标存储
    $vmTemplate=$vms.template #模板
    $vmIP=$vms.IP #虚拟机IP
    $vmMask=$vms.mask #虚拟机NETMASK
    $vmGateway=$vms.gateway #虚拟机GATEWAY
    $vmProject=$vms.project #虚拟机备注
    $vmSpec=$vms.osspec # 系统类型，centos 或者 windows
    $vmCpu=$vms.cpu #虚拟机CPU
    $vmMemory=$vms.memory #虚拟机内存
    $vmDisk=$vms.disk #虚拟机添加磁盘大小
    $vmHarddatastore=$vms.datastore #虚拟机新增磁盘目标存储
    $vmNetworkName=$vms.networkname #端口组名称
    $Location=$vms.location #虚拟机所在文件夹
    $Pool=$vms.pool #虚拟机所在的资源池
    $admin=$vms.admin # 负责人

    # 连接VC
    Connect-VIServer -Server $vcip -Protocol https -User "administrator@vsphere.local" -Password "Admin@123" 

    $getvm = Get-VM $vmName -ErrorAction "SilentlyContinue" # 集群查找是否有此名称的主机
    
    if ($getvm)
    {
	    Write-Host -ForegroundColor Blue "主机名已存在： $vmName"
	    $datetime=Get-Date
	    $content="$datetime 主机名已存在： $vmName"
	    continue
    }
    else
	    {
        # 自定义规范配置 IP，首先要在 vcenter 里面创建一个没有 NIC 的虚拟机自定义规范
        Get-OSCustomizationSpec $vmSpec | New-OSCustomizationNicMapping -IpMode UseStaticIP -IpAddress $vmIP -SubnetMask $vmMask -DefaulTGateway $vmGateway
	    $Note = "系统：" + $vmSpec + "，主机名：" + $vmName + "，IP地址：" + $vmIP + "，负责人：" + $admin + "，创建时间:" +$date

	    # 通过模板部署虚拟机
	    New-vm -Name $vmName -Template $vmTemplate -StorageFormat "Thin" -Datastore $vmDatastore -OSCustomizationspec $vmSpec  -Pool $Pool -Notes $Note -Confirm:$false
	
	    # 配置vCPU ，内存 
        Set-VM -VM $vmName -NumCpu $vmCpu -MemoryGB $vmMemory -Confirm:$false

	    # 添加磁盘
	    if ( $vmDisk -eq "" -or $vmDisk -eq 0 )
	    { 
	    }
	    else
	    {
		    Get-VM $vmName | New-HardDisk -CapacityGB $vmDisk -Persistence persistent -DiskType Flat -StorageFormat Thin -Confirm:$false
	    }

	    # 修改为所需网络标签，且设置网卡打开电源时连接
	    Get-VM $vmName | Get-NetworkAdapter | Set-NetworkAdapter -NetworkName $vmNetworkName -StartConnected:$true -Confirm:$false

        # 删除规范中原网络相关配置
        Get-OSCustomizationSpec $vmSpec | Get-OSCustomizationNicMapping | Remove-OSCustomizationNicMapping -Confirm:$false
	
	    # 开机
	    Start-VM $vmName -Confirm:$false

	    # 定时1分钟
	    sleep -s (5*1)
	    }

    #断开连接
    Disconnect-VIServer $vcip -confirm:$false
}

