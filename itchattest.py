#coding=utf8
import requests
import itchat

KEY = '31d6960f5cef4fd1b16a03188b318f62'

def get_response(msg):
    apiUrl = 'http://www.tuling123.com/openapi/api'
    data = {
        'key'    : KEY,
        'info'   : msg,
        'userid' : 'wechat-robot',
    }
    try:
        r = requests.post(apiUrl, data=data).json()
        return r.get('text')
    except:
        return

@itchat.msg_register(itchat.content.TEXT,isGroupChat=True)
def tuling_reply(msg):
    if(msg['isAt']):
        defaultReply = 'I received: ' + msg['Text']
        reply = get_response(msg['Text'])
        return reply or defaultReply
    else:
        return

itchat.auto_login()
itchat.run()