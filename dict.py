#!/usr/bin/env python
#-*- coding: utf-8 -*-

# yum install xclip python-xlib python-notify  
# apt-get install xclip python-xlib python-notify  

import os
import sys
from Xlib import X,XK,display
from Xlib.ext import record
from Xlib.protocol import rq
import urllib2
import json
import pynotify

record_dpy=display.Display()
# Create a recording context; we only want key and mouse events
ctx = record_dpy.record_create_context(
0,
[record.AllClients],
[{
'core_requests': (0, 0),
'core_replies': (0, 0),
'ext_requests': (0, 0, 0, 0),
'ext_replies': (0, 0, 0, 0),
'delivered_events': (0, 0),
'device_events': (X.KeyPress, X.MotionNotify),
'errors': (0, 0),
'client_started': False,
'client_died': False,
}])

pre_word="" #上次翻译的词语
appkey="Your AppKey" #百度翻译申请的appKey

def viewTranslate():
	global pre_word
	global appkey
	url="http://fanyi.youdao.com/translate?smartresult=dict&smartresult=rule&smartresult=ugc&sessionFrom=dict.top' -d 'type=AUTO& i=%s&doctype=json&xmlVersion=1.4&keyfrom=fanyi.web&ue=UTF-8&typoResult=true&flag=false" % (pre_word)
	# url="http://openapi.baidu.com/public/2.0/bmt/translate?client_id=%s&q=%s&from=auto&to=auto" % (appkey,pre_word)
	result=urllib2.urlopen(url).read()
	json_result=json.loads(result)
	pynotify.init("AutoTranslate")
	try:
		error_msg=json_result["error_msg"]
		query=json_result["query"]
		bubble=pynotify.Notification('"'+query+'"的翻译出错',error_msg)
		print error_msg
		bubble.show()
	except:
		trans_result=json_result["translateResult"]
		print trans_result
		src=trans_result[0][0]["src"]
		dst=trans_result[0][0]["tgt"]		
		bubble=pynotify.Notification('"'+src+'"的翻译结果',dst)
		bubble.show()

def record_callback(reply):
	global pre_word
	if reply.category != record.FromServer:
		return
	if reply.client_swapped:
		#print "* received swapped protocol data, cowardly ignored"
		return
	if not len(reply.data) or ord(reply.data[0]) < 2:# not an event
		return
	data = reply.data
	while len(data):
		event, data = rq.EventField(None).parse_binary_value(data, record_dpy.display, None, None)
		if event.type == X.ButtonRelease:
			pipe = os.popen("xclip -o")
			text = pipe.readline()
			pipe.readlines()    #清空管道剩余部分
			pipe.close()
			text=text.strip('\r\n\x00').lower().strip()
			if pre_word != text and text!="":
				pre_word=text
				viewTranslate()
            
def gettext():
	os.system("xclip -f /dev/null")           #清空剪切板
	record_dpy.record_enable_context(ctx,record_callback)
  	record_dpy.record_free_context(ctx)
  
def main():
	gettext()
  
if __name__=='__main__':
  	main()
