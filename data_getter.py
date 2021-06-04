from __future__ import print_function
import sys
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

SCOPES = ['https://www.googleapis.com/auth/spreadsheets',
          'https://www.googleapis.com/auth/drive',
          'https://www.googleapis.com/auth/drive.file']

SPREADSHEET_ID = 'REPLACE WITH SPREADSHEET ID'
RANGE_NAME = 'A:D'
SHEET_ID = 'REPLACE WITH SHEET ID'

def main():
    completed = {}
    creds = None

    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'REPLACE WITH SECRETS FILE NAME', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID,
                                range=RANGE_NAME).execute()
    values = result.get('values', [])

    if not values:
        return "NO DATA"
    else:
        #print('Phone #, Carrier:')
        for row in values:

            completed[row[2]] = row[3]
        del completed['Phone Number (no spaces)']

        request_body = {
            'requests':[
                {
                'deleteDimension': {
                    'range': {
                        'sheetId': SHEET_ID,
                        'dimension': 'ROWS',
                        'startIndex': 1,
                        'endIndex': 1 + len(completed)
                    }
                }
            }
        ]
    }
        service.spreadsheets().batchUpdate(
            spreadsheetId = SPREADSHEET_ID,
            body=request_body
        ).execute()
        return completed
