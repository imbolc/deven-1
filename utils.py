from datetime import datetime


def parse_rundate(s):
    day, month, year = s.split('-')
    month = month.title()
    return datetime.strptime(f'{day}-{month}-{year}', '%d-%b-%y')
