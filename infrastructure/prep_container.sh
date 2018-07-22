#!/usr/bin/env sh

# Prevent unprivilegeds from writing to /tmp
lxc exec safecontainer -- chmod 755 /tmp/

# Prevent the container from having internet access
lxc exec safecontainer -- ifconfig eth0 down

# Build the preloader and install it on the container
gcc -shared -o /tmp/preloader.so -fPIC preloader.c
lxc file push /tmp/preloader.so safecontainer/
