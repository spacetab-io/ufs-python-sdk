from .utils import get_item
from .session import Session
from .wrapper.types import TIME_SW
from .wrapper.requests import RequestWrapper
from .wrapper import Clarify, TimeTable, AdditionalInfoStationRoute, RouteParamsStationRoute


class API(object):
    def __init__(self, username: str, password: str, terminal: str):
        self.__session = Session(username, password, terminal)
        self.__request_wrapper = RequestWrapper(self.__session)

    def time_table(self, from_: 'str or int', to, day: int, month: int, time_sw: TIME_SW=TIME_SW.NO_SW, time_from: int=None,
                   time_to: int=None, suburban: bool=False):
        xml, json = self.__request_wrapper.make_request('TimeTable', from_=from_, to=to, day=day, month=month,
                                                        time_sw=time_sw, time_from=time_from, time_to=time_to,
                                                        suburban=suburban)
        return TimeTableBuilder(xml, json)

    def station_route(self, day: int, month: int, from_: 'str or int', use_static_schedule: bool, suburban=False):
        xml, json = self.__request_wrapper.make_request('StationRoute', from_=from_, day=day, month=month,
                                                        use_static_schedule=use_static_schedule,
                                                        suburban=suburban)
        return StationRoute(xml, json)

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
            self.train_point = json.get('TrainPoint', None)
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
