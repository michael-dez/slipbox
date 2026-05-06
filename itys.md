---
title: Configuring apt Sources
date: 2022-11-30
tags:
    - homelab
    - proxmox
    - debian
    - ubuntu
    - apt
    - sources
    - sourceslist
    - repositories
    - configure
---
# Configuring Debian-like Repositories
The main repository sources list is in the file:
```bash
/etc/apt/sources.list
```
Additional repository lists can be placed in:
```bash
/etc/apt/sources.list.d/
```

## Configure Proxmox to Use Community Repositories
To switch Proxmox from the default enterprise repositories to community repositories, as a user with root permissions, rename:
```bash
/etc/apt/sources.list.d/pve-enterprise.list
```
to
```bash
/etc/apt/sources.list.d/pve-community.list
```
then modify the file contents to look like this:
```bash
deb http://download.proxmox.com/pve bullseye pve-no-subscription
```
Confirm everything works with an `sudo apt update`.
