#!/usr/bin/env python3
import sys
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import math
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import data_getter
import time

EMAIL = 'REPLACE WITH SENDING EMAIL'
PASS = 'REPLACE WITH SENDING EMAIL PASSWORD'
SMTP = "smtp.gmail.com"
PORT = 587
SERVER = smtplib.SMTP(SMTP,PORT)

SERVER.ehlo()
SERVER.starttls()
SERVER.login(EMAIL, PASS)
msg = MIMEMultipart()

def get_numbers():
    final_list = []
    str_to_gateway = {
        "T-Mobile": "@tmomail.net",
        "AT&T": "@txt.att.net",
        "Cricket": "@mms.cricketwireless.net",
        "Sprint": "@messaging.sprintpcs.com",
        "Verizon": "@vtext.com"
    }

    with open("current_users.txt", "r+") as file:
        total_nums = []

        all_numbers = file.readlines()
        for index, number in enumerate(all_numbers):
            all_numbers[index] = number.strip("\n")


        data = data_getter.main()
        if data == "NO DATA" or data == {}:
            while '' in all_numbers:
                all_numbers.remove('')
            return all_numbers

        else:
            new_nums = []

            for number in data:
                completed_concat = number + str_to_gateway[data[number]]
                final_list.append(completed_concat)

            for test_num in final_list:
                if test_num not in all_numbers:
                    file.write(test_num + "\n")
                    new_nums.append(test_num)

            file.seek(0)
            total_nums = file.readlines()

            for i, n in enumerate(total_nums):
                total_nums[i] = n.strip("\n")

            while '' in total_nums:
                total_nums.remove('')

            return total_nums

NUMBERS = get_numbers()

class Webpage:
    result = requests.get("https://www.worldometers.info/coronavirus/country/us/")
    src = result.content

    def __init__(self):
        self.soup = BeautifulSoup(self.src, 'html.parser')

    def us_cases(self):
        us_cases_elems = self.soup.select('.content-inner > div:nth-child(6) > div:nth-child(2) > span:nth-child(1)')
        return us_cases_elems[0].getText()

    def us_deaths(self):
        us_deaths_elems = self.soup.select('.content-inner > div:nth-child(7) > div:nth-child(2) > span:nth-child(1)')
        return us_deaths_elems[0].getText()

    def us_recovered(self):
        us_recovered_elemns = self.soup.select(".content-inner > div:nth-child(8) > div:nth-child(2) > span:nth-child(1)")
        return us_recovered_elemns[0].getText()

    def handle_file(self, filename, cases_to_write):
        the_file = open(filename, 'r+')
        number = int(the_file.read())
        the_file.seek(0)
        the_file.truncate(0)
        the_file.write(cases_to_write)
        the_file.close()
        return number

    def make_percent(self, number, places):
        ratio = round(number, places)
        hundred = ratio * 100
        percent = str(math.floor(hundred))
        return percent + "%"

    def format_difference(self, difference):
        difference_list = list(str(difference))
        difference_list.reverse()
        for i in range(3, len(difference_list), 4):
            difference_list.insert(i, ",")
        difference_list.reverse()
        difference = "".join(difference_list)
        return difference

    def make_message(self, cases, deaths, recovered, death_rate, difference_in_cases):
        today = datetime.now()
        format_today = today.strftime("%B %d, %Y")
        message = "\n" + "As of: " + format_today + "\n" + "\n" + "CASES: " + str(cases) + "\n" + "DEATHS: " + str(deaths) + "\n" + "RECOVERED: " + str(recovered) + "\n" + "DEATH RATE: " + str(death_rate) + "\n" + "INCREASE + " + str(difference_in_cases) + "  "
        return message



#initializes webpage
us_corona_page = Webpage()

#cases, deaths, recovered
cases = us_corona_page.us_cases()
cases_for_message = cases

deaths = us_corona_page.us_deaths()
deaths_for_message = deaths

recovered = us_corona_page.us_recovered()

#convert casees and deaths to a value that can be cast to int
cases = cases.replace(",", "")
deaths = deaths.replace(",", "")

#death rate
death_rate = int(deaths) / int(cases)
death_rate = us_corona_page.make_percent(death_rate, 2)

#previous day's cases & increase in cases
previous_day_cases = us_corona_page.handle_file('us_scraper_storage.txt', cases)

difference_in_cases = int(cases) - previous_day_cases
difference_in_cases = math.floor(difference_in_cases)
difference_in_cases = us_corona_page.format_difference(difference_in_cases)

#message
MESSAGE = us_corona_page.make_message(cases=cases_for_message, deaths=deaths_for_message, recovered=recovered, death_rate=death_rate, difference_in_cases=difference_in_cases)

#sending messages
for number in NUMBERS:
    msg['From'] = EMAIL
    msg['To'] = number
    msg['Subject'] = "US COVID-19 CASES"
    body = MESSAGE
    msg.attach(MIMEText(body, 'plain'))

    sms = msg.as_string()
    SERVER.sendmail(EMAIL, number, sms)
    time.sleep(2)

SERVER.quit()
