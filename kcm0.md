---
title: Proxmox User Management
date: 2022-11-30
tags:
    - proxmox
    - terraform
    - user-management
    - permissions
    - pveum
---
Role Based Access Control (RBAC) in Proxmox is useful for creating "service accounts" to incorporate the Proxmox api in automation. This example creates a role/user for use with the Proxmox Terraform plugin.

## Create a role
```bash
pveum role add TerraformProv -privs "VM.Allocate VM.Clone VM.Config.CDROM VM.Config.CPU VM.Config.Cloudinit VM.Config.Disk VM.Config.HWType VM.Config.Memory VM.Config.Network VM.Config.Options VM.Monitor VM.Audit VM.PowerMgmt Datastore.AllocateSpace Datastore.Audit"
```

## Create a user and set password
```bash
pveum user add terraform-prov@pve --password <password>
```

## Associate role with user
```bash
pveum aclmod / -user terraform-prov@pve -role TerraformProv
```

## Reference
- https://pve.proxmox.com/wiki/User_Management
- https://registry.terraform.io/providers/Telmate/proxmox/latest/docs


