import json
from jinja2 import Template

def generate_preseed_cfg(config, template = 'templates/preseed.cfg.j2'):
  with open(template) as f:
    template = Template(f.read())
  return template.render(**config)

if __name__ == '__main__':
  with open('preseed.json') as f:
    config = json.loads(f.read())
  
  print(
    generate_preseed_cfg(config)
  )
