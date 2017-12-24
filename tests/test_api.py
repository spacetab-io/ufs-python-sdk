import os
import unittest
from ufs_sdk import API
from datetime import datetime
from ufs_sdk.wrapper.types import TIME_SW, DIRECTION_GROUP
from ufs_sdk.wrapper.requests import RESPONSE_PARAM_NAMES
from ufs_sdk.wrapper import ReferenceParamsTimeTable, AdditionalInfoTimeTable, TrainsTimeTable
import mock


class MockSession(object):
    def __init__(self):
        self.headers = {}
        self.auth = None
        self.text = None

    def get(self, url, timeout=None):
        """Заглушка для метода Time Table
                    В первом случае возвращаем данные с уточнением станций
                    Во втором - инфу по конкретной станции
                """
        if 'TimeTable' in url:
            if str('МОСКВА'.encode('cp1251')) in url:
                url = 'TimeTableClarify'
            else:
                url = 'TimeTable'
        else:
            url = url.replace('https://www.ufs-online.ru/webservices/Railway/Rest/Railway.svc/', '')
            url = url[:url.index('?terminal')]

        self.text = open('tests/data/{}.xml'.format(url), 'r', encoding='utf8').read()
        return self


class TestAPI(unittest.TestCase):

    @mock.patch('requests.Session', MockSession)
    def setUp(self):
        self.maxDiff = None
        self.datetime = datetime.fromtimestamp(0).replace(hour=3)

        self.username = os.environ.get('USERNAME', None)
        self.password = os.environ.get('PASSWORD', None)
        self.terminal = os.environ.get('TERMINAL', None)

        self.api = API(self.username, self.password, self.terminal)

    def test_time_table_clarify(self):
        time_table = self.api.time_table('МОСКВА', 'САНКТ-ПЕТЕРБУРГ', 24, 12, TIME_SW.NO_SW)
        self.assertEquals(time_table.is_clarify, True)
        self.assertEquals(time_table.train_point, 'to')
        self.assertEquals(time_table.data.stations[0].station_root, 'КРАС')
        self.assertEquals(time_table.data.stations[0].station_code, '2038563')
        self.assertEquals(time_table.data.stations[0].station_name, 'ТОННЕЛЬНАЯ')

    def test_time_table(self):
        time_table = self.api.time_table(10000001, 10000002, 24, 12, TIME_SW.NO_SW)
        self.assertEquals(time_table.is_clarify, None)

        self.assertEquals(time_table.data.reference_params.reference_code, 11)
        self.assertEquals(time_table.data.reference_params.reference_date, '02.02')

        self.assertEquals(time_table.data.route_params.origin, 'МОСКВА')
        self.assertEquals(time_table.data.route_params.destination, 'С-ПЕТЕРБУР')
        self.assertEquals(time_table.data.route_params.origin_code, 2000000)
        self.assertEquals(time_table.data.route_params.destination_code, 2004000)
        self.assertEquals(time_table.data.route_params.from_code, 2000000)
        self.assertEquals(time_table.data.route_params.to_code, 2004000)
        self.assertEquals(time_table.data.route_params.allowed_doc_types, 'ПН,СР,ЗП,ЗЗ,ПМ,ВБ')
        self.assertEquals(time_table.data.route_params.direction_group, DIRECTION_GROUP.INTERNAL)

        self.assertEquals(time_table.data.trains[0].number, '756А')
        self.assertEquals(time_table.data.trains[0].client_number, '756А')
        self.assertEquals(time_table.data.trains[0].route.origin, 'МОСКВА ОКТ')
        self.assertEquals(time_table.data.trains[0].route.destination, 'С-ПЕТЕР-ГЛ')
        self.assertEquals(time_table.data.trains[0].route.origin_code, 2006004)
        self.assertEquals(time_table.data.trains[0].route.destination_code, 2004001)
        self.assertEquals(time_table.data.trains[0].passenger_departure_date, '07:40')
        self.assertEquals(time_table.data.trains[0].origin_parking_time, '07:40')
        self.assertEquals(time_table.data.trains[0].travel_time, '07:40')
        self.assertEquals(time_table.data.trains[0].passenger_arrival_time, '07:40')
        self.assertEquals(time_table.data.trains[0].destination_parking_time, '07:40')
        self.assertEquals(time_table.data.trains[0].depth_train_sales.date, '01.07.2017')
        self.assertEquals(time_table.data.trains[0].depth_train_sales.days, 59)
        self.assertEquals(time_table.data.trains[0].additional_info.train_days_activity, 'ЕЖ')
        self.assertEquals(time_table.data.trains[0].route_length, 650)
        self.assertEquals(time_table.data.trains[0].train_name, 'Сапсан')
        self.assertEquals(time_table.data.trains[0].departure_time.date, self.datetime)
        self.assertEquals(time_table.data.trains[0].departure_time.time_offset, '+03:00')
        self.assertEquals(time_table.data.trains[0].departure_time.time_type, 0)
        self.assertEquals(time_table.data.trains[0].arrival_time.date, self.datetime)
        self.assertEquals(time_table.data.trains[0].arrival_time.time_offset, '+03:00')
        self.assertEquals(time_table.data.trains[0].arrival_time.time_type, 0)

    def test_station_route(self):
        station_route = self.api.station_route(4043, 5, 8, True, True)

        self.assertEquals(station_route.additional_info.reference_content, 'СРАНЫЙУФС')
        self.assertEquals(station_route.additional_info.station_name, 'МОСКВА-ПАССАЖИРСКАЯ-ПАВЕЛЕЦКАЯ')
        self.assertEquals(station_route.additional_info.passenger_departure_time, '05.08')
        self.assertEquals(station_route.additional_info.documents_formation_time, '04.08')

        self.assertEquals(station_route.route_params.trains[0].number, '967363')
        self.assertEquals(station_route.route_params.trains[0].client_number, '7271')
        self.assertEquals(station_route.route_params.trains[0].route.origin, 'МОСКВА-ПАССАЖИРСКАЯ-ПАВЕЛЕЦКАЯ')
        self.assertEquals(station_route.route_params.trains[0].route.destination, 'АЭРОПОРТ-ДОМОДЕДОВО')
        self.assertEquals(station_route.route_params.trains[0].route.origin_code, 4043)
        self.assertEquals(station_route.route_params.trains[0].route.destination_code, 4036)
        self.assertEquals(station_route.route_params.trains[0].passenger_departure_date, '00:01:00')
        self.assertEquals(station_route.route_params.trains[0].travel_time, '00:01:00')
        self.assertEquals(station_route.route_params.trains[0].passenger_arrival_time, '00:01:00')
        self.assertEquals(station_route.route_params.trains[0].train_days_activity, 'ежедн.')