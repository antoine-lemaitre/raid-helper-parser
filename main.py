from extractor import raid_extractor, raid_extractor_by_character, find_character, clean_date, find_character_with_attendance_stats, raid_attendance_statistics
import click
import json
import datetime


@click.command()
@click.option('-e','--extractor', is_flag=True, help='Extract data from dump.csv file')
@click.option('-c','--character', is_flag=True, help='Results of attendence by characters')
@click.option('-f','--find', help='Find attendence for a specific character')
@click.option('-s','--stats', help='Find attendence for a specific character and his participation statistics')
@click.option('-r','--raid-stats', is_flag=True, help='Find attendence statistics for raids')
@click.option('-b','--before-date', default=datetime.datetime.now(), help='Find attendence before a specific date with format: day-month-year. Example: -b 11-09-2020')
@click.option('-a','--after-date', default=None, help='Find attendence after a specific date with format: day-month-year. Example: -b 21-06-2020')
def selector(extractor, find, before_date, after_date, character, stats, raid_stats):

    date_range = clean_date(after_date,before_date)

    if extractor:
        click.echo(json.dumps(raid_extractor(date_range), indent=4, sort_keys=True, ensure_ascii=False))

    elif character:
        click.echo('Results by character')
        click.echo(json.dumps(raid_extractor_by_character(date_range), indent=4, sort_keys=True, ensure_ascii=False))
    
    elif find:
        click.echo('Finding player attendance ' + find)
        click.echo(json.dumps(find_character(find, date_range), indent=4, sort_keys=True, ensure_ascii=False))
    
    elif stats:
        click.echo('Finding ' + stats + ' attendance statistics')
        click.echo(stats + " was {0:.0%}".format(find_character_with_attendance_stats(stats, date_range)))

    elif raid_stats:
        click.echo('Finding attendance statistics')
        click.echo(json.dumps(raid_attendance_statistics(date_range), indent=4, sort_keys=True, ensure_ascii=False))

    else:
        click.echo('You need to choose at least one argument. Please see --help')

if __name__ == '__main__':
    selector()
