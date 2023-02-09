import requests
import json
import datetime
import pytz
import smtplib
from email.mime.text import MIMEText
from email.header import Header

def send_mail(str):
	mail_host="SMTP_SERVER"
	mail_user="SMTP_USER"
	mail_pass="SMTP_PASSWD"
	sender = 'SENDER_ADDRESS'
	receivers = ['RECIPIENT1','RECIPIENT2']

	message = MIMEText(str, 'plain', 'utf-8')
	message['From'] = Header("SENDER_NAME", 'utf-8')
	message['To'] =  Header("RECIPIENT_NAME", 'utf-8')

	subject = 'New status detected on Elsevier Tracking System'
	message['Subject'] = Header(subject, 'utf-8')

	smtpObj = smtplib.SMTP_SSL(mail_host,465)
	smtpObj.login(mail_user,mail_pass)
	smtpObj.sendmail(sender, receivers, message.as_string())

fr=open('./latest_status.txt', 'r')

url = "https://***.execute-api.us-east-1.amazonaws.com/tracker/UUID"

payload={}
headers={}

response = requests.request("GET", url, headers=headers, data=payload)

json_result = json.loads(response.text)

i=-1
nowdate=fr.read()
fr.close()

REArray=json_result["ReviewEvents"]
REArray.sort(key=lambda x:x["Date"])

try:
	while REArray[i]["Date"]>int(nowdate):
		send_mail("An updated status detected on Elsevier at "+datetime.datetime.fromtimestamp(REArray[i]["Date"],pytz.timezone("Asia/Shanghai")).strftime('%Y-%m-%d %H:%M:%S')+" UTC +8. Event Description: "+REArray[i]["Event"])
		i-=1
except:
	pass

fw=open('./latest_status.txt', 'w')
fw.write(str(json_result["ReviewEvents"][-1]["Date"]))
fw.close()