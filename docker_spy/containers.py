from termcolor import colored
from dateutil.parser import parse

from . import client
from .utils import get_age
from .images import get_image_tag




def get_container_names(list_of_containers):
    containers = ""
    for container in list_of_containers:
        if len(list_of_containers) == list_of_containers[-1]:
            containers += container.name
        else:
            containers += container.name + ", "
    return containers



def get_container_status(status):
    green = ["created", "running"]
    yellow = ["restarting", "paused"]
    if status in green:
        return colored(status, "green")
    if status in yellow:
        return colored(status, "yellow")
    else:
        return colored(status, "red")

def get_containers(all=False):
    containers = []
    while True:
        try: 
            list_of_containers = client.containers.list(all=all)
            break
        except Exception: 
            continue
    for container in list_of_containers:
        created = get_age(parse(container.attrs['Created']).replace(tzinfo=None))
        image = colored(get_image_tag(container.image.tags), "cyan")
        status = get_container_status(container.status)
        containers.append((container.name, image, status, created))
    return containers
