#!/usr/bin/env sh

# Kill all old processes
lxc exec safecontainer -- killall  -u unprivileged --older-than 30s -signal KILL

# Delete all old directories
lxc exec safecontainer -- find /tmp/ -mindepth 1  -type d -mmin +1 -exec rm -rf {}  \;
