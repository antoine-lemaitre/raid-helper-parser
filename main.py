from extractor import raid_extractor, raid_extractor_by_character, find_character, clean_date
import click
import json
import datetime


@click.command()
@click.option('-e','--extractor', is_flag=True, help='Extract data from dump.csv file')
@click.option('-f','--find', help='Find attendence for a specific character')
@click.option('-b','--before-date', default=datetime.datetime.now(), help='Find attendence before a specific date with format: day-month-year. Example: -b 11-09-2020')
@click.option('-a','--after-date', default=None, help='Find attendence after a specific date with format: day-month-year. Example: -b 21-06-2020')
@click.option('-c','--character', is_flag=True, help='Results of attendence by characters')
def selector(extractor, find, before_date, after_date, character):

    date_range = clean_date(after_date,before_date)

    if extractor:
        click.echo(json.dumps(raid_extractor(date_range), indent=4, sort_keys=True, ensure_ascii=False))

    elif character:
        click.echo('Results by character')
        click.echo(json.dumps(raid_extractor_by_character(date_range), indent=4, sort_keys=True, ensure_ascii=False))
    
    elif find:
        click.echo('Find ' + find)
        click.echo(json.dumps(find_character(find, date_range), indent=4, sort_keys=True, ensure_ascii=False))

    else:
        click.echo('You need to choose at least one argument. Please see --help')

if __name__ == '__main__':
    selector()
