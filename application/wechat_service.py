from flask import Flask, jsonify, request
from .utils.util import *


app = Flask(__name__)

@app.route('/message', methods=['POST'])
def message():
  """ 
  Service entrance 
  args:
    {'recipient' : ['email1','email2'], 'msg' : 'message'}
    recipient : optional, missing recipient, default to all
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
  user_email = params['recipient']
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

  params['recipient'] = usersID
  send_wechat(params)
  return jsonify({'msg':'success'}), 201
