import urllib2,json
import telegram

from bs4 import BeautifulSoup
import time
import sendgrid
from twilio.rest import Client
import os
from sendgrid.helpers.mail import 

url = "MASKED_URL"
request = urllib2.Request(url)
page = urllib2.urlopen(request)
soup = BeautifulSoup(page,"lxml")

status="down"

try :
	status_string=(soup.find_all('p')[0].get_text())
except IndexError:
        status="open"

print('Status is ',status)

url = "http://MASKED_URL/LatestBTCRate?currency=MASKED"
request = urllib2.Request(url)
page = urllib2.urlopen(request)
soup = BeautifulSoup(page,"lxml")
buystring=(soup.find_all('p')[0].get_text())
buystring=buystring.split('.')[0]
buyint=int(buystring.replace(',',''))
buyintreal = buyint*1.082
buyprice = buyint*(1.082)+0.0004*(buyintreal*(buyintreal/200000))
print(buyprice)

url = "https://MASKED/api/ticker"

try :
	req =urllib2.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
	response = urllib2.urlopen(req)
	data = json.loads(response.read().decode('utf-8'))
	sellprice_MASKED =  int(float(data['stats']['BTC']['highest_bid']))*0.9764
	profit_MASKED = sellprice_MASKED-buyprice
except urllib2.HTTPError as err:
	profit_MASKED=0

profit_percentage = profit_MASKED/sellprice_MASKED*100


if(   profit_percentage > 3 and status=="open" ):
        sg = sendgrid.SendGridAPIClient(apikey="MASKED")
        from_email = Email("MASKED@MASKED.com")
        to_email = Email("MASKED@MASKED.com")
        subject = "UPSIDE +  " + str(profit_percentage)
        content = Content("text/plain", "Just Alerting")
        mail = Mail(from_email, subject, to_email, content)
        response = sg.client.mail.send.post(request_body=mail.get())

	account_sid = "MASKED"
	auth_token = "MASKED"
	client = Client(account_sid, auth_token)


	bot = telegram.Bot(token="MASKED")
	bot.send_message(chat_id='MASKED', text=subject)
