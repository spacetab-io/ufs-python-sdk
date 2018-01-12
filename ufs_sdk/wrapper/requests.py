from ufs_sdk.utils import get_ufs_datetime

# Называть однотипно переменные для слабаков
REQUEST_PARAM_NAMES = {
    'from_': 'from',
    'advert_domain': 'advertDomain',
    'remote_check_in': 'RemoteCheckIn',
    'id_cust': 'idcust',
    'pay_type': 'PayType',
    'international_service_class': 'internationalServiceClass',
    'use_static_schedule': 'useStaticSchedule',
    'join_train_complex': 'joinTrainComplex',
    'groupping_type': 'GrouppingType',
    'search_option': 'searchOption',
    'id_trans': 'IdTrans',
    'id_blank': 'IdBlank',
    'force_new_tech': 'ForceNewTech',
    'blanks_id': 'BlanksId',
    'food_allowance_code': 'FoodAllowanceCode',
    'all_languages': 'AllLanguages',
    'is_description': 'IsDescription'
}
# Называть переменные разными именами ? Не, не слышал
ARRAYS = ['SC', 'N', 'C', 'CK', 'Blank', 'CO_SERVICES', 'LOYALTY_CARDS', 'Warning', 'EPrintPoint']


class RequestWrapper(object):
    def __init__(self, session):
        self.session = session

    def make_request(self, method_name, get=True, **kwargs):
        if get:
            params = self.get_params(kwargs)
            response = self.session.make_api_request(method_name, params, get)
            if method_name == 'GetTicketBlank':
                return response
            return self.get_json_xml(response, method_name)

    # Пытаться напрямую конвертировать их xml в объект - жопа
    # Для этого использую слой конвертации в json, где исправляются имена и их чудеса с массивами
    def get_json_xml(self, response, method_name):
        json = {}
        for item in response:
            if len(item.getchildren()) != 0:
                tag_data = self.get_json_rec(item, {}, method_name)
            else:
                tag_data = self.get_item(item)

            if item.tag not in json.keys():
                if item.tag in ARRAYS or (method_name == 'AvailableFood' and item.tag in ['Food']):
                    json[item.tag] = [tag_data]
                else:
                    json[item.tag] = tag_data
            else:
                if item.tag in ARRAYS or (method_name == 'AvailableFood' and item.tag in ['Food']):
                    json[item.tag].append(tag_data)
                else:
                    json[item.tag] = tag_data

            if type(json[item.tag]) is dict and item.attrib != {}:
                for key in item.attrib.keys():
                    json[item.tag][key] = item.attrib[key]
            elif type(json[item.tag]) is list and item.attrib != {}:
                if type(json[item.tag][-1]) is not dict:
                    json[item.tag][-1] = {'data': json[item.tag][-1]}
                for key in item.attrib.keys():
                    json[item.tag][-1][key] = item.attrib[key]
            elif item.attrib != {}:
                data = json[item.tag] if json.get(item.tag) is not None else None
                json[item.tag] = {'data': data}
                for key in item.attrib.keys():
                    json[item.tag][key] = item.attrib[key]
        return response, json

    # Уходим в рекурсивное преобразование тегов в json
    def get_json_rec(self, xml, json, method_name):
        for item in xml:
            if len(item.getchildren()) == 0:
                if len(item.getchildren()) != 0:
                    tag_data = self.get_json_rec(item, {}, method_name)
                else:
                    tag_data = self.get_item(item)
                if item.tag not in json.keys():
                    if item.tag in ARRAYS or (method_name == 'AvailableFood' and item.tag in ['Food']):
                        json[item.tag] = [tag_data]
                    else:
                        json[item.tag] = tag_data
                else:
                    if item.tag in ARRAYS or (method_name == 'AvailableFood' and item.tag in ['Food']):
                        json[item.tag].append(tag_data)
                    else:
                        json[item.tag] = tag_data
            else:
                if item.tag not in json.keys():
                    if item.tag in ARRAYS or (method_name == 'AvailableFood' and item.tag in ['Food']):
                        json[item.tag] = [self.get_json_rec(item, {}, method_name)]
                    else:
                        json[item.tag] = self.get_json_rec(item, {}, method_name)
                else:
                    if item.tag in ARRAYS or (method_name == 'AvailableFood' and item.tag in ['Food']):
                        json[item.tag].append(self.get_json_rec(item, {}, method_name))
                    else:
                        json[item.tag] = self.get_json_rec(item, {}, method_name)

            if type(json[item.tag]) is dict and item.attrib != {}:
                for key in item.attrib.keys():
                    json[item.tag][key] = item.attrib[key]
            elif type(json[item.tag]) is list and item.attrib != {}:
                for key in item.attrib.keys():
                    if type(json[item.tag][-1]) is not dict:
                        json[item.tag][-1] = {'data': json[item.tag][-1]}
                    json[item.tag][-1][key] = item.attrib[key]
            elif item.attrib != {}:
                data = json[item.tag] if json.get(item.tag) is not None else None
                json[item.tag] = {'data': data}
                for key in item.attrib.keys():
                    json[item.tag][key] = item.attrib[key]
        return json

    @staticmethod
    def get_item(item):
        if item.text is None:
            return True
        if item.tag in ['ArrivalTime', 'DepartureTime', 'ConfirmTimeLimit', 'ExpireSetEr', 'ChangeFoodBefore',
                        'ChangeFoodBefore', 'ConfirmTimeLimit']:
            return get_ufs_datetime(item)
        if item.tag in ['C']:
            tag_data = item.text
            if '[ ' in tag_data:
                tag_data = tag_data.replace('[ ')
            elif ' ]' in tag_data:
                tag_data = tag_data.replace(' ]')
            if '[' in tag_data:
                tag_data = tag_data.replace('[')
            elif ']' in tag_data:
                tag_data = tag_data.replace(']')
            return tag_data
        return item.text

    # Строим get строку запроса
    def get_params(self, params):
        get_params = ''
        for key in params.keys():
            if params[key] is not None:
                get_params += '&%s=%s' % (self.convert_request_param_name(key),
                                          params[key] if type(params[key]) is str else
                                          (int(params[key]) if type(params[key]) is bool else params[key]))

        return get_params

    # Получаем имя запроса
    # В запросе есть параметр from(служебное слово языка)
    # Пришлось делать преобразование
    @staticmethod
    def convert_request_param_name(param):
        if param in REQUEST_PARAM_NAMES:
            return REQUEST_PARAM_NAMES[param]
        return param
