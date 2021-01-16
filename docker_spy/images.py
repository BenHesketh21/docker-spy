from dateutil.parser import parse

from . import client
from .utils import get_age

def get_image_tag(image_tags):
    if len(image_tags) == 0:
        return "None"
    else:
        return image_tags[0]

def get_images():
    images = []
    for image in client.images.list():
        if image.attrs["RepoTags"] != []:
            created = get_age(parse(image.attrs["Created"]).replace(tzinfo=None))
            name_and_tag = image.tags[0].split(":")
            _id = image.short_id.split(":")[1]
            images.append((_id, name_and_tag[0], name_and_tag[1], created))
    return images