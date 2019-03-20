from datetime import datetime


def get_money(item):
    if item not in ['', 'Unknown', 'NoValue', None]:
        return int(float(item) * 100)
    return None

def get_array(items, item_class):
    if items is not None:
        return [item_class(item) for item in items]
    return None


def get_item(item, item_class):
    if type(item) is not bool and item is not None:
        return item_class(item) if item_class is not int else int(float(item))
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

def get_compare_datetime(date, time=None):
    if date is not None:
        if len(date) == 5:
            date = datetime.strptime(date, '%d.%m').replace(year=datetime.now().year)
        elif len(date) == 6:
            date = datetime.strptime(date, '%d%m%y')
        else:
            date = datetime.strptime(date, '%d%m%Y')
        if time is not None:
            if len(time) == 4:
                date = date.replace(hour=int(time[:2]), minute=int(time[2:]))
            else:
                date = date.replace(hour=int(time.split(':')[0]), minute=int(time.split(':')[1]))
    return date
    
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
        else:
            return [item_type(item) for item in string.split(', ')]
    return None


def get_ufs_datetime(xml):
    try:

        if len(xml.text) == 10:
            return {'Date': datetime.strptime(xml.text, '%d.%m.%Y'),
                'TimeOffset': xml.attrib.get('timeOffset', None),
                'TimeType': xml.attrib.get('timeType', None)}

        return {'Date': datetime.strptime(xml.text, '%d.%m.%Y %X'),
                'TimeOffset': xml.attrib.get('timeOffset', None),
                'TimeType': xml.attrib.get('timeType', None)}
    except:
        return {'Date': xml.text,
                'TimeOffset': xml.attrib.get('timeOffset', None),
                'TimeType': xml.attrib.get('timeType', None)}
