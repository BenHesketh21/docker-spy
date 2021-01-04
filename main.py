import docker
import time
import os
from tabulate import tabulate
from termcolor import colored
import sys

client = docker.from_env()

def get_image_tag(image_tags):
    if len(image_tags) == 0:
        return "None"
    else:
        return image_tags[0]

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
    for container in client.containers.list(all=all):
        containers.append((container.name, colored(get_image_tag(container.image.tags), "cyan"), get_container_status(container.status)))
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
            name_and_tag = image.tags[0].split(":")
            images.append((name_and_tag[0], name_and_tag[1]))
    return images

def cls(): 
    print('\033[H\033[J')

def get_networks():
    networks = []
    for network in client.networks.list():
        network.reload()
        if network.attrs["IPAM"]["Options"] == {} or "com.docker.compose.network" in network.attrs["Labels"].keys():
            networks.append((network.name, get_container_names(network.containers)))
    return sorted(networks)

def title(title):
    return "\n\n======\n\n" +colored(title + "\n\n", "grey", attrs=["bold", "underline"])



last_screen = ""
while True:
    screen = ""
    args = sys.argv
    if "images" in args:
        screen += title("Images") + tabulate(get_images(), headers=["Name", "Tags"])
    if "containers" in args:
        screen += title("Containers") + tabulate(get_containers(all=True), headers=["Name", "Image", "Status"])
    if "networks" in args:
        screen += title("Networks") + tabulate(get_networks(), headers=["Name", "Attached Containers"])
    if screen != last_screen:
        cls()
        print(screen)
        last_screen = screen
    time.sleep(0.5)
