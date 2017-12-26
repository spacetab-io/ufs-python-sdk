from .utils import get_item
from .session import Session
from .wrapper.requests import RequestWrapper
from .wrapper.types import TimeSw, Lang, TrainWithSeat, GrouppingType, JoinTrains, SearchOption
from .wrapper import Clarify, TimeTable, AdditionalInfoStationRoute, RouteParamsStationRoute, TrainList


class API(object):
    def __init__(self, username: str, password: str, terminal: str):
        self.__session = Session(username, password, terminal)
        self.__request_wrapper = RequestWrapper(self.__session)

    def time_table(self, from_: 'str or int', to, day: int, month: int, time_sw: TimeSw=TimeSw.NO_SW, time_from: int=None,
                   time_to: int=None, suburban: bool=None):
        xml, json = self.__request_wrapper.make_request('TimeTable', from_=from_, to=to, day=day, month=month,
                                                        time_sw=time_sw, time_from=time_from, time_to=time_to,
                                                        suburban=suburban)
        return TimeTableBuilder(xml, json['S'])

    def station_route(self, day: int, month: int, from_: 'str or int', use_static_schedule: bool, suburban=None):
        xml, json = self.__request_wrapper.make_request('StationRoute', from_=from_, day=day, month=month,
                                                        use_static_schedule=use_static_schedule,
                                                        suburban=suburban)
        return StationRoute(xml, json['S'])

    def train_list(self, from_: 'str or int', to, day: int, month: int, advert_domain: str=None, lang: str=Lang.RU,
                   time_sw: TimeSw=TimeSw.NO_SW, time_from: int=None, time_to: int=None,
                   train_with_seat: TrainWithSeat=None, join_train_complex: bool=None, groupping_type: GrouppingType=None,
                   join_trains: JoinTrains=None, search_option: SearchOption=None):
        xml, json = self.__request_wrapper.make_request('TrainList', from_=from_, to=to, day=day, month=month,
                                                        advert_domain=advert_domain, time_sw=time_sw, lang=lang,
                                                        time_from=time_from, time_to=time_to, train_with_seat=train_with_seat,
                                                        join_train_complex=join_train_complex, groupping_type=groupping_type,
                                                        join_trains=join_trains, search_option=search_option)
        return TrailListBuilder(xml, json)

    @property
    def last_response(self):
        return self.__session.last_response_data

    @property
    def last_request(self):
        return self.__session.last_request_data


class TimeTableBuilder(object):
    def __init__(self, xml, json):
        # Признак уточнения станции
        self.is_clarify = json.get('UC', None)
        if self.is_clarify is not None:
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
        self.is_clarify = json['S'].get('UC', None)
        if self.is_clarify is not None:
            # Признак начальной или конечной станции следования
            self.train_point = json['S'].get('parameter', None)
            self.data = Clarify(json['S'])
        else:
            self.data = TrainList(json['S'])
            self.balance = get_item(json.get('Balance'), float)
            self.balance_imit = get_item(json.get('BalanceLimit'), float)

        self.xml = xml
        self.json = json

