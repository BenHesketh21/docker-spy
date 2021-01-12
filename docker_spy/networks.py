from . import client
from .utils import get_age
from dateutil.parser import parse


def get_networks():
    networks = []
    for network in client.networks.list():
        network.reload()
        if network.attrs["IPAM"]["Options"] == {} or "com.docker.compose.network" in network.attrs["Labels"].keys():
            networks.append((network.name, len(network.containers), get_age(parse(network.attrs["Created"]).replace(tzinfo=None))))
    return sorted(networks)