#-*- coding: UTF-8 -*-
import requests
from bs4 import BeautifulSoup
import re
import urlparse
import json
import io

conf = {}

with io.open('config.json', 'r', encoding='utf-8') as f:
	conf = json.load(f)


loginpayload = {'p': 'login', 'nick': conf['username'], 'password': conf['password'], 'submit': 'Login'}
shiftdatapayload = {'p': 'user_shifts', 'start_day': conf['startday'], 'end_day': conf['endday'], 'rooms[]': conf['room'], 'types[]': conf['angeltype'], 'filled[]': ['0', '1']}

s = requests.Session()
s.post(conf['engelsystemurl'], params = loginpayload, verify = False)
r = s.get(conf['engelsystemurl'], params = shiftdatapayload, verify = False)

soup = BeautifulSoup(r.text)
entries = [entries.findAll(href=re.compile("\?p=user_myshifts")) for entries in soup.findAll('td', {'class': 'entries'})]

angels = {}
newangels = {}

try:
  with io.open('angels.json', 'r', encoding='utf-8') as f:
    angels = json.load(f)
except:
  pass


for users in entries:
  for user in users: 
    params = urlparse.parse_qs(urlparse.urlparse(user['href']).query)
    if not angels.has_key(params['id'][0]):
      newangels[params['id'][0]] = user.text
      angels[params['id'][0]] = user.text
      print 'New angel ' + user.text + ' (' + params['id'][0] + ') found.'
      
for angelid in newangels:
  messagepayload = {'to': (conf['sendmessagesto'] if ('sendmessagesto' in conf) else angelid), 'text': conf['messagetext'].replace('###name###', newangels[angelid]), 'submit': 'save'}
  s.post(conf['engelsystemurl'] + '?p=user_messages&action=send', params = messagepayload, verify = False)
  print 'Sent message to angel ' + newangels[angelid] + ' (' + angelid + ').'

with io.open('angels.json', 'w', encoding='utf-8') as f:
  f.write(unicode(json.dumps(angels, ensure_ascii=False)))
