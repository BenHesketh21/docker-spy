import time
import sys
from tabulate import tabulate


from docker_spy.containers import get_containers
from docker_spy.images import get_images
from docker_spy.networks import get_networks
from docker_spy.utils import title, cls

last_screen = ""
empty = False
try:
    while True:
        screen = ""
        args = sys.argv
        if len(args) == 1 and not empty:
            move_on = input("Are you sure you don't want to see any resources? N/Y: ")
            if move_on == "N" or move_on == "n":
                resources = input("Which resources would you like to see? (Seperated by spaces)")
                all_res = ["containers", "networks", "images"]
                for resource in all_res:
                    if resource in resources:
                        args.append(resource)
            if move_on == "Y" or move_on == "y":
                empty = True
                print("Okay... Have fun")

            
        all_ops = []
        if "images" in args:
            all_ops.append
            screen += title("Images") + tabulate(get_images(), headers=["Name", "Tags", "Age"])
        if "containers" in args:
            screen += title("Containers") + tabulate(get_containers(all=True), headers=["Name", "Image", "Status", "Age"])
        if "networks" in args:
            screen += title("Networks") + tabulate(get_networks(), headers=["Name", "Attached Containers", "Age"])
        if screen != last_screen:
            cls()
            print(screen)
            last_screen = screen
        time.sleep(0.7)
except KeyboardInterrupt:
    print("\nThank you for using Docker Spy, see you soon!")