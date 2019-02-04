#!/bin/bash -ex

#curl -s 127.0.0.1:8080/build/ -d@test.json | jq "."

rm -f debian-9.7.0-amd64-netinst.iso initrd.gz preseed-debian-9.7.0-amd64-netinst.iso vmlinuz  debian-9.7.0-amd64-netinst.iso.torrent test.img

python3 client.py

qemu-img create test.img 4G

qemu-system-x86_64 -accel hvf -smp 1 -m 1G -net nic -net user \
-cdrom preseed-debian-9.7.0-amd64-netinst.iso \
-hda test.img \
-nographic -serial mon:stdio \
-kernel vmlinuz \
-append "console=ttyS0 hostname=generalov domain=local" \
-initrd initrd.gz



qemu-system-x86_64 -accel hvf -smp 1 -m 1G -net nic -net user \
-hda test.img \
-vnc 0.0.0.0:0 -k en-us \
-nographic -serial mon:stdio


# qemu-system-x86_64 -accel hvf -smp 1 -m 1G -net nic -net user \
# -hda test.img \
# -vnc 0.0.0.0:0 -k en-us \
# -curses



