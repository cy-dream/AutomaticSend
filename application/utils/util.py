import json
import yaml
import pymongo
import requests as req


with open('wechat_msg.yml') as config:
  param = yaml.load(config)
  mongo = param['mongo']


user_information = (mongo['host'], mongo['database'])

class mongo_database():
  def __init__(self, config):
    self.client = None
    self.config = config
  def __enter__(self):
    host, dbName = self.config
    self.client = pymongo.MongoClient(
      host,
      27017
    )
    return self.client
  def __exit__(self, *args):
    self.client.close()


def get_userID(user_email):
  """
    Get the corresponding user_id by user_email
    return "id | id1 | id2", [email, email2, email3]
  """
  usersID = ''
  exist_user_email = set()  
  with mongo_database(config=user_information) as client:
    collection = client[user_information[1]][mongo['collection']]
    cursor = collection.find({'email':{'$in':user_email}})
    for x in cursor:
      usersID += x['userID'] + '|'
      exist_user_email.add(x['email'])
  return usersID, exist_user_email

def send_wechat(params):
  """ wechat invoke interface """
  url="https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token="+get_token()
  values ={
    "touser": params['recipients'],
    "msgtype": "text",
    "agentid": param['wechat']['agentid'],
    "text": {
      "content": params['msg']
    },
    "safe":0
  }
  data = json.dumps(values, ensure_ascii=False)
  re = req.post(url, data.encode('utf-8'))
  return re.text


def get_token():
  """ get token """
  url='https://qyapi.weixin.qq.com/cgi-bin/gettoken'
  values = {
    'corpid' : param['wechat']['corpid'],
    'corpsecret': param['wechat']['corpsecret']
  }
  re = req.post(url, params=values)
  data = json.loads(re.text)
  return data["access_token"]
