# -*- coding: utf-8 -*-
from datetime import datetime
from lxml import etree
import requests
import json
import yaml
import re

with open('../wechat_msg.yml') as config:
  param = yaml.load(config)
  recipients = param['recipients']

# send content
def send_msg(recipient, msg):
  url = 'http://127.0.0.1:5000/message'
  values = {
    'recipients' : recipient,
    'msg' : msg
  }
  headers = {'content-type': 'application/json'}
  r = requests.post(url, data=json.dumps(values), headers=headers)

def get_link():
  with open('num.txt', 'r') as f:
    old_num = int(f.read())
  url = 'https://www.xxbiquge.com/0_547/'
  response = requests.get(url)
  response.encoding = 'utf-8'
  html = etree.HTML(response.text)
  tag_links = html.xpath('//*[@id="list"]/dl/dd/a')
  for link in tag_links[-10:]:
    title = link.xpath('./text()')
    lianjie = 'https://www.xxbiquge.com' + link.xpath('./@href')[0]
    title_num = re.search(r'\d*', title[0], re.M|re.I)
    num = int(title_num.group(0))
    if num > old_num:
      content = get_text(lianjie)
      content_send(title, content)
      with open('num.txt', 'w') as f:
        f.write(str(num))

# The content is too long, divided into four sends
# The maximum sending length is 2048 bytes    
def content_send(title, content):
  if '正在手打中' not in content:
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    content_length = len(content) // 4
    accepter = recipients['cydream']
    for num in range(1, 5):
      send_msg(accepter, '标题：'+title[0]+ str(num) +'\n时间：'+now+'\n'+content[content_length*(num-1):content_length*num])

# Gets the text and removes all tags and Spaces
def get_text(url):
  response = requests.get(url)
  response.encoding='utf-8'
  content = re.search(r'(<div id="content">)([\s\S]*)(<div class="bottem2">)', str(response.text), re.M|re.I)
  dr = re.compile(r'<[^>]+>',re.S)
  content = dr.sub('', content.group(2))
  return content.replace('&nbsp;','').replace('nbsp','')

if __name__ == '__main__':
  get_link()
  # test send message
  #send_msg(recipients['cydream'], 'I Love You Si')