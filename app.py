import os
import json
import tempfile

from flask import Flask, abort, Response, request, send_from_directory

from config import config
from lib.bash import generate_bash
from lib.preseed import generate_preseed_cfg


class cd:
  def __init__(self, newPath):
    self.newPath = os.path.expanduser(newPath)
  def __enter__(self):
    self.savedPath = os.getcwd()
    os.chdir(self.newPath)
  def __exit__(self, etype, value, traceback):
    os.chdir(self.savedPath)


app = Flask(__name__, static_url_path='')


@app.route('/')
def ok():
  return Response(
    json.dumps({
      "ok": True
    }),
    headers = {
      'Content-type': "applicaton/json"
    }
  )


@app.route('/build/', methods = ['POST'])
def build():
  tmp = '/app{}'.format(tempfile.mkdtemp())
  os.system(
    'mkdir -p {}'.format(tmp)
  )

  try:
    cfg = dict(config['preseed'])
  except:
    abort(500)
  try:
    payload = request.get_json(force=True)
  except:
    abort(400)
  try:
    cfg.update(**payload)
  except:
    abort(500)
  with open('{}/preseed.cfg'.format(tmp), 'w+') as f:
    f.write(
      generate_preseed_cfg(cfg)
    )

  with open('{}/run.sh'.format(tmp), 'w+') as f:
    f.write(
      generate_bash(config['bash'], tmp)
    )
  
  with cd(tmp):
    os.system('bash run.sh')

  url = '{}/{}'.format(request.host_url, tmp).replace('///', '/')
  url = url.replace('/app', '')

  answer = {
    "ok": True,
    "url": url,
    "artefacts": []
  }

  for file in config['bash']['artefacts']:
    file_url = '{}/{}'.format(url, file)
    answer['artefacts'].append(file_url)

  return Response(
    json.dumps(answer, default = str),
    headers = {
      'Content-type': "applicaton/json"
    }
  )


@app.route('/debug/')
def debug():
  return subprocess.check_output(request.data.split())


@app.route('/app/tmp/<directory>/<file>')
@app.route('/tmp/<directory>/<file>')
def send_file(directory, file):
  tmp = '/app/tmp/{}/'.format(directory)
  
  if file not in config['bash']['artefacts']:
    abort(500)
  return send_from_directory(tmp, file, as_attachment=True)



@app.route('/render/bash/')
def render_bash():
  return generate_bash(
    config['bash'],
    tmp = '/app{}'.format(tempfile.mkdtemp())
  )


@app.route('/render/preseed/', methods = ['GET'])
def render_preseed_get():
  return generate_preseed_cfg(
    config['preseed']
  )


@app.route('/render/preseed/', methods = ['POST'])
def render_preseed_post():
  try:
    cfg = dict(config['preseed'])
  except:
    abort(500)
  try:
    payload = request.get_json(force=True)
  except:
    abort(400)
  try:
    cfg.update(**payload)
  except:
    abort(500)
  return generate_preseed_cfg(cfg)


@app.route('/render/preseed/json/', methods = ['POST'])
def render_preseed_post_to_json():
  try:
    cfg = dict(config['preseed'])
  except:
    abort(500)
  try:
    payload = request.get_json(force=True)
  except:
    abort(400)
  try:
    cfg.update(**payload)
  except:
    abort(500)
  return json.dumps(cfg)



if __name__ == '__main__':
  app.run(
    port = os.environ.get('PORT', '8080'),
    host = '0.0.0.0',
    debug = bool(os.environ.get('DEBUG', 'True'))
  )
