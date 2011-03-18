#!/usr/bin/env python
# encoding: utf8

# Copyright 2011 Gleb Kanterov. gleb@kanterov.ru

import urllib2
import leaf
import re
import datetime
import gdata.calendar.data
import gdata.calendar.client
import gdata.acl.data
import atom.data

# Edit here \/ \/ \/ \/
GOOGLE_ACCOUNT = "THIS IS"
PASSWORD = "SECRET"

DAYS = [["Web", "QA", "Enterprise"], ["PM + HR", "Mobile"]]
CODEFEST_DATE = datetime.datetime(2011, 3, 19, 0, 0, 0, 0)
ONE_DAY = datetime.timedelta(days=1)

def get_client():
    client = gdata.calendar.client.CalendarClient(source='yourCo-yourAppName-v1')
    client.ClientLogin(GOOGLE_ACCOUNT, PASSWORD, client.source)

    return client

calendar_client = get_client()

def get_calendar():
    calendar = gdata.calendar.data.CalendarEntry()
    calendar.title = atom.data.Title(text='Codefest')
    calendar.summary = atom.data.Summary(text='Расписание докладок на codefest')
    calendar.where.append(gdata.calendar.data.CalendarWhere(value='Novosibirsk'))
    calendar.color = gdata.calendar.data.ColorProperty(value='#2952A3')
    calendar.timezone = gdata.calendar.data.TimeZoneProperty(value='Asia/Novosibirsk')
    calendar.hidden = gdata.calendar.data.HiddenProperty(value='false')

    new_calendar = calendar_client.InsertCalendar(new_calendar=calendar)

    return new_calendar

def add_event(start, end, name, topic, topic_about, day, where):
    event = gdata.calendar.data.CalendarEventEntry()

    if name is not None:
        event.title = atom.data.Title(text=name)
        event.content = atom.data.Content()
        event.where.append(gdata.calendar.data.CalendarWhere(value=where))
    else:
        event.title = atom.data.Title(text=topic)
        event.content = atom.data.Content(text=topic_about)
        event.where.append(gdata.calendar.data.CalendarWhere(value=where))

    start_time = CODEFEST_DATE + day * ONE_DAY + datetime.timedelta(hours=start[0], minutes=start[1])
    end_time = CODEFEST_DATE + day * ONE_DAY + datetime.timedelta(hours=end[0], minutes=end[1])

    event.when.append(gdata.calendar.data.When(start=start_time.isoformat(), end=end_time.isoformat()))

    new_event = calendar_client.InsertEvent(event)

def get_schedule():
    html = urllib2.urlopen("http://codefest.ru/program/2011-03/").read()
    doc = leaf.parse(html)

    programs = doc("table.program tbody")

    section = 0
    day = 0

    for program in programs:
        talks = program("tr")
        
        for talk in talks:
            time_tag = talk("td")[0]
            about_tag = talk("td")[-1]
            topic_tag = talk.get("td a")

            start = (None, None)
            end = (None, None)
            topic = None
            topic_about = None
            speaker = None
            name = None

            if time_tag is not None:
                time = time_tag.text
                r = re.search(u".*(\d\d):(\d\d).*(\d\d):(\d\d).*", time) 
                if r is not None:
                    start = (int(r.group(1)), int(r.group(2)))
                    end = (int(r.group(3)), int(r.group(4)))


            if topic_tag is not None:
                topic = topic_tag.text
                topic_about = topic_tag.href

            if about_tag is not None:
                name = about_tag.text

            print time_tag.text, topic, topic_about, DAYS[day][section]
            add_event(start, end, name, topic, topic_about, day, DAYS[day][section])

        section += 1 

        if len(DAYS[day]) == section:
            day += 1
            section = 0
