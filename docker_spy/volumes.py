from . import client
from .utils import get_age


def get_volumes(all=False):
    volumes = []
    while True:
        try: 
            list_of_volumes = client.volumes.list()
            break
        except Exception: 
            continue
    for volume in list_of_volumes:
        if volume.attrs["Labels"] == {}:
            _id = volume.short_id
            name = volume.name
            age = volume.attrs["Mountpoint"]
            volumes.append((_id, name, age))
    return sorted(volumes)