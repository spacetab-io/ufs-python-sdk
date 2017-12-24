from ufs_sdk.utils import get_ufs_datetime

REQUEST_PARAM_NAMES = {'from_': 'from'}
RESPONSE_PARAM_NAMES = {
    # TimeTableClarify
    'UC': 'IsClarify',
    'SC': 'Stations',
    'PD': 'StationRoot',
    'CC': 'StationCode',
    'C': 'StationName',
    # TimeTableNormal
    'Z2': 'ReferenceParams',
    'K': 'ReferenceCode',
    'D': 'ReferenceDate',
    'PP': 'RouteParams',
    'N': 'Trains',
    'C1': 'OriginCode',
    'C2': 'DestinationCode',
    'N1': 'Number',
    'N2': 'ClientNumber',
    'NP': 'Route',
    'T1': 'PassengerDepartureDate',
    'T2': 'OriginParkingTime',
    'T3': 'TravelTime',
    'T4': 'PassengerArrivalTime',
    'T5': 'DestinationParkingTime',
    'J': 'AdditionalInfo',
    'DW': 'TrainDaysActivity',
    'L': 'RouteLength',
    'NN': 'TrainName'
}

# Называть переменные разными именами ? Не, не слышал
ARRAYS = ['Stations', 'Trains', 'StationName']


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
            param_name = self.convert_response_param_name(item.tag)
            if len(item.getchildren()) != 0:
                tag_data = self.get_json_rec(item, {})
            else:
                tag_data = True if item.text is None else (item.text
                                                           if param_name not in ['ArrivalTime', 'DepartureTime']
                                                           else get_ufs_datetime(item))

            if param_name not in json.keys():
                if param_name in ARRAYS:
                    json[param_name] = [tag_data]
                else:
                    json[param_name] = tag_data
            else:
                if param_name in ARRAYS:
                    json[param_name].append(tag_data)
                else:
                    json[param_name] = [json[param_name]]
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
            param_name = self.convert_response_param_name(item.tag)
            if len(item.getchildren()) == 0:
                if len(item.getchildren()) != 0:
                    tag_data = self.get_json_rec(item, {})
                else:
                    tag_data = True if item.text is None else (item.text
                                                               if param_name not in ['ArrivalTime', 'DepartureTime']
                                                               else get_ufs_datetime(item))
                if param_name not in json.keys():
                    if param_name in ARRAYS:
                        json[param_name] = [tag_data]
                    else:
                        json[param_name] = tag_data
                else:
                    if param_name in ARRAYS:
                        json[param_name].append(tag_data)
                    else:
                        json[param_name] = [json[param_name]]
            else:
                json[param_name] = self.get_json_rec(item, {})
        return json

    # Строим get строку запроса
    def get_params(self, params):
        get_params = ''
        for key in params.keys():
            get_params += '&%s=%s' % (self.convert_request_param_name(key),
                                      params[key].encode('cp1251') if type(params[key]) is str else params[key])
        return get_params

    # Получаем имя запроса
    # В запросе есть параметр from(служебное слово языка)
    # Пришлось делать преобразование
    @staticmethod
    def convert_request_param_name(param):
        if param in REQUEST_PARAM_NAMES.keys():
            return REQUEST_PARAM_NAMES[param]
        return param

    # УФСМАТЬВАШУ не умею давать имена
    # Так что меняем весь их бред на адекватные названия
    @staticmethod
    def convert_response_param_name(param):
        if param in RESPONSE_PARAM_NAMES.keys():
            return RESPONSE_PARAM_NAMES[param]
        return param
