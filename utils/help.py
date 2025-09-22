from dateutil import rrule
from datetime import datetime
from logs.logging import get_logger
from math import floor,log10

logger = get_logger("help") 


def round_significance(value, sig):
    
    if value:
        r_value = round(value, sig - int(floor(log10(abs(value)))) - 1)
    else:
        r_value = value
    
    return r_value

def to_str_date(date: datetime.date, fmt: str = '%Y-%m-%d') -> str:
    return date.strftime(fmt)

def timestamp():
    now = datetime.now()
    timestamp = datetime.timestamp(now)
    return timestamp

def days_in_range(date_from_str,date_to_str):
    date1 = datetime.strptime(date_from_str, "%Y-%m-%d").date()
    date1_0 = datetime(date1.year, date1.month, date1.day)
    date2 = datetime.strptime(date_to_str, "%Y-%m-%d").date()
    date_list = list(rrule.rrule(rrule.DAILY, dtstart=date1_0, until=date2))
    return date_list

def str_timestamp():
    today = datetime.now()
    year = str(today.year)
    month = str(today.month).zfill(2)
    day = str(today.day).zfill(2)
    hour = str(today.hour).zfill(2)
    minute = str(today.minute).zfill(2)
    second = str(today.second).zfill(2)

    date_str_list = [year,month,day,hour,minute]
    timestamp = ''.join(date_str_list)

    timestamp = year+month+day+hour+minute+second
    return timestamp

def valida_dias_uteis_mes(dias_uteis_min=4):
    today = datetime.today()
    mes_0 = today.replace(day=1)

    days = (today-mes_0).days+1

    dias_uteis=0
    for i in range(days):
        date = mes_0.replace(day=i+1)
        weekday = date.weekday()
        dias_uteis = dias_uteis + 1 if weekday not in [6,5] else dias_uteis

    if dias_uteis>=dias_uteis_min:
        return True
    else:
        return False

def create_directory(directory_name):
    import os

    # define the name of the directory to be created
    path = os.getcwd()+"/"+directory_name

    try:
        os.mkdir(path)
        return directory_name
    except OSError:
        print ("Não foi possível criar o diretório")
        raise Exception('Não foi possível criar o diretório')

def multiply_time(time_str,multiply_factor):
    if (not time_str) or (not multiply_factor):
        return "00:00:00"
    lines = [time_str]*int(multiply_factor)
    total = 0
    for line in lines:
        h, m, s = map(int, line.split(":"))
        total += 3600*h + 60*m + s
    return("%02d:%02d:%02d" % (total / 3600, total / 60 % 60, total % 60))