import json
from jinja2 import Template

def generate_bash(config, tmp, template = 'templates/generate.bash.j2'):
  with open(template) as f:
    template = Template(f.read())
  return template.render(**config, tmp=tmp)


if __name__ == '__main__':
  config = {
    'install': True,
    'packages': [
      'xorriso',
      'cpio',
      'genisoimage',
      'wget',
      'aria2'
    ],
    'destination': './isofiles',
    'torrent_url': 'https://cdimage.debian.org/debian-cd/current/amd64/bt-cd/debian-9.7.0-amd64-netinst.iso.torrent',
    'torrent_file': 'debian-9.7.0-amd64-netinst.iso.torrent',
    'iso_src_file': 'debian-9.7.0-amd64-netinst.iso',
    'output_filename': 'preseed-debian-9.7.0-amd64-netinst.iso',
    'preseed_url': 'https://gitlab.com/egeneralov/debian-preseed-iso/raw/master/preseed.cfg',
    'artefacts': [
      'isofiles/install.amd/vmlinuz',
      'isofiles/install.amd/initrd.gz',
      'preseed-debian-9.7.0-amd64-netinst.iso'
    ]
  }
  
  
  print(
    generate_bash(config)
  )
