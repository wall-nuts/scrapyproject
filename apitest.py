#encoding:utf-8
import requests,json

postdata={'key':'31d6960f5cef4fd1b16a03188b318f62','info':'','userid':'1'}

r = requests.post('http://www.tuling123.com/openapi/api',data=postdata)
d = json.loads(r.text)
print(d['text'])