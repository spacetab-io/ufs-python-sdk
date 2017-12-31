from .utils import get_item
from .session import Session
from .utils import get_array, get_bool_item, get_ufs_datetime
from .wrapper.requests import RequestWrapper
from .wrapper.types import TimeSw, Lang, TrainWithSeat, GrouppingType, JoinTrains, SearchOption, Confirm
from .wrapper import (Clarify, TimeTable, AdditionalInfoStationRoute, RouteParamsStationRoute, TrainList,
                      GeneralInformation, TrainCarListEx, Blank, DateTime, BlankUpdateOrderInfo, Order)


class API(object):
    def __init__(self, username: str, password: str, terminal: str):
        self.__session = Session(username, password, terminal)
        self.__request_wrapper = RequestWrapper(self.__session)

    def time_table(self, from_: 'str or int', to: 'str or int', day: int, month: int, time_sw: TimeSw=TimeSw.NO_SW,
                   time_from: int=None, time_to: int=None, suburban: bool=None):
        xml, json = self.__request_wrapper.make_request('TimeTable', from_=from_, to=to, day=day, month=month,
                                                        time_sw=time_sw, time_from=time_from, time_to=time_to,
                                                        suburban=suburban)
        return TimeTableBuilder(xml, json['S'])

    def station_route(self, day: int, month: int, from_: 'str or int', use_static_schedule: bool, suburban=None):
        xml, json = self.__request_wrapper.make_request('StationRoute', from_=from_, day=day, month=month,
                                                        use_static_schedule=use_static_schedule,
                                                        suburban=suburban)
        return StationRoute(xml, json['S'])

    def train_list(self, from_: 'str or int', to: 'str or int', day: int, month: int, advert_domain: str=None,
                   lang: str=Lang.RU, time_sw: TimeSw=TimeSw.NO_SW, time_from: int=None, time_to: int=None,
                   train_with_seat: TrainWithSeat=None, join_train_complex: bool=None, groupping_type: GrouppingType=None,
                   join_trains: JoinTrains=None, search_option: SearchOption=None):
        xml, json = self.__request_wrapper.make_request('TrainList', from_=from_, to=to, day=day, month=month,
                                                        advert_domain=advert_domain, time_sw=time_sw, lang=lang,
                                                        time_from=time_from, time_to=time_to, train_with_seat=train_with_seat,
                                                        join_train_complex=join_train_complex, groupping_type=groupping_type,
                                                        join_trains=join_trains, search_option=search_option)
        return TrailListBuilder(xml, json)

    def car_list_ex(self, from_: 'str or int', to: 'str or int', day: int, month: int, train: 'str or int',
                    time: str=None, lang: Lang=Lang.RU, type_car=None, advert_domain: str=None,
                    groupping_type: GrouppingType=None):
        xml, json = self.__request_wrapper.make_request('CarListEx', from_=from_, to=to, day=day, month=month,
                                                        train=train, time=time, lang=lang, type_car=type_car,
                                                        advert_domain=advert_domain, groupping_type=groupping_type)
        return CarListEx(xml, json['S'])


    def confirm_ticket(self, id_trans: int, confirm: Confirm, site_fee: int=None, lang: Lang=Lang.RU):
        xml, json = self.__request_wrapper.make_request('ConfirmTicket', id_trans=id_trans, confirm=confirm,
                                                        site_fee=site_fee, lang=lang)
        return ConfirmTicket(xml, json)

    def update_order_info(self, id_trans: int):
        xml, json = self.__request_wrapper.make_request('UpdateOrderInfo', id_trans=id_trans)
        return UpdateOrderInfo(xml, json)

    @property
    def last_response(self):
        return self.__session.last_response_data

    @property
    def last_request(self):
        return self.__session.last_request_data


class TimeTableBuilder(object):
    def __init__(self, xml, json):
        # Признак уточнения станции
        self.is_clarify = get_bool_item(json.get('UC', None))
        if self.is_clarify:
            # Признак начальной или конечной станции следования
            self.train_point = json.get('parameter', None)
            self.data = Clarify(json)
        else:
            self.data = TimeTable(json)

        self.xml = xml
        self.json = json


class StationRoute(object):
    def __init__(self, xml, json):
        # УФС слишком крутые, им не надо описание данного поля. Нам, видимо, тоже...
        self.additional_info = get_item(json.get('Z1'), AdditionalInfoStationRoute)
        self.route_params = get_item(json.get('PP'), RouteParamsStationRoute)

        self.xml = xml
        self.json = json


class TrailListBuilder(object):
    def __init__(self, xml, json):
        # Признак уточнения станции
        self.is_clarify = get_bool_item(json['S'].get('UC', None))
        if self.is_clarify:
            # Признак начальной или конечной станции следования
            self.train_point = json['S'].get('parameter', None)
            self.data = Clarify(json['S'])
        else:
            self.data = TrainList(json['S'])
            self.balance = get_item(json.get('Balance'), float)
            self.balance_limit = get_item(json.get('BalanceLimit'), float)

        self.xml = xml
        self.json = json


class CarListEx(object):
    def __init__(self, xml, json):
        # Общая информация по запросу
        self.general_information = get_item(json.get('Z3'), GeneralInformation)
        # Информация о поезде
        self.trains = get_array(json.get('N'), TrainCarListEx)

        self.xml = xml
        self.json = json


class ConfirmTicket(object):
    def __init__(self, xml, json):
        self.status = get_item(json.get('Status'), int)
        self.transaction_id = get_item(json.get('TransID'), int)
        self.confirm_time_limit = get_item(json.get('ConfirmTimeLimit'), DateTime)
        self.electronic_registration = get_item(json.get('RemoteCheckIn'), int)
        self.order_number = get_item(json.get('OrderNum'), int)
        self.electronic_registration_expire = get_item(json.get('ExpireSetEr'), DateTime)
        self.blank = get_array(json.get('Blank'), Blank)
        self.is_test = get_item(json.get('IsTest'), int)
        self.reservation = json.get('Reservation')

        self.xml = xml
        self.json = json


class UpdateOrderInfo(object):
    def __init__(self, xml, json):
        # Текущий статус операции: «0» - успешная операция «1»- неуспешная операция
        self.status = get_item(json.get('Status'), int)
        # Информация о билете заказа
        self.blank = get_array(json.get('Blank'), BlankUpdateOrderInfo)
        # Дата и время, до которого можно воспользоваться услугой смены РП.
        # Атрибут «timeOffset="+ЧЧ:ММ"» содержит информацию о часовом поясе для данного элемента, где "+ЧЧ:ММ"
        # разница в часах и минутах от UTC(Всемирное координированное время) конкретного места.
        # Доступно для заказов с возможностью выбора РП
        self.change_food_before = get_item(json.get('ChangeFoodBefore'), DateTime)
        # Информация о заказе
        self.order = get_item(json.get('Order'), Order)

        self.xml = xml
        self.json = json
