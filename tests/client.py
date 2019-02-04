import requests


with open('test.json') as f:
  payload = f.read()


# r = requests.post(
#   'http://127.0.0.1:8080/build/',
#   data = payload
# )

r = requests.post(
  'https://debian-preseed-generator.herokuapp.com/build/',
  data = payload
)


print(r)
print(r.json())

if not r.ok:
  if r.status_code == 400:
    raise Exception('Failed. Bad payload?')
  raise Exception('Failed. Server error.')


for url in r.json()['artefacts']:
  file_name = url.split('/')[5]
  file_request = requests.get(url)
  if file_request.ok:
    with open(file_name, 'wb+') as f:
      f.write(file_request.content)
  else:
    print(file_name, url, file_request.status_code)


