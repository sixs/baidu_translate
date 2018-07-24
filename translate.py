#encoding: utf-8
'''
author: sixseven
date: 2018-07-24
topic: 百度翻译
contact: 2557692481@qq.com
desc: 1、进行post请求前需要进行两次首页get请求，第一次获取cookie，第二次根据cookie刷新token
		2、sign参数加密中：window[l]其中l="gtk"，window["gtk"]是在外部赋值为"320305.131321201"，所以需手动赋值或直接替换
'''
import re
import execjs
import requests
from copy import deepcopy
import json

def get_sign(value):
	'''
	获取sign参数
	'''
	with open("./decrypt.js", encoding='utf-8', mode='r') as fp:
		js = fp.read()
	ctx = execjs.compile(js)
	sign = ctx.call('get_sign', value)
	return sign

def translate(value, from_lan, to_lan):
	'''
	翻译
	'''
	session = requests.Session()
	proxies = {
		'http': '127.0.0.1:3128'
	}
	headers = {
		'Host':'fanyi.baidu.com',
		'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
	}

	index_url = 'http://fanyi.baidu.com'
	index_headers = deepcopy(headers)

	# 第一次访问首页获取cookie
	index_req = session.get(index_url, headers=index_headers, proxies=proxies)
	cookie_match = re.findall(r'BAIDUID=[A-Z0-9:=]+;', index_req.headers['Set-Cookie'])
	cookie = cookie_match[0]

	# 第二访问首页刷新token
	index_req = session.get(index_url, headers=index_headers, proxies=proxies)
	token_match = re.findall(r'token: \'([0-9a-z]{32})\',', index_req.text)
	token = token_match[0]

	# post请求进行翻译
	trans_url = 'http://fanyi.baidu.com/v2transapi'
	post_headers = deepcopy(headers)
	post_headers['Origin'] = 'http://fanyi.baidu.com'
	post_headers['Cookie'] = cookie
	sign = get_sign(value)
	data = {
		'from':from_lan,
		'to':to_lan,
		'query':value,
		'transtype':'realtime',
		'simple_means_flag':3,
		'sign':sign,
		'token':token,
	}
	post_req = session.post(trans_url, headers=post_headers, data=data, proxies=proxies)
	json_data = json.loads(post_req.text)
	if 'error' in json_data:
		print('error')
	else:
		print('success')
		print(json_data)

def main():
	value = 'hello'
	from_lan = 'en'
	to_lan = 'zh'
	translate(value, from_lan, to_lan)

if __name__ == '__main__':
	main()
