#!/usr/bin/env sh

all: create_container setup_container protect_container

destroy_container:
	lxc list | grep safecontainer && lxc delete --force safecontainer || true

create_container:
	# create the container
	lxc list | grep safecontainer || \
          (lxc launch ubuntu:`cat /etc/issue | cut -d ' '  -f2 | cut -d '.' -f 1-2` safecontainer -s default && \
	# wait a bit to allow network to come up \
	sleep 5)

setup_container:
	# install this first!
	lxc exec safecontainer -- apt install make

        # push the payload
	tar cf - container_payload/ | lxc exec safecontainer tar xf -

	# run the makefile on the container
	lxc exec safecontainer -- bash -c "cd /root/container_payload ; make -f Makefile.safecontainer"

protect_container:
	# Prevent the container from having internet access
	lxc exec safecontainer -- bash -c "cd /root/container_payload ; make -f Makefile.safecontainer protect"

