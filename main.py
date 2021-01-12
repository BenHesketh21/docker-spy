import docker
import time
import os
from tabulate import tabulate
from termcolor import colored
import sys
import datetime
from dateutil.parser import parse

client = docker.from_env()

def get_image_tag(image_tags):
    if len(image_tags) == 0:
        return "None"
    else:
        return image_tags[0]

def get_age(creation_time):
    now = datetime.datetime.utcnow()
    age = now - creation_time
    age = age - datetime.timedelta(microseconds=age.microseconds)
    return age

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
        except: 
            continue
    for container in list_of_containers:
        created = get_age(parse(container.attrs['Created']).replace(tzinfo=None))
        image = colored(get_image_tag(container.image.tags), "cyan")
        status = get_container_status(container.status)
        containers.append((container.name, image, status, created))
    return containers

def get_container_names(list_of_containers):
    containers = ""
    for container in list_of_containers:
        if len(list_of_containers) == list_of_containers[-1]:
            containers += container.name
        else:
            containers += container.name + ", "
    return containers

def get_images():
    images = []
    for image in client.images.list():
        if image.attrs["RepoTags"] != []:
            created = get_age(parse(image.attrs["Created"]).replace(tzinfo=None))
            name_and_tag = image.tags[0].split(":")
            images.append((name_and_tag[0], name_and_tag[1], created))
    return images

def cls(): 
    print('\033[H\033[J')

def get_networks():
    networks = []
    for network in client.networks.list():
        network.reload()
        if network.attrs["IPAM"]["Options"] == {} or "com.docker.compose.network" in network.attrs["Labels"].keys():
            networks.append((network.name, len(network.containers), get_age(parse(network.attrs["Created"]).replace(tzinfo=None))))
    return sorted(networks)

def title(title):
    return "\n\n======\n\n" +colored(title + "\n\n", "grey", attrs=["bold", "underline"])



last_screen = ""
while True:
    screen = ""
    args = sys.argv
    if "images" in args:
        screen += title("Images") + tabulate(get_images(), headers=["Name", "Tags", "Age"])
    if "containers" in args:
        screen += title("Containers") + tabulate(get_containers(all=True), headers=["Name", "Image", "Status", "Age"])
    if "networks" in args:
        screen += title("Networks") + tabulate(get_networks(), headers=["Name", "Attached Containers", "Age"])
    if screen != last_screen:
        cls()
        print(screen)
        last_screen = screen
    time.sleep(0.5)