import hashlib
import requests
import json

alphabet = 'abcdefghijklmnopqrstuvwxyz0123456789'

u = 'pkkao'

def solve(name):
  x = hashlib.md5(u + name).hexdigest()
  solution = ''
  for i in range(4):
    answer += alphabet[int(x[i*4:i*4 + 4], 16) % 36]
  return {'name': name, 'solution':answer}

if __name__ == '__main__':
  solutions = []

  for i in range(11):
    r = requests.get('https://captcha.delorean.codes/u/pkkao/challenge')
    x = json.loads(r.text)['images']
    for c in x:
      solutions.append(solve(c['name']))

  final = {'solutions':solutions}
  r = requests.post('https://captcha.delorean.codes/u/pkkao/solution', data = json.dumps(final))
  print(r.text)
