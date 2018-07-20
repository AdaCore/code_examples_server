#!/usr/bin/env sh

# Prevent unprivilegeds from writing to /tmp
lxc exec safecontainer -- chmod 755 /tmp/

# Prevent the container from having internet access
lxc exec safecontainer -- ifconfig eth0 down
