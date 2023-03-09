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
j=0
nowdate=fr.read()
fr.close()

REArray=json_result["ReviewEvents"]
REArray.sort(key=lambda x:x["Date"])
str_table=""

try:
	while REArray[j]:
		str_table+=str(REArray[j]["Id"])+"\t"+datetime.datetime.fromtimestamp(REArray[j]["Date"],pytz.timezone("Asia/Shanghai")).strftime('%Y-%m-%d %H:%M:%S')+"\t"+REArray[j]["Event"]+"\t\t\t"+str(REArray[j]["Revision"])+"\n"
		j+=1
except:
	pass

try:
	while REArray[i]["Date"]>int(nowdate):
		send_mail("An updated status detected on Elsevier at "+datetime.datetime.fromtimestamp(REArray[i]["Date"],pytz.timezone("Asia/Shanghai")).strftime('%Y-%m-%d %H:%M:%S')+" UTC+0800."+"\r\n"+"Event Description: "+REArray[i]["Event"]+".\r\n"+"View detailed information from API at https://tnlkuelk67.execute-api.us-east-1.amazonaws.com/tracker/4b9b6857-734a-493c-a6e4-396c691b418e and Author Hub at https://track.authorhub.elsevier.com/?uuid=4b9b6857-734a-493c-a6e4-396c691b418e.\r\n\r\n"+"Event ID\t\tTime\t\t\t\tEvent Description\t\t\tRevision"+"\n"+str_table)
		i-=1
except:
	pass

fw=open('./latest_status.txt', 'w')
fw.write(str(json_result["ReviewEvents"][-1]["Date"]))
fw.close()
