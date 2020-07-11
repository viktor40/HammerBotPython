import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import json

SCOPE = ["https://spreadsheets.google.com/feeds"]
SECRETS_FILE = "forms-key.json"
SPREADSHEET = "application test answers"
# Based on docs here - http://gspread.readthedocs.org/en/latest/oauth2.html
# Load in the secret JSON key (must be a service account)
json_key = json.load(open(SECRETS_FILE))
# Authenticate using the signed key

credentials = ServiceAccountCredentials.from_json_keyfile_name(SECRETS_FILE, SCOPE)


gc = gspread.authorize(credentials)
print("The following sheets are available")
for sheet in gc.openall():
    print("{} - {}".format(sheet.title, sheet.id))
# Open up the workbook based on the spreadsheet name
workbook = gc.open(SPREADSHEET)
# Get the first sheet
sheet = workbook.sheet1
# Extract all data into a dataframe
data = pd.DataFrame(sheet.get_all_records())
# Do some minor cleanups on the data
# Rename the columns to make it easier to manipulate
# The data comes in through a dictionary so we can not assume order stays the
# same so must name each column
column_names = {'Tijdstempel': 'timestamp',
                'What is your Minecraft IGN?': 'ign',
                'How long have you been playing MC?': 'playing',
                'Why would you like to join our server?': 'application_reason',
                'How old are you?': 'age',
                }
data.rename(columns=column_names, inplace=True)
data.timestamp = pd.to_datetime(data.timestamp)
print(data.head())