#!/usr/bin/env python3

import sys, os
from instascrape import *
import ezsheets
from datetime import datetime

session_id = "REPLACE WITH INSTAGRAM SESSION ID"

headers = {"user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Mobile Safari/537.36 Edg/87.0.664.57",
           "cookie": f"sessionid={session_id};"}

class InstaTracker:
    def __init__(self):
        self.INSTA_INSTAGRAM = Profile("REPLACE WITH INSTAGRAM PROFILE ID")
        self.INSTA_INSTAGRAM.scrape(headers=headers)
        self.SPREADSHEET = ezsheets.Spreadsheet("REPLACE WITH SPREADSHEET ID")
        self.SHEET = self.SPREADSHEET[0]
        print("Getting instagram profile...")

    def getNumberPosts(self):
        print("Getting number of posts...")
        return self.INSTA_INSTAGRAM.posts

    def getFollowing(self):
        print("Getting number of following...")
        return self.INSTA_INSTAGRAM.following

    def getFollowers(self):
        followers = self.INSTA_INSTAGRAM.followers
        print("Getting number of followers... ")
        return followers

    def getDate(self):
        date = datetime.now()
        actualDate = date.strftime("%m/%d/%Y")
        month = date.strftime("%b")
        print("Getting date...")
        return actualDate, month

    def getOpenRow(self):
        print("Analyzing spreadsheet for next avaliable row...")
        for row in range(1,self.SHEET.rowCount):
            cell = 'A' + str(row)
            if self.SHEET[cell] == "":
                return row

    def getIncrease(self, currentFollowers):
        with open("insta_storage.txt", 'r+') as file:
            oldFollowers = int(file.read())
            file.truncate(0)
            file.seek(0)
            file.write(str(currentFollowers))

        difference = currentFollowers - oldFollowers
        if difference > 0:
            difference = "+" + str(difference)
        elif difference < 0:
            difference = "-" + str(difference)
        return difference

    def updateSpreadsheetFollowers(self, row, followers, date, month):
        # checks for the next empty row to use
        print("Updating spreadsheet...")
        self.SHEET.updateRow(row, [date, followers, increase, following, posts, month])


insta = InstaTracker()

followers = insta.getFollowers()
increase = insta.getIncrease(followers)
date, month = insta.getDate()
posts = insta.getNumberPosts()
following = insta.getFollowing()

row = insta.getOpenRow()
insta.updateSpreadsheetFollowers(row, followers, date, month)
print("Complete!")
