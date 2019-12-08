import random
import time
import requests
import json
import datetime
import pytz

url = "https://freegeoip.app/json/"

headers = {
    'accept': "application/json",
    'content-type': "application/json"
    }

def give_random_ip():
    new_ip = ''
    new_ip = str(random.randint(0, 255)) + '.' + str(random.randint(0, 255)) + '.' + str(random.randint(0, 255)) + '.' + str(random.randint(0, 255))
    return new_ip

def create_a_list():
    new_list = []
    while len(new_list) < 100:
        ip = give_random_ip()
        if ip not in new_list:
            new_list.append(ip)
    return new_list

def use_freegeoip(ip):
    new_url = url + ip
    response = requests.request("GET", new_url, headers=headers)
    new_response = response.text
    return new_response

def get_all_timezones(the_list):
    timezones_list = []
    for i in the_list:
        response = use_freegeoip(i)
        new_dict = json.loads(response)
        new_timezone = new_dict.get('time_zone')
        if (new_timezone not in timezones_list) and (new_timezone != ''):
            timezones_list.append(new_timezone)
        new_time = random.uniform(0.5, 1)
        time.sleep(new_time)
    return timezones_list

def give_random_datetime():
    month = random.randint(1, 12)
    if month == 2:
        day = random.randint(1, 28)
    elif month in [1, 3, 5, 7, 8, 10, 12]:
        day = random.randint(1, 31)
    else:
        day = random. randint(1, 30)
    hour = random.randint(0, 23)
    minute = random.randint(0, 59)
    second = random.randint(0, 59)
    new_datetime = datetime.datetime(2019, month, day, hour, minute, second, tzinfo=None)
    return new_datetime

def datetime_to_unix_timestamp (the_datetime):
    new_unix_timestamp = time.mktime(the_datetime.timetuple())
    return new_unix_timestamp

def another_timezone (the_unix_timestamp, timezone):
    try:
        new_timezone = pytz.timezone(timezone)
        new_datetime = the_datetime.fromtimestamp(the_unix_timestamp, tz=new_timezone)
        return new_datetime
    except pytz.exceptions.UnknownTimeZoneError:
        error_message = 'Unknown time zone'
        return error_message

def get_timezones_output (the_unix_timestamp, timezones_list):
    timezones_output = []
    for timezone in timezones_list:
        new_datetime = another_timezone(the_unix_timestamp, timezone)
        new_output = timezone + '\t' + str(new_datetime) + '\n'
        timezones_output.append(new_output)
    return timezones_output

def final_output (the_datetime, the_unix_timestamp, timezones_list):
    print ('Random date:\t', the_datetime)
    print ('Unix timestamp:\t', the_unix_timestamp)
    print ('Another timezones:')
    for timezone in timezones_list:
        new_datetime = another_timezone(the_unix_timestamp, timezone)
        print('%30s' % timezone, '\t', str(new_datetime))
    
the_list = create_a_list()
timezones_list = get_all_timezones(the_list)
the_datetime = give_random_datetime()
the_unix_timestamp = datetime_to_unix_timestamp (the_datetime)
final_output (the_datetime, the_unix_timestamp, timezones_list)


    

