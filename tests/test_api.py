import os
import unittest
from ufs_sdk import API
from datetime import datetime
from ufs_sdk.exceptions import UfsTrainListError
from ufs_sdk.wrapper import ReferenceParamsTimeTable, AdditionalInfoTimeTable, TrainTimeTable
from ufs_sdk.wrapper.types import TimeSw, DirectionGroup, CarCategories, Services
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
        elif 'Train' in url:
            if str('АГАПОВКА'.encode('cp1251')) in url:
                url = 'TrainListClarify'
            elif str('КРЫМ'.encode('cp1251')) in url:
                url = 'TrainListError'
            else:
                url = 'TrainList'
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
        time_table = self.api.time_table('МОСКВА', 'САНКТ-ПЕТЕРБУРГ', 24, 12, TimeSw.NO_SW)
        self.assertEquals(time_table.is_clarify, True)
        self.assertEquals(time_table.train_point, 'to')
        self.assertEquals(time_table.data.stations[0].station_root, 'КРАС')
        self.assertEquals(time_table.data.stations[0].station_code, '2038563')
        self.assertEquals(time_table.data.stations[0].station_name, 'ТОННЕЛЬНАЯ')

    def test_time_table(self):
        time_table = self.api.time_table(10000001, 10000002, 24, 12, TimeSw.NO_SW)
        self.assertEquals(time_table.is_clarify, None)

        self.assertEquals(time_table.data.reference_params.reference_code, 11)
        self.assertEquals(time_table.data.reference_params.reference_date, '02.02')

        self.assertEquals(time_table.data.route_params.origin, 'МОСКВА')
        self.assertEquals(time_table.data.route_params.destination, 'С-ПЕТЕРБУР')
        self.assertEquals(time_table.data.route_params.origin_code, 2000000)
        self.assertEquals(time_table.data.route_params.destination_code, 2004000)
        self.assertEquals(time_table.data.route_params.from_code, 2000000)
        self.assertEquals(time_table.data.route_params.to_code, 2004000)
        self.assertEquals(time_table.data.route_params.allowed_doc_types, ['ПН', 'СР', 'ЗП', 'ЗЗ', 'ПМ', 'ВБ'])
        self.assertEquals(time_table.data.route_params.direction_group, DirectionGroup.INTERNAL)

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

    def test_train_list_clarify(self):
        train_list = self.api.train_list('МОСКВА', 'АГАПОВКА', 24, 12)
        self.assertEquals(train_list.is_clarify, True)
        self.assertEquals(train_list.train_point, 'to')
        self.assertEquals(train_list.data.stations[0].station_root, 'КРАС')
        self.assertEquals(train_list.data.stations[0].station_code, '2038563')
        self.assertEquals(train_list.data.stations[0].station_name, 'ТОННЕЛЬНАЯ')

    def test_train_list_error(self):
        try:
            self.api.train_list('МОСКВА', 'КРЫМ', 24, 12)
        except UfsTrainListError as ex:
            self.assertEquals(UfsTrainListError, type(ex))

    def test_train_list(self):
        train_list = self.api.train_list('МОСКВА', 'ПИТЕР', 24, 12)

        self.assertEquals(train_list.data.general_information.reference_code, 62)
        self.assertEquals(train_list.data.general_information.reference_type, 'Ц')
        self.assertEquals(train_list.data.general_information.route_params.origin, 'МОСКВА')
        self.assertEquals(train_list.data.general_information.route_params.destination, 'С-ПЕТЕРБУР')
        self.assertEquals(train_list.data.general_information.route_params.origin_code, 2000000)
        self.assertEquals(train_list.data.general_information.route_params.destination_code, 2004000)
        self.assertEquals(train_list.data.general_information.route_params.from_code, 2000000)
        self.assertEquals(train_list.data.general_information.route_params.to_code, 2004000)
        self.assertEquals(train_list.data.general_information.route_params.allowed_doc_types, ['ПН', 'СР', 'ЗП', 'ЗЗ', 'ПМ', 'ВБ'])
        self.assertEquals(train_list.data.general_information.route_params.direction_group, DirectionGroup.INTERNAL)
        self.assertEquals(train_list.data.general_information.cipher, 'О')
        self.assertEquals(train_list.data.trains[0].number_part, 116)
        self.assertEquals(train_list.data.trains[0].is_logical_train, None)
        self.assertEquals(train_list.data.trains[0].number, '116С')
        self.assertEquals(train_list.data.trains[0].client_number, '116С')
        self.assertEquals(train_list.data.trains[0].category, ['С', 'К'])
        self.assertEquals(train_list.data.trains[0].train_name, None)
        self.assertEquals(train_list.data.trains[0].route.origin, 'АДЛЕР')
        self.assertEquals(train_list.data.trains[0].route.destination, 'С-ПЕТ-ЛАД')
        self.assertEquals(train_list.data.trains[0].route.origin_code, None)
        self.assertEquals(train_list.data.trains[0].route.destination_code, None)
        self.assertEquals(train_list.data.trains[0].passenger_departure_time, '02.02')
        self.assertEquals(train_list.data.trains[0].passenger_arrival_time, '02.02')
        self.assertEquals(train_list.data.trains[0].passenger_departure_date, '00:12')
        self.assertEquals(train_list.data.trains[0].origin_parking_time, '00:36')
        self.assertEquals(train_list.data.trains[0].travel_time, '09:46')
        self.assertEquals(train_list.data.trains[0].passenger_arrival_date, '09:58')
        self.assertEquals(train_list.data.trains[0].destination_parking_time, None)
        self.assertEquals(train_list.data.trains[0].is_electronic_registration, True)
        self.assertEquals(train_list.data.trains[0].origin_departure_time, '31.01')
        self.assertEquals(train_list.data.trains[0].route_length, 654)
        self.assertEquals(train_list.data.trains[0].cars[0].category, 'ЛЮКС')
        self.assertEquals(train_list.data.trains[0].cars[0].car_category, 'СВ')
        self.assertEquals(train_list.data.trains[0].cars[0].service_class, '1Л')
        self.assertEquals(train_list.data.trains[0].cars[0].services, [Services.COND, Services.BED])
        self.assertEquals(train_list.data.trains[0].cars[0].country_way, 'РЖД/С-КВ')
        self.assertEquals(train_list.data.trains[0].cars[0].car_owner, 'ФПК')
        self.assertEquals(train_list.data.trains[0].cars[0].car_category_belonging, 'МЖ')
        self.assertEquals(train_list.data.trains[0].cars[0].ticket_price, 3934.0)
        self.assertEquals(train_list.data.trains[0].cars[0].min_ticket_price, 270.0)
        self.assertEquals(train_list.data.trains[0].cars[0].max_service_price, 3934.0)
        self.assertEquals(train_list.data.trains[0].cars[0].service_price, 270.0)
        self.assertEquals(train_list.data.trains[0].cars[0].is_two_place, None)
        self.assertEquals(train_list.data.trains[0].cars[0].is_four_place, None)
        self.assertEquals(train_list.data.trains[0].cars[0].car_info.free_places, None)
        self.assertEquals(train_list.data.trains[0].cars[0].car_info.kupe_down_free_places, 15)
        self.assertEquals(train_list.data.trains[0].cars[0].car_info.kupe_up_free_places, None)
        self.assertEquals(train_list.data.trains[0].cars[0].car_info.kupe_down_side_free_places, None)
        self.assertEquals(train_list.data.trains[0].cars[0].car_info.kupe_up_side_free_places, None)
        self.assertEquals(train_list.data.trains[0].cars[0].car_info.man_places, None)
        self.assertEquals(train_list.data.trains[0].cars[0].car_info.women_places, 3)
        self.assertEquals(train_list.data.trains[0].cars[0].car_info.whole_kupe, None)
        self.assertEquals(train_list.data.trains[0].cars[0].car_info.mixed_kupe, 12)
        self.assertEquals(train_list.data.trains[0].cars[0].car_info.car_category, 'Л')
        self.assertEquals(train_list.data.trains[0].cars[0].car_info.count_whole_kupe, 6)
        self.assertEquals(train_list.data.trains[0].cars[0].is_dynamic_price, True)
        self.assertEquals(train_list.data.trains[0].cars[0].is_discount, None)
        self.assertEquals(train_list.data.trains[0].cars[0].reservation, None)
        self.assertEquals(train_list.data.trains[0].cars[0].client_fee.min, 350)
        self.assertEquals(train_list.data.trains[0].cars[0].client_fee.max, 350)

        self.assertEquals(train_list.data.trains[0].special_conditions.comment, 'КУРИТЬ ЗАПРЕЩЕНО.ПРЕДВАРИТЕЛЬНЫЙ ДОСМОТР')
        self.assertEquals(train_list.data.trains[0].brand, 'САПСАН')
        self.assertEquals(train_list.data.trains[0].cross_border, True)
        self.assertEquals(train_list.data.trains[0].is_suburban_train, True)
        self.assertEquals(train_list.data.trains[0].departure_time.date, self.datetime)
        self.assertEquals(train_list.data.trains[0].departure_time.time_offset, '+03:00')
        self.assertEquals(train_list.data.trains[0].departure_time.time_type, 0)
        self.assertEquals(train_list.data.trains[0].arrival_time.date, self.datetime)
        self.assertEquals(train_list.data.trains[0].arrival_time.time_offset, '+03:00')
        self.assertEquals(train_list.data.trains[0].arrival_time.time_type, 0)
        self.assertEquals(train_list.data.trains[0].passenger_railway_station.origin_code, 2000006)
        self.assertEquals(train_list.data.trains[0].passenger_railway_station.destination_code, 2000170)
        self.assertEquals(train_list.data.trains[0].passenger_departure_station.code, 2000006)
        self.assertEquals(train_list.data.trains[0].passenger_departure_station.name, 'МОСКВА БЕЛОРУССКАЯ')
        self.assertEquals(train_list.data.trains[0].passenger_arrival_station.code, 2000170)
        self.assertEquals(train_list.data.trains[0].passenger_arrival_station.name, 'СМОЛЕНСК ЦЕНТРАЛЬНЫЙ')




        self.assertEquals(train_list.balance, 30000.00)
        self.assertEquals(train_list.balance_imit, 0.00)


