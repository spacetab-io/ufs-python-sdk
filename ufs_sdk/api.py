from .utils import get_item
from .session import Session
from .utils import get_array, get_bool_item, get_datetime
from .wrapper.requests import RequestWrapper
from .wrapper.types import TimeSw, Lang, TrainWithSeat, GrouppingType, JoinTrains, SearchOption, Confirm, Registration
from .wrapper import (Clarify, TimeTable, AdditionalInfoStationRoute, RouteParamsStationRoute, TrainList,
                      GeneralInformation, TrainCarListEx, Blank, DateTime, BlankUpdateOrderInfo, Order,
                      BlankElectronicRegistration, Food, BlankRefund)


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

    def electronic_registration(self, id_trans: int, reg: Registration, id_blank: int=None):
        xml, json = self.__request_wrapper.make_request('ElectronicRegistration', id_trans=id_trans, reg=reg,
                                                        id_blank=id_blank)
        return ElectronicRegistration(xml, json)

    def available_food(self, id_trans: int, advert_domain: str, lang: Lang.RU=Lang.RU):
        xml, json = self.__request_wrapper.make_request('AvailableFood', id_trans=id_trans, advert_domain=advert_domain,
                                                        lang=lang)
        return AvailableFood(xml, json)

    def change_food(self, id_trans: int, blanks_id: int, food_allowance_code: str, advert_domain: str,
                    lang: Lang.RU=Lang.RU):
        xml, json = self.__request_wrapper.make_request('ChangeFood', id_trans=id_trans, blanks_id=blanks_id,
                                                        food_allowance_code=food_allowance_code,
                                                        advert_domain=advert_domain, lang=lang)
        return ChangeFood(xml, json['PIT'])

    def refund_amount(self, id_trans: int, id_blank: int, doc: int, lang: Lang.RU=Lang.RU):
        xml, json = self.__request_wrapper.make_request('RefundAmount', id_trans=id_trans, id_blank=id_blank,
                                                        doc=doc, lang=lang)
        return RefundAmount(xml, json)

    def refund(self, id_trans: int, id_blank: int, doc: int, stan: str=None, lang: Lang.RU=Lang.RU):
        xml, json = self.__request_wrapper.make_request('Refund', id_trans=id_trans, id_blank=id_blank,
                                                        doc=doc, stan=stan, lang=lang)
        return Refund(xml, json)

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


class ElectronicRegistration(object):
    def __init__(self, xml, json):
        # Текущий статус операции: «0» – успешная
        self.status = get_item(json.get('Status'), int)
        # Информация о билете заказа
        self.blank = get_array(json.get('Blank'), BlankElectronicRegistration)

        self.xml = xml
        self.json = json


class AvailableFood(object):
    def __init__(self, xml, json):
        self.change_food_before = get_item(json.get('ChangeFoodBefore'), DateTime)
        self.food = get_array(json['FoodAllowances'].get('Food'), Food) if json.get('FoodAllowances') is not None else None

        self.xml = xml
        self.json = json


class ChangeFood(object):
    def __init__(self, xml, json):
        # Порядковый номер документа
        self.number = json.get('PR')
        # Номер поезда
        self.train_number = json.get('N')
        # Дата отправления поезда
        self.departure_date = json.get('D')
        # Код станции отправления
        self.departure_number = get_item(json.get('C1'), int)
        # Код станции прибытия
        self.arrival_number = get_item(json.get('C2'), int)
        # Номер вагона
        self.car_number = get_item(json.get('B'), int)
        # Класс обслуживания
        self.service_class = json.get('KV')
        # Номера мест
        self.place_number = get_item(json.get('M'), int)
        # Количество пассажиров
        self.passengers_amount = get_item(json.get('KOL'), int)
        # Номер электронного билета
        self.electronic_number = get_item(json.get('NEB'), int)
        # Код РП
        self.food_code = json.get('V')
        # Название РП
        self.food_name = json.get('NAME')
        # Описание РП
        self.food_description = json.get('DESC')

        self.xml = xml
        self.json = json


class RefundAmount(object):
    def __init__(self, xml, json):
        # Статус операции: «0» – успешная
        self.status = get_item(json.get('Status'), int)
        # Сумма сервисного сбора за возврат
        self.fee = get_item(json.get('Fee'), float)
        # Величина комиссионного сбора УФС в %, В случае, если комиссия является фиксированной величиной,
        # то передается в данном параметре «0»
        self.tax_percent = get_item(json.get('TaxPercent'), float)
        # Общая сумма к возврату
        self.amount = get_item(json.get('Amount'), float)
        # Информация о билете заказа
        self.blanks = get_array(json.get('Blank'), BlankRefund)

        self.xml = xml
        self.json = json


class Refund(object):
    def __init__(self, xml, json):
        # Статус операции: «0» – успешная
        self.status = get_item(json.get('Status'), int)
        # Номер транзакции возврата
        self.refund_id = get_item(json.get('RefundTransID'), int)
        # Время осуществления возврата
        self.refund_date = get_datetime(json.get('RefundTime'))
        # Сумма сервисного сбора за возврат
        self.fee = get_item(json.get('Fee'), float)
        # Величина комиссионного сбора УФС в %, В случае, если комиссия является фиксированной величиной,
        # то передается в данном параметре «0»
        self.tax_percent = get_item(json.get('TaxPercent'), float)
        # Общая сумма к возврату
        self.amount = get_item(json.get('Amount'), float)
        # Информация о билете заказа
        self.blanks = get_array(json.get('Blank'), BlankRefund)

        self.xml = xml
        self.json = json
