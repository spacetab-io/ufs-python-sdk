from ufs_sdk.utils import get_ufs_datetime

REQUEST_PARAM_NAMES = {'from_': 'from'}
# Называть переменные разными именами ? Не, не слышал
ARRAYS = ['SC', 'N', 'C']


class RequestWrapper(object):
    def __init__(self, session):
        self.session = session

    def make_request(self, method_name, get=True, **kwargs):
        if get:
            params = self.get_params(kwargs)
            response = self.session.make_api_request(method_name, params, get)
            return self.get_json_xml(response)

    # Пытаться напрямую конвертировать их xml в объект - жопа
    # Для этого использую слой конвертации в json, где исправляются имена и их чудеса с массивами
    def get_json_xml(self, response):
        json = {}
        s = self.get_child_by_name(response, 'S').attrib
        if s != {}:
            json['TrainPoint'] = s['parameter']
        for item in response.find('./S'):
            if len(item.getchildren()) != 0:
                tag_data = self.get_json_rec(item, {})
            else:
                tag_data = True if item.text is None else (item.text
                                                           if item.tag not in ['ArrivalTime', 'DepartureTime']
                                                           else get_ufs_datetime(item))

            if item.tag not in json.keys():
                if item.tag in ARRAYS:
                    json[item.tag] = [tag_data]
                else:
                    json[item.tag] = tag_data
            else:
                if item.tag in ARRAYS:
                    json[item.tag].append(tag_data)
                else:
                    json[item.tag] = tag_data
        print(json)
        return response.find('./S'), json

    # Получаю тег по имени
    @staticmethod
    def get_child_by_name(xml, child_name):
        for item in xml:
            if item.tag == child_name:
                return item

    # Уходим в рекурсивное преобразование тегов в json
    def get_json_rec(self, xml, json):
        for item in xml:
            if len(item.getchildren()) == 0:
                if len(item.getchildren()) != 0:
                    tag_data = self.get_json_rec(item, {})
                else:
                    tag_data = True if item.text is None else (item.text
                                                               if item.tag not in ['ArrivalTime', 'DepartureTime']
                                                               else get_ufs_datetime(item))
                if item.tag not in json.keys():
                    if item.tag in ARRAYS:
                        json[item.tag] = [tag_data]
                    else:
                        json[item.tag] = tag_data
                else:
                    if item.tag in ARRAYS:
                        json[item.tag].append(tag_data)
                    else:
                        json[item.tag] = tag_data
            else:
                if item.tag not in json.keys():
                    if item.tag in ARRAYS:
                        json[item.tag] = [self.get_json_rec(item, {})]
                    else:
                        json[item.tag] = self.get_json_rec(item, {})
                else:
                    if item.tag in ARRAYS:
                        json[item.tag].append(self.get_json_rec(item, {}))
                    else:
                        json[item.tag] = self.get_json_rec(item, {})
        return json

    # Строим get строку запроса
    def get_params(self, params):
        get_params = ''
        for key in params.keys():
            get_params += '&%s=%s' % (self.convert_request_param_name(key),
                                      params[key].encode('cp1251') if type(params[key]) is str else
                                      (int(params[key]) if type(params[key]) is bool else params[key]))
        return get_params

    # Получаем имя запроса
    # В запросе есть параметр from(служебное слово языка)
    # Пришлось делать преобразование
    @staticmethod
    def convert_request_param_name(param):
        if param in REQUEST_PARAM_NAMES.keys():
            return REQUEST_PARAM_NAMES[param]
        return param
