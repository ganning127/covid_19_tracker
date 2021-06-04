#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import math
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

numbers = ["REPLACE WITH YOUR MAILING LIST"]
email = 'SENDING EMAIL'
pas = 'SENDING EMAIL PASSWORD'
smtp = "smtp.gmail.com"
port = 587
server = smtplib.SMTP(smtp,port)
server.ehlo()
server.starttls()
server.ehlo()
server.login(email,pas)
msg = MIMEMultipart()


result = requests.get("https://www.worldometers.info/coronavirus/country/us/")
src = result.content
soup = BeautifulSoup(src, 'html.parser')

def us_cases():
    us_cases_elems = soup.select('.content-inner > div:nth-child(6) > div:nth-child(2) > span:nth-child(1)')
    print("Getting cases...")
    return us_cases_elems[0].getText()

def us_deaths():
    us_death_elems = soup.select('.content-inner > div:nth-child(7) > div:nth-child(2) > span:nth-child(1)')
    print("Getting deaths...")
    return us_death_elems[0].getText()

def us_recovered():
    us_recovered_elems = soup.select('.content-inner > div:nth-child(8) > div:nth-child(2) > span:nth-child(1)')
    print("Getting recovered...")
    return us_recovered_elems[0].getText()

def percent(number, places):
    ratio = round(number, places)
    hundred = ratio * 100
    percent = str(math.floor(hundred))
    return percent + "%"

cases = us_cases()
deaths = us_deaths()

division_cases = cases.replace(",", "")
division_deaths = deaths.replace(",", "")

recovered = us_recovered()

ratio_of_death = int(division_deaths)/int(division_cases)

percentage_death = percent(ratio_of_death, 2)


def file_maker(filename):
    theFile = open(filename, 'r+')
    number = int(theFile.read())
    theFile.seek(0)
    theFile.truncate(0)
    theFile.write(division_cases)
    theFile.close()
    return number


num = file_maker('us_coronavirus_storage.txt')
difference = int(division_cases) - int(num)
difference = math.floor(difference)
difference_list = list(str(difference))
difference_list.reverse()

for i in range(3, len(difference_list), 4):
    difference_list.insert(i, ",")
difference_list.reverse()
difference = "".join(difference_list)
 
#time and date
today = datetime.now()
formatToday = today.strftime("%B %d, %Y")
message = "\n" + "As of: " + formatToday + "\n" + "\n" + "CASES: " + str(cases) + "\n" + "DEATHS: " + str(deaths) + "\n" + "RECOVERED: " + str(recovered) + "\n" + "DEATH RATE: " + str(percentage_death) + "\n" + "INCREASE + " + str(difference) + "  "

print("Sending messages...")
for number in numbers:
    msg['From'] = email
    msg['To'] = number
    msg['Subject'] = "US COVID-19 CASES:"
    body = message
    msg.attach(MIMEText(body,'plain'))

    sms=msg.as_string()
    server.sendmail(email,number,sms)

print("Messages sent.")
server.quit()
