import datetime
from tabulate import tabulate
from termcolor import colored

def get_age(creation_time):
    now = datetime.datetime.utcnow()
    age = now - creation_time
    age = age - datetime.timedelta(microseconds=age.microseconds)
    if age.days != 0:
        return f"{age.days} Days"
    return age

def cls(): 
    print('\033[H\033[J')



def title(title):
    return "\n\n======\n\n" +colored(title + "\n\n", "grey", attrs=["bold", "underline"])

def add_op(op_title, data, headers):
    return title(op_title) + tabulate(data, headers=headers)