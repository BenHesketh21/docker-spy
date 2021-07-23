import datetime
from tabulate import tabulate
from termcolor import colored

def get_age(creation_time):
    now = datetime.datetime.utcnow()
    age = now - creation_time
    age = age - datetime.timedelta(microseconds=age.microseconds)
    if age.days != 0:
        return f"{age.days} Days"
    elif age.seconds > 3600:
        return f"{int(age.seconds/3600)} Hours"
    elif age.seconds > 60:
        return f"{int(age.seconds/60)} Mins"
    else:
        return f"{int(age.seconds)} Secs"

def cls(): 
    print('\033[H\033[J')



def title(title):
    return "\n\n======\n\n" +colored(title + "\n\n", "grey", attrs=["bold", "underline"])

def add_op(op_title, data, headers):
    return title(op_title) + tabulate(data, headers=headers)