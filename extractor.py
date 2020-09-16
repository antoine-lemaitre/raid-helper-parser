from raid import Raid
import csv
import datetime
import click
import sys
import json


def clean_name(str):
    name = str[2:]
    name = name[:-2]

    return name

def clean_date(after_date, before_date):
    # check sarting range
    if after_date:
        try:
            day = int(after_date[:2])
            month = int(after_date[3:5])
            year = int(after_date[6:10])
            after_date = datetime.datetime(year, month, day)
        except ValueError:
            click.echo("Oops! That was not valid date. Use --help for more informations.")
            sys.exit()
    else:
        after_date = datetime.datetime(1970, 1, 1)

    # check ending range
    if not isinstance(before_date, datetime.datetime):
        try:
            day = int(before_date[:2])
            month = int(before_date[3:5])
            year = int(before_date[6:10])
            before_date = datetime.datetime(year, month, day)
        except ValueError:
            click.echo("Oops! That was not valid date. Use --help for more informations.")

    if before_date < after_date:
        click.echo("Oops! Date range is not accurate. Use --help for more informations.")
        sys.exit()

    date_cleaned = [after_date, before_date]

    return date_cleaned

def raid_extractor(date_range):
    file = open('dump.csv')
    fileReader = csv.reader(file)
    data = list(fileReader)


    raids = []
    guild_raid_attendance = []

    for row in range(len(data)):
        for x in data[row]:
            if x == "-- start --":

                event_date = data[row+2][1]
                try:
                    date_raid = datetime.datetime(int(event_date[6:10]),int(event_date[3:5]),int(event_date[:2]))
                except ValueError:
                    pass


                # Check if raid in date range
                if date_raid >= date_range[0] and date_raid <= date_range[1]:
                    event_name = data[row+2][0]
                    event_time = data[row+2][2]
                    event_description = data[row+2][3]
                    event_created_by = data[row+2][4]
                    event_link = data[row+2][5]

                    # Create a new raid
                    raid_obj = Raid(event_name, event_date, event_time, event_description, event_created_by, event_link)
                    raids.append(raid_obj)

                    # Iterate through all roles
                    i = 3

                    while i < 14:
                        for num_tank in range(len(data[row+i])):
                            if num_tank == 0:
                                role = str(data[row+i][num_tank])
                                continue

                            temp_str = str(data[row+i][num_tank]).split("--")

                            if len(temp_str) > 1:
                                try:
                                    raid_obj.add_attendee(role, clean_name(temp_str[2]))
                                except IndexError:
                                    print("IndexError : " + str(temp_str))

                        i += 1
                
                    guild_raid_attendance.append(raid_obj.export_attendence_to_json())

    return guild_raid_attendance


def raid_extractor_by_character(date_range):
    extracted = {}

    for raid in raid_extractor(date_range):
        for attendee in raid['attendees']:
            extracted.setdefault(attendee, []).append(raid['date'])

    return extracted


def find_character(find, date_range):
    extracted = raid_extractor_by_character(date_range)

    attendence = {}

    for attendee in extracted.keys():
        if find.lower() in attendee.lower():
            for presence in extracted[attendee]:
                attendence.setdefault(attendee, []).append(presence)
    
    return attendence

def find_character_with_attendance_stats(player_stats, date_range):
    raid_attendance = 0
    raid_number = len(raid_extractor(date_range))
    character = find_character(player_stats, date_range)

    for pseudo in character.keys():
        raid_attendance += len(character[pseudo])

    stats = raid_attendance / raid_number
    return stats


def raid_attendance_statistics(date_range):
    extracted = raid_extractor_by_character(date_range)
    raid_number = len(raid_extractor(date_range))

    attendence = {}

    for attendee in extracted.keys():
        attendee_presence = len(extracted[attendee])
        attendence.setdefault(attendee, []).append("{0:.0%}".format(attendee_presence / raid_number))

    return attendence