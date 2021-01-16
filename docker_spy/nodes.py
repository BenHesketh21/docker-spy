from . import client


def get_nodes():
    nodes = []
    #while True:
    #    try:
    list_of_nodes = client.nodes.list()
    #        break
    #    except Exception:
    #        continue
    for node in list_of_nodes:
        _id = node.short_id
        name = node.attrs["Description"]["Hostname"]
        role = node.attrs["Spec"]["Role"]
        nodes.append((_id, name, role))
    return nodes
