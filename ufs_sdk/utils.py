from datetime import datetime


def get_array(items, item_class):
    if items is not None:
        return [item_class(item) for item in items]
    return None


def get_item(item, item_class):
    if item is not None:
        return item_class(item)
    return None


def get_datetime(item):
    if item is not None:
        return datetime.strptime(item, '%Y-%m-%dT%X')
    return None


def get_datetime_array(items):
    if items is not None:
        return [datetime.strptime(item, '%Y-%m-%dT%X') for item in items]
    return None


def set_datetime(item):
    if item is not None:
        return item.strftime('%Y-%m-%dT%X')
    return None


def get_ufs_datetime(xml):
    return {'Date': datetime.strptime(xml.text, '%d.%m.%Y %X'),
            'TimeOffset': xml.attrib.get('timeOffset', None),
            'TimeType': xml.attrib.get('timeType', None)}
