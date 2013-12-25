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

angels = {}
newangels = []
allangels = {}

try:
  with io.open('angels.json', 'r', encoding='utf-8') as f:
    angels = json.load(f)
except:
  pass

r = s.get(conf['engelsystemurl'] + '?p=user_messages', verify = False)

soup = BeautifulSoup(r.text)
angelids = soup.findAll('option')
for angel in angelids:
  allangels[angel.get('value')] = angel.text

r = s.get(conf['engelsystemurl'], params = shiftdatapayload, verify = False)

soup = BeautifulSoup(r.text)
entries = soup.findAll('td', {'class': 'entries'})

for entrieslist in entries:
  entry = entrieslist.text.split(': ')
  entry = entry[1].split(', ')
  for singleentry in entry:
   if singleentry.find(" needed") == -1:
    if singleentry not in newangels:
      newangels.append(singleentry)
      print 'Found angel ' + singleentry + ' found.'


for angel in allangels:
  if allangels[angel] in newangels:
    if angel not in angels:
      messagepayload = {'to': (conf['sendmessagesto'] if ('sendmessagesto' in conf) else angel), 'text': conf['messagetext'].replace('###name###', allangels[angel]), 'submit': 'save'}
      s.post(conf['engelsystemurl'] + '?p=user_messages&action=send', params = messagepayload, verify = False)
      print 'Sent message to angel ' + allangels[angel] + ' (' + angel + ').'
      angels[angel] = allangels[angel]

with io.open('angels.json', 'w', encoding='utf-8') as f:
  f.write(unicode(json.dumps(angels, ensure_ascii=False)))
