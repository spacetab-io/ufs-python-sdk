from datetime import datetime


def get_array(items, item_class):
    if items is not None:
        return [item_class(item) for item in items]
    return None


def get_item(item, item_class):
    if item is not None:
        return item_class(item)
    return None


def get_bool_item(item):
    if item is not None:
        return bool(item)
    return False


def get_datetime(item):
    if item is not None:
        return datetime.strptime(item, '%d.%m.%Y %X')
    return None


def set_datetime(item):
    if item is not None:
        return item.strftime('%d.%m.%Y %X')
    return None


def get_list_from_string(string, item_type):
    if string is not None and type(string) is str:
        if ', ' in string:
            return [item_type(item) for item in string.split(', ')]
        elif ',' in string:
            return [item_type(item) for item in string.split(',')]
        elif '; ' in string:
            return [item_type(item) for item in string.split('; ')]
        elif ';' in string:
            return [item_type(item) for item in string.split(';')]
    return None


def get_ufs_datetime(xml):
    try:
        return {'Date': datetime.strptime(xml.text, '%d.%m.%Y %X'),
                'TimeOffset': xml.attrib.get('timeOffset', None),
                'TimeType': xml.attrib.get('timeType', None)}
    except:
        return {'Date': xml.text,
                'TimeOffset': xml.attrib.get('timeOffset', None),
                'TimeType': xml.attrib.get('timeType', None)}
