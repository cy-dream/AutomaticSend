from flask import Flask, jsonify, request
from .utils.util import *
import json

app = Flask(__name__)

@app.route('/message', methods=['POST'])
def message():
  """ 
  Service entrance 
  args:
    {'recipients' : ['email1','email2'], 'msg' : 'message'}
    recipients : optional, missing recipients, default to all
    msg : must
  returns:
    The parameter must contain msg field. else return {'errmsg':'missing msg in parameters'}
    if Email does not exist
      return {'errmsg':'Email does not exist','invalid_email': ['email1', 'email2']}
    else:
      return { 'msg': 'success' }
  """
  params = request.get_json(force=True,silent=True)
  if not params or not 'msg' in params:
    return jsonify({'errmsg':'missing msg in parameters'}), 400
  user_email = params['recipients']
  if user_email:
    usersID, exist_user_email = get_userID(user_email)
  else:
    usersID = '@all'

  not_exist_user_email = list(set(user_email).difference(exist_user_email))
  if not_exist_user_email:
    error = {
      'errmsg':'Email does not exist',
      'invalid_email':not_exist_user_email
    }
    return jsonify(error), 400

  params['recipients'] = usersID
  result = json.loads(send_wechat(params))
  if result.get('errcode') != 0:
    return jsonify({'msg':'failure'}), 400

  return jsonify({'msg':'success'}), 201
