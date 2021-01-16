from dateutil.parser import parse

from . import client
from .utils import get_age

def get_services():
    services = []
    while True:
        try:
            list_of_services = client.services.list()
            break
        except Exception:
            continue
    for service in list_of_services:
        _id = service.short_id
        name = service.name
        age = get_age(parse(service.attrs["CreatedAt"]).replace(tzinfo=None))
        image = service.attrs["Spec"]["TaskTemplate"]["ContainerSpec"]["Image"].split("@")[0]
        replicas = service.attrs["Spec"]["Mode"]["Replicated"]["Replicas"]
        services.append((_id, name, image, replicas, age))
    return services