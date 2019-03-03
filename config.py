config = {
  'bash': {
    'install': False,
    'packages': [
      'xorriso',
      'cpio',
      'genisoimage',
      'wget',
      'aria2'
    ],
    'destination': './isofiles',
    'torrent_url': 'https://cdimage.debian.org/debian-cd/current/amd64/bt-cd/debian-9.8.0-amd64-netinst.iso.torrent',
    'torrent_file': 'debian-9.8.0-amd64-netinst.iso.torrent',
    'iso_src_file': 'debian-9.8.0-amd64-netinst.iso',
    'output_filename': 'preseed-debian-9.8.0-amd64-netinst.iso',
    'artefacts': [
      'vmlinuz',
      'initrd.gz',
      'preseed-debian-9.8.0-amd64-netinst.iso',
      'debian-9.8.0-amd64-netinst.iso',
      'debian-9.8.0-amd64-netinst.iso.torrent',
      'preseed.cfg',
#       'build.log'
    ]
  },
  'preseed': {
    "hostname": "debian",
    "domain": "debian.localdomain",
    "locale": "en_US",
    "keymap": "us",
    "interface": {
      "type": "auto"
    },
    "mirror": "ftp.nl.debian.org",
    "root": {
      "create": True,
      "password": "ok"
    },
    "user": {
      "create": True,
      "fullname": "Eduard Generalov",
      "username": "egeneralov",
      "password": "ok"
    },
    "clock": {
      "utc": True,
      "zone": "UTC",
      "ntp": {
        "enabled": True,
        "server": "0.debian.pool.ntp.org"
      }
    },
    "partman": {
      "remove": {
        "lvm": True,
        "md": True
      },
      "method": "regular",
      "recipe": "auto",
      "expert_recipe": "root :: 40 300 100000000 ext4 $primary{ } $bootable{ } method{ format } format{ } use_filesystem{ } filesystem{ ext4 } mountpoint{ / } .",
      "auto": True,
      "noswap": True
    },
    "apt": {
      "auto": True,
      "upgrade": "full-upgrade",
      "recommends": False,
      "non_free": True,
      "contrib": True,
      "use_mirror": True,
      "security_host": "security.debian.org",
      "services_select": [
        "security",
        "updates"
      ],
      "include": [
        "openssh-server",
        "ca-certificates",
        "curl",
        "wget",
        "acpid",
        "acpi-support-base",
        "python-pip"
      ],
      "popularity_participate": False
    },
    "grub": {
      "bootdev": "/dev/sda",
      "only_debian": True
    },
    "commands": {
      "late": "in-target echo echo GRUB_CMDLINE_LINUX_DEFAULT=\"console=tty0 console=ttyS0,115200n8 serial\" | tee -a /etc/default/grub; in-target update-grub;"
    },
    "reboot": "note",
    "poweroff": True
  }
}
