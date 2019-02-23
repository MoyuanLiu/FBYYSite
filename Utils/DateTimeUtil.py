import time
from datetime import timedelta, date
from time import strftime

def is_valid_date(strdate,pattern):
    try:
        time.strptime(strdate, pattern)
        return True
    except:
        return False

def get_day_of_today(n=0):
    '''''
       if n>=0,date is larger than today
       if n<0,date is less than today
       date format = "YYYY-MM-DD"
       '''
    if (n < 0):
        n = abs(n)
        dayval = date.today() - timedelta(days=n)
    else:
        dayval = date.today() + timedelta(days=n)
    return dayval
