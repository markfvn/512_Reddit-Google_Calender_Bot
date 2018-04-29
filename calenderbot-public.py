################################################################################
#
# Reddit-Google Calender Bot
# Cornell College CSC 512 Project
#
#
#
################################################################################

from __future__ import print_function
from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

import dateutil.parser as dp

import datetime
import praw

reddit = praw.Reddit(client_id='',
                     client_secret='',
                     user_agent='')
###############################
SCOPES = 'https://www.googleapis.com/auth/calendar'
store = file.Storage('credentials.json')
creds = store.get()
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
    creds = tools.run_flow(flow, store)
service = build('calendar', 'v3', http=creds.authorize(Http()))
###############################


subreddit = "RunnerHub"
phrase = "job"
events = []



# perform check if date is acutal date

class event:
    def __init__(self, title, date, url):
        self.title = title
        self.date = date
        self.url = url
        # google calender intigration
        # make event
    def edit(self, date, url):
        self.date = date
        self.url = url
        # google calender intigration
        # ubdate event
    def getTitle(self):
        return self.title
    def getDate(self):
        return self.date
    def getUrl(self):
        return self.url


def checkPosts(subreddit, phrase):
    for sub in reddit.subreddit(subreddit).new(limit=25):
        if phrase.lower() in sub.title.lower():
            try:
                i = sub.selftext.index("\n")
            except ValueError:
                i = -1
            events.append(event(sub.title, sub.selftext[0:i], sub.shortlink))


def dateTimeParcer(dt):
    if(dt.find(" ") == -1):
        print("fail")
    else:
        datetime = dt
        if not datetime.find("{") == -1:
            datetime = datetime[datetime.index("{") + 1:len(datetime)]
        if not datetime.find("}") == -1:
            datetime = datetime[0:datetime.index("}")]
        d = datetime.index(" ")
        date = datetime[0:d]
        date = date.strip(" ")
        datetime2 = datetime[d + 1:len(datetime)]
        d2 = datetime2.index(" ")
        time = datetime2[0:d2]
        time = time.strip(" ")
        time = time + ":00"
        timezone = datetime2[d2:len(datetime2)]
        timezone = timezone.strip(" ")
        timezone = timezone.strip("(")
        timezone = timezone.strip(")")
        return [date, time, timezone]

def postEvents():
    if len(events) > 0:
        for e in events:
            d = e.getDate()
            dt = dateTimeParcer(d)
            dt = dt[0] + "T" + dt[1]
            event = {
              'summary': e.getTitle(),
              'description': e.getUrl(),
              'start': {
                'dateTime': dt,
                'timeZone': 'America/Los_Angeles',
              },
              'end': {
                'dateTime': dt,
                'timeZone': 'America/Los_Angeles',
              }
            }
            event = service.events().insert(calendarId="", body=event).execute()
            print('Event created: %s' % (event.get('htmlLink')))
            #print(event)



checkPosts(subreddit, phrase)
postEvents()

#events = service.events().list(calendarId='c6av9nmghqvg6h5mblu3qa3m5g@group.calendar.google.com', timeMin='2018-04-30T00:00:00Z',
# timeMax='2018-05-30T23:59:59Z').execute()

#event = service.events().get(calendarId='c6av9nmghqvg6h5mblu3qa3m5g@group.calendar.google.com', eventId='eventId').execute()
