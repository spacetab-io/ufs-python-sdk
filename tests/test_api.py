import os
import json
import unittest
from ufs_sdk import API
from datetime import datetime
from ufs_sdk.wrapper import PassDoc
from ufs_sdk.exceptions import UfsTrainListError, UfsAPIError
from ufs_sdk.wrapper.types import (TimeSw, DirectionGroup, CarCategories, Services, Confirm, ElectronicRegistration,
                                   Test, PrintFlag, RzhdStatus, Registration, ReferenceCode, InOneKupe, Bedding,
                                   FullKupe, RemoteCheckIn, PayType, Storey, PlaceDemands, TicketFormat)
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
        new_url = None
        if 'TrainRoute' not in url:
            if 'TimeTable' in url:
                if str('МОСКВА') in url:
                    new_url = 'TimeTableClarify'
                else:
                    new_url = 'TimeTable'
            elif 'Train' in url:
                if str('АГАПОВКА') in url:
                    new_url = 'TrainListClarify'
                elif str('КРЫМ') in url:
                    new_url = 'TrainListError'
                else:
                    new_url = 'TrainList'

        if new_url is None:
            new_url = url.replace('https://www.ufs-online.ru/webservices/Railway/Rest/Railway.svc/', '')
            new_url = new_url[:new_url.index('?terminal')]


        self.text = open('tests/data/{}.xml'.format(new_url), 'r', encoding='utf8').read()
        
        if new_url == 'GetTicketBlank':
            self.headers['Content-Type'] = 'text/html'

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
        self.assertEquals(time_table.is_clarify, False)

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
        self.assertEquals(time_table.data.trains[0].arrival_time.date, '03:00:00')
        self.assertEquals(time_table.data.trains[0].arrival_time.time_offset, None)
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

    def test_train_route(self):
        train_route = self.api.train_route(1, 1, 1, 1)

        self.assertEquals(train_route.additional_info.desc, 'РАСПИСАНИЕ ДВИЖЕНИЯ ПОЕЗДА')
        self.assertEquals(train_route.additional_info.train_number, '002А')
        self.assertEquals(train_route.additional_info.departure_date, '10.04')
        self.assertEquals(train_route.additional_info.arrival_date, '03.04')

        self.assertEquals(train_route.route_params.origin, 'МОСКВА ОКТ')
        self.assertEquals(train_route.route_params.destination, 'С-ПЕТЕР-ГЛ')
        self.assertEquals(train_route.route_params.origin_code, 2006004)
        self.assertEquals(train_route.route_params.destination_code, 2004001)

        self.assertEquals(train_route.routes[0].desc, 'ОСНОВНОЙ МАРШРУТ')

        self.assertEquals(train_route.routes[0].route_info.origin, 'МОСКВА ОКТ')
        self.assertEquals(train_route.routes[0].route_info.destination, 'С-ПЕТЕР-ГЛ')

        self.assertEquals(train_route.routes[0].route_stops[0].station_name, 'МОСКВА ОКТ')
        self.assertEquals(train_route.routes[0].route_stops[0].station_code, 2006004)
        self.assertEquals(train_route.routes[0].route_stops[0].arrival_date, None)
        self.assertEquals(train_route.routes[0].route_stops[0].arrival_time, None)
        self.assertEquals(train_route.routes[0].route_stops[0].stop_duration, 0)
        self.assertEquals(train_route.routes[0].route_stops[0].days_count, None)
        self.assertEquals(train_route.routes[0].route_stops[0].distance, 0)
        self.assertEquals(train_route.routes[0].route_stops[0].local_departure_time, '23:55:00')
        self.assertEquals(train_route.routes[0].route_stops[0].local_arrival_time, None)
        self.assertEquals(train_route.routes[0].route_stops[0].station_info.name, 'МОСКВА ОКТЯБРЬСКАЯ')
        self.assertEquals(train_route.routes[0].route_stops[0].station_info.shortname, None)
        self.assertEquals(train_route.routes[0].route_stops[0].station_info.code, 2006004)
        self.assertEquals(train_route.routes[0].route_stops[0].station_info.is_multi_station, False)
        self.assertEquals(train_route.routes[0].route_stops[0].station_info.multi_station_code, 2000000)
        self.assertEquals(train_route.routes[0].route_stops[0].station_info.alias, 'МОСКВА')

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
        except UfsAPIError as ex:
            self.assertEquals(UfsAPIError, type(ex))

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
        self.assertEquals(train_list.data.trains[0].is_logical_train, False)
        self.assertEquals(train_list.data.trains[0].number, '116С')
        self.assertEquals(train_list.data.trains[0].client_number, '116С')
        self.assertEquals(train_list.data.trains[0].category, 'СК')
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
        self.assertEquals(train_list.data.trains[0].cars[0].ticket_price, 393400)
        self.assertEquals(train_list.data.trains[0].cars[0].min_service_price, 27000)
        self.assertEquals(train_list.data.trains[0].cars[0].max_price, 393400)
        self.assertEquals(train_list.data.trains[0].cars[0].service_price, 27000)
        self.assertEquals(train_list.data.trains[0].cars[0].is_two_place, False)
        self.assertEquals(train_list.data.trains[0].cars[0].is_four_place, False)
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
        self.assertEquals(train_list.data.trains[0].cars[0].is_discount, False)
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
        self.assertEquals(train_list.data.trains[0].arrival_time.date, '03:00:00')
        self.assertEquals(train_list.data.trains[0].arrival_time.time_offset, None)
        self.assertEquals(train_list.data.trains[0].arrival_time.time_type, 0)
        self.assertEquals(train_list.data.trains[0].passenger_railway_station.origin_code, 2000006)
        self.assertEquals(train_list.data.trains[0].passenger_railway_station.destination_code, 2000170)
        self.assertEquals(train_list.data.trains[0].passenger_departure_station.code, 2000006)
        self.assertEquals(train_list.data.trains[0].passenger_departure_station.name, 'МОСКВА БЕЛОРУССКАЯ')
        self.assertEquals(train_list.data.trains[0].passenger_arrival_station.code, 2000170)
        self.assertEquals(train_list.data.trains[0].passenger_arrival_station.name, 'СМОЛЕНСК ЦЕНТРАЛЬНЫЙ')

        self.assertEquals(train_list.balance, 3000000)
        self.assertEquals(train_list.balance_limit,0)

    def test_car_list_ex(self):
        car_list_ex = self.api.car_list_ex(1000001, 2000000, 3, 2, '00031#031А', '17:23')

        self.assertEquals(car_list_ex.general_information.reference_code, 62)
        self.assertEquals(car_list_ex.general_information.reference_type, 'М')
        self.assertEquals(car_list_ex.general_information.route_params.origin, 'ХЕЛЬСИНКИ')
        self.assertEquals(car_list_ex.general_information.route_params.destination, 'МОСКВА ОКТ')
        self.assertEquals(car_list_ex.general_information.route_params.origin_code, 1000001)
        self.assertEquals(car_list_ex.general_information.route_params.destination_code, 2006004)
        self.assertEquals(car_list_ex.general_information.route_params.from_code, 1000001)
        self.assertEquals(car_list_ex.general_information.route_params.to_code, 2006004)
        self.assertEquals(car_list_ex.general_information.route_params.allowed_doc_types, ['ЗП', 'ЗЗ'])
        self.assertEquals(car_list_ex.general_information.route_params.direction_group, 1)
        self.assertEquals(car_list_ex.general_information.cipher, True)

        self.assertEquals(car_list_ex.train.number, '00031#031А')
        self.assertEquals(car_list_ex.train.client_number, '00031')
        self.assertEquals(car_list_ex.train.category, True)
        self.assertEquals(car_list_ex.train.train_name, 'Лев Толстой')
        self.assertEquals(car_list_ex.train.route.origin, 'ХЕЛЬСИНКИ')
        self.assertEquals(car_list_ex.train.route.destination, 'МОСКВА')
        self.assertEquals(car_list_ex.train.passenger_departure_time, '03.02')
        self.assertEquals(car_list_ex.train.passenger_arrival_time, '04.02')
        self.assertEquals(car_list_ex.train.passenger_departure_date, '17:23')
        self.assertEquals(car_list_ex.train.origin_parking_time, None)
        self.assertEquals(car_list_ex.train.travel_time, '014:56')
        self.assertEquals(car_list_ex.train.passenger_arrival_date, '09:19')
        self.assertEquals(car_list_ex.train.destination_parking_time, None)
        self.assertEquals(car_list_ex.train.is_electronic_registration, False)
        self.assertEquals(car_list_ex.train.origin_departure_time, True)
        self.assertEquals(car_list_ex.train.route_length, 1073)

        self.assertEquals(car_list_ex.train.cars[0].category, 'ЛЮКС')
        self.assertEquals(car_list_ex.train.cars[0].car_category, None)
        self.assertEquals(car_list_ex.train.cars[0].car_gen_info, '1/2')
        self.assertEquals(car_list_ex.train.cars[0].service_class, None)
        self.assertEquals(car_list_ex.train.cars[0].services, [Services.COND, Services.BED])
        self.assertEquals(car_list_ex.train.cars[0].services_info, None)
        self.assertEquals(car_list_ex.train.cars[0].country_way, None)
        self.assertEquals(car_list_ex.train.cars[0].car_owner, None)
        self.assertEquals(car_list_ex.train.cars[0].car_category_belonging, 'МЖ')
        self.assertEquals(car_list_ex.train.cars[0].ticket_price, 0)
        self.assertEquals(car_list_ex.train.cars[0].min_service_price, None)
        self.assertEquals(car_list_ex.train.cars[0].max_price, None)
        self.assertEquals(car_list_ex.train.cars[0].service_price, None)
        self.assertEquals(car_list_ex.train.cars[0].is_dynamic_price, False)
        self.assertEquals(car_list_ex.train.cars[0].is_two_place, False)
        self.assertEquals(car_list_ex.train.cars[0].is_four_place, False)

        self.assertEquals(car_list_ex.train.cars[0].car_info[0].is_electronic_registration, True)
        self.assertEquals(car_list_ex.train.cars[0].car_info[0].car_num, 11)
        self.assertEquals(car_list_ex.train.cars[0].car_info[0].free_places, None)
        self.assertEquals(car_list_ex.train.cars[0].car_info[0].kupe_down_free_places, 12)
        self.assertEquals(car_list_ex.train.cars[0].car_info[0].kupe_up_free_places, 0)
        self.assertEquals(car_list_ex.train.cars[0].car_info[0].kupe_down_side_free_places, None)
        self.assertEquals(car_list_ex.train.cars[0].car_info[0].kupe_up_side_free_places, None)
        self.assertEquals(car_list_ex.train.cars[0].car_info[0].man_places, None)
        self.assertEquals(car_list_ex.train.cars[0].car_info[0].women_places, None)
        self.assertEquals(car_list_ex.train.cars[0].car_info[0].whole_kupe, 12)
        self.assertEquals(car_list_ex.train.cars[0].car_info[0].mixed_kupe, None)
        self.assertEquals(car_list_ex.train.cars[0].car_info[0].count_whole_kupe, 0)
        self.assertEquals(car_list_ex.train.cars[0].car_info[0].linens, False)
        self.assertEquals(car_list_ex.train.cars[0].car_info[0].free_places_list, ['1Ц', '2Ц', '3Ц', '4Ц', '5Ц', '6Ц', '11Ц', '12Ц', '13Ц', '14Ц', '15Ц', '16Ц'])
        self.assertEquals(car_list_ex.train.cars[0].car_info[0].car_category, 'Л')
        self.assertEquals(car_list_ex.train.cars[0].car_info[0].is_two_storey, False)
        self.assertEquals(car_list_ex.train.cars[0].car_info[0].route_type, None)
        self.assertEquals(car_list_ex.train.cars[0].car_info[0].table_free_places, None)
        self.assertEquals(car_list_ex.train.cars[0].car_info[0].playground_free_places, None)
        self.assertEquals(car_list_ex.train.cars[0].car_info[0].table_playground_free_places, None)
        self.assertEquals(car_list_ex.train.cars[0].car_info[0].animals_free_places, None)
        self.assertEquals(car_list_ex.train.cars[0].car_info[0].default_free_places, None)
        self.assertEquals(car_list_ex.train.cars[0].car_info[0].is_rp_selected, True)
        self.assertEquals(car_list_ex.train.cars[0].car_info[0].arrival, datetime.now().replace(month=8, day=21, hour=7, minute=20, second=0, microsecond=0))
        self.assertEquals(car_list_ex.train.cars[0].car_info[0].place_numbers, None)
        self.assertEquals(car_list_ex.train.cars[0].car_info[0].folding_place_numbers, None)
        self.assertEquals(car_list_ex.train.cars[0].car_info[0].animals_place_numbers, None)
        self.assertEquals(car_list_ex.train.cars[0].car_info[0].mother_place_numbers, None)
        self.assertEquals(car_list_ex.train.cars[0].car_info[0].children_place_numbers, None)
        self.assertEquals(car_list_ex.train.cars[0].car_info[0].is_floating, False)
        self.assertEquals(car_list_ex.train.cars[0].car_info[0].place_type_number, None)
        self.assertEquals(car_list_ex.train.cars[0].car_info[0].subtype, None)
        self.assertEquals(car_list_ex.train.cars[0].car_info[0].up_place, None)
        self.assertEquals(car_list_ex.train.cars[0].car_info[0].down_place, None)
        self.assertEquals(car_list_ex.train.cars[0].car_info[0].down_side_place, None)
        self.assertEquals(car_list_ex.train.cars[0].car_info[0].up_side_place, None)
        self.assertEquals(car_list_ex.train.cars[0].car_info[0].down_near_wc_place, None)
        self.assertEquals(car_list_ex.train.cars[0].car_info[0].up_near_wc_place, None)
        self.assertEquals(car_list_ex.train.cars[0].car_info[0].down_side_near_wc_place, None)
        self.assertEquals(car_list_ex.train.cars[0].car_info[0].up_side_near_wc_place, None)
        self.assertEquals(car_list_ex.train.cars[0].car_info[0].schema, 'TVER_2/4_V1')
        self.assertEquals(car_list_ex.train.cars[0].is_discount, False)
        self.assertEquals(car_list_ex.train.cars[0].is_reservation, False)
        self.assertEquals(car_list_ex.train.cars[0].available_tariffs, [1, 9, 10])
        self.assertEquals(car_list_ex.train.cars[0].is_loyalty_cards, None)
        self.assertEquals(car_list_ex.train.cars[0].is_full_kupe, True)
        self.assertEquals(car_list_ex.train.special_conditions, None)
        self.assertEquals(car_list_ex.train.brand, None)
        self.assertEquals(car_list_ex.train.is_suburban_train, False)
        self.assertEquals(car_list_ex.train.departure_time.date, self.datetime)
        self.assertEquals(car_list_ex.train.departure_time.time_offset, '+02:00')
        self.assertEquals(car_list_ex.train.departure_time.time_type, 1)
        self.assertEquals(car_list_ex.train.arrival_time.date, '03:00:00')
        self.assertEquals(car_list_ex.train.arrival_time.time_offset, None)
        self.assertEquals(car_list_ex.train.arrival_time.time_type, 0)
        self.assertEquals(car_list_ex.train.passenger_railway_station.origin_code, 1000001)
        self.assertEquals(car_list_ex.train.passenger_railway_station.destination_code, 2006004)
        self.assertEquals(car_list_ex.train.passenger_departure_station.code, 1000001)
        self.assertEquals(car_list_ex.train.passenger_departure_station.name, 'ХЕЛЬСИНКИ')
        self.assertEquals(car_list_ex.train.passenger_arrival_station.code, 2006004)
        self.assertEquals(car_list_ex.train.passenger_arrival_station.name, 'МОСКВА ОКТЯБРЬСКАЯ')

    def test_buy_tickets(self):
        pass_doc = PassDoc('ЗП', 'ЗЗ934647165', '01051956', '1', 'KEN', first_name='Вася', last_name='Пупкин')
        buy_tickets = self.api.buy_ticket(2000000, 1000001, 2, 3, '032A', 'М', pass_doc, InOneKupe.NOT_SIDE,
                                          RemoteCheckIn.TRY_AUTO_ER, PayType.CASH)

        self.assertEquals(buy_tickets.creation_date, '010216')
        self.assertEquals(buy_tickets.carrier, 'ОАО "ФПК"')
        self.assertEquals(buy_tickets.carrier_inn, 7708709686)
        self.assertEquals(buy_tickets.reservation_time, '0809')
        self.assertEquals(buy_tickets.train_number, '032А')
        self.assertEquals(buy_tickets.departure_date, '02.03')
        self.assertEquals(buy_tickets.departure_time, '19:53')
        self.assertEquals(buy_tickets.train_category, True)
        self.assertEquals(buy_tickets.train_name, 'ЛЕВ ТОЛСТОЙ')
        self.assertEquals(buy_tickets.train_brand, 'ЛЕВ ТОЛСТОЙ')
        self.assertEquals(buy_tickets.origin, 'МОСКВА')
        self.assertEquals(buy_tickets.destination, 'ХЕЛЬСИНКИ')
        self.assertEquals(buy_tickets.origin_code, 2000000)
        self.assertEquals(buy_tickets.destination_code, 1000001)
        self.assertEquals(buy_tickets.car_number, 15)
        self.assertEquals(buy_tickets.segment_type, 1)
        self.assertEquals(buy_tickets.car_category, 'М')
        self.assertEquals(buy_tickets.service_class, '1А')
        self.assertEquals(buy_tickets.kupe_sex, True)
        self.assertEquals(buy_tickets.carrier_name, 'ФПК')
        self.assertEquals(buy_tickets.places_amount, 2)
        self.assertEquals(buy_tickets.place_number, [1, 2])
        self.assertEquals(buy_tickets.total_price, 3568390)
        self.assertEquals(buy_tickets.special_conditions, 'КУРИТЬ ЗАПРЕЩЕНО')
        self.assertEquals(buy_tickets.departure_time_info, 'ВРЕМЯ ОТПР И ПРИБ МОСКОВСКОЕ')
        self.assertEquals(buy_tickets.high_comfort, 'У0')
        self.assertEquals(buy_tickets.arrival_date, '03.03')
        self.assertEquals(buy_tickets.arrival_time, '10:26')

        self.assertEquals(buy_tickets.tickets_info[0].ticket_number, 1)
        self.assertEquals(buy_tickets.tickets_info[0].ticket_price, 3568390)
        self.assertEquals(buy_tickets.tickets_info[0].tariff_nds, 543823)
        self.assertEquals(buy_tickets.tickets_info[0].service_nds, 0)
        self.assertEquals(buy_tickets.tickets_info[0].ticket_eb_price,0)
        self.assertEquals(buy_tickets.tickets_info[0].ticket_platzkart_price,0)
        self.assertEquals(buy_tickets.tickets_info[0].ads_nds,0)
        self.assertEquals(buy_tickets.tickets_info[0].percent_tariff_nds,0)
        self.assertEquals(buy_tickets.tickets_info[0].percent_service_nds,0)
        self.assertEquals(buy_tickets.tickets_info[0].commission_nds,0)
        self.assertEquals(buy_tickets.tickets_info[0].privilege_info, None)
        self.assertEquals(buy_tickets.tickets_info[0].ticket_category, 'ПОЛНЫЙ')
        self.assertEquals(buy_tickets.tickets_info[0].place_tier, 'Н')
        self.assertEquals(buy_tickets.tickets_info[0].place_tier_description, 'НИЖНЕЕ')
        self.assertEquals(buy_tickets.tickets_info[0].passenger_info.doc, 'ЗЗ934647165')
        self.assertEquals(buy_tickets.tickets_info[0].passenger_info.fio, 'Ivanov=Petr')
        self.assertEquals(buy_tickets.tickets_info[0].passenger_info.identifier, 14656796)
        self.assertEquals(buy_tickets.tickets_info[0].passenger_info.sex, 'M')
        self.assertEquals(buy_tickets.tickets_info[0].passenger_info.citizenship, 'KEN')
        self.assertEquals(buy_tickets.tickets_info[0].passenger_info.birth_date, datetime(year=1956, month=5, day=1))

        self.assertEquals(buy_tickets.tickets_info[0].place_list, '001,002')
        self.assertEquals(buy_tickets.tickets_info[0].storey, None)
        self.assertEquals(buy_tickets.tickets_info[0].blank_id, 5164203)
        self.assertEquals(buy_tickets.tickets_info[0].place_count, 2)
        self.assertEquals(buy_tickets.tickets_info[0].is_rp_selected, True)

        self.assertEquals(buy_tickets.departure_datetime.date, self.datetime)
        self.assertEquals(buy_tickets.departure_datetime.time_offset, '+02:00')
        self.assertEquals(buy_tickets.departure_datetime.time_type, 1)
        self.assertEquals(buy_tickets.arrival_datetime.date, '03:00:00')
        self.assertEquals(buy_tickets.arrival_datetime.time_offset, None)
        self.assertEquals(buy_tickets.arrival_datetime.time_type, 0)
        self.assertEquals(buy_tickets.amount, 3568390)
        self.assertEquals(buy_tickets.id_trans, 48715079)
        self.assertEquals(buy_tickets.status, 0)
        self.assertEquals(buy_tickets.balance, 3000000)
        self.assertEquals(buy_tickets.balance_limit, 0.000)
        self.assertEquals(buy_tickets.print_point, 'В кассах ОАО "РЖД", ОАО "ФПК", на транзакционных терминалах ТТС и ТТР')
        self.assertEquals(buy_tickets.print_point_phone, None)

        self.assertEquals(buy_tickets.test, Test.TEST)
        self.assertEquals(buy_tickets.is_eticket_print_point, True)
        self.assertEquals(buy_tickets.confirm_time_limit.date, self.datetime)
        self.assertEquals(buy_tickets.confirm_time_limit.time_offset, '+03:00')
        self.assertEquals(buy_tickets.confirm_time_limit.time_type, None)
        self.assertEquals(buy_tickets.reservation, True)
        self.assertEquals(buy_tickets.reservation_type, 1)
        self.assertEquals(buy_tickets.client_fee, 176000)
        self.assertEquals(buy_tickets.order_id, 82328)

        self.assertEquals(buy_tickets.warnings[0].code, 1)
        self.assertEquals(buy_tickets.warnings[0].text, 'Уже есть бронирование с данными параметрами')
        self.assertEquals(buy_tickets.warnings[0].external_data.key, 'Order ID')
        self.assertEquals(buy_tickets.warnings[0].external_data.value, 37859369841651)

        self.assertEquals(buy_tickets.print_points[0].station, 'СМОЛЕНСК ЦЕНТРАЛЬНЫЙ')
        self.assertEquals(buy_tickets.print_points[0].run_time, '03:10')
        self.assertEquals(buy_tickets.print_points[0].direction, 'opposite')

    def test_confirm_ticket(self):
        confirm_ticket = self.api.confirm_ticket(48715626, Confirm.CONFIRM, 0)

        self.assertEquals(confirm_ticket.status, 0)
        self.assertEquals(confirm_ticket.transaction_id, 48715626)
        self.assertEquals(confirm_ticket.confirm_time_limit.date, self.datetime)
        self.assertEquals(confirm_ticket.confirm_time_limit.time_type, None)
        self.assertEquals(confirm_ticket.confirm_time_limit.time_offset, '+03:00')
        self.assertEquals(confirm_ticket.electronic_registration, ElectronicRegistration.CONFIRM)
        self.assertEquals(confirm_ticket.order_number, 70864898287763)
        self.assertEquals(confirm_ticket.electronic_registration_expire.date, self.datetime)
        self.assertEquals(confirm_ticket.electronic_registration_expire.time_offset, '+03:00')
        self.assertEquals(confirm_ticket.electronic_registration_expire.time_type, None)
        self.assertEquals(confirm_ticket.blank[0].ticket_identifier, 5164710)
        self.assertEquals(confirm_ticket.blank[0].ticket_number, 70864898287763)
        self.assertEquals(confirm_ticket.is_test, Test.TEST)
        self.assertEquals(confirm_ticket.reservation, None)

    def test_update_order_info(self):
        update_order_info = self.api.update_order_info(48715626)

        self.assertEquals(update_order_info.status, 0)

        self.assertEquals(update_order_info.blank[0].ticket_identifier, 5164702)
        self.assertEquals(update_order_info.blank[0].electronic_registration, ElectronicRegistration.CONFIRM)
        self.assertEquals(update_order_info.blank[0].print_flag, PrintFlag.NOT_PRINTED)
        self.assertEquals(update_order_info.blank[0].rzhd_status, RzhdStatus.ELECTRONIC_REGISTRATION)
        self.assertEquals(update_order_info.blank[0].food.code, 'Б')
        self.assertEquals(update_order_info.blank[0].food.name, 'ЗАВТРАК-БЛИНЫ/СЫР')
        self.assertEquals(update_order_info.blank[0].food.description, 'ЗАКУСКА СЫРНАЯ, БЛИНЫ, СУХАЯ ЧАСТЬ К РАЦИОНУ')

        self.assertEquals(update_order_info.change_food_before.date, self.datetime)
        self.assertEquals(update_order_info.change_food_before.time_offset, '+03:00')

        self.assertEquals(update_order_info.order.id, 82596)
        self.assertEquals(update_order_info.order.root_id, 48715620)
        self.assertEquals(update_order_info.order.order_items[0].id, 48715620)
        self.assertEquals(update_order_info.order.order_items[0].status, 0)

        self.assertEquals(update_order_info.order.order_items[0].blank[0].ticket_identifier, 5164702)
        self.assertEquals(update_order_info.order.order_items[0].blank[0].electronic_registration, ElectronicRegistration.CONFIRM)
        self.assertEquals(update_order_info.order.order_items[0].blank[0].print_flag, PrintFlag.NOT_PRINTED)
        self.assertEquals(update_order_info.order.order_items[0].blank[0].rzhd_status, RzhdStatus.ELECTRONIC_REGISTRATION)
        self.assertEquals(update_order_info.order.order_items[0].blank[0].food.code, 'Б')
        self.assertEquals(update_order_info.order.order_items[0].blank[0].food.name, 'ЗАВТРАК-БЛИНЫ/СЫР')
        self.assertEquals(update_order_info.order.order_items[0].blank[0].food.description, 'ЗАКУСКА СЫРНАЯ, БЛИНЫ, СУХАЯ ЧАСТЬ К РАЦИОНУ')

    def test_electronic_registration(self):
        electronic_registration = self.api.electronic_registration(48715620, Registration.CONFIRM)

        self.assertEquals(electronic_registration.status, 0)

        self.assertEquals(electronic_registration.blanks[0].ticket_identifier, 5164702)
        self.assertEquals(electronic_registration.blanks[0].electronic_registration, ElectronicRegistration.CONFIRM)

    def test_get_ticket_blank(self):
        get_ticket_blank = self.api.get_ticket_blank(1, TicketFormat.HTML)
        html_file = open('tests/data/GetTicketBlank.xml', 'r').read()
        self.assertEquals(get_ticket_blank.content, html_file)

    def test_available_food(self):
        available_food = self.api.available_food(48715620, '')
        self.assertEquals(available_food.change_food_before.time_offset, '+03:00')
        self.assertEquals(available_food.change_food_before.time_type, None)
        self.assertEquals(available_food.change_food_before.date, self.datetime)

        self.assertEquals(available_food.food[0].code, 'Б')
        self.assertEquals(available_food.food[0].name, 'ЗАВТРАК-БЛИНЫ/СЫР')
        self.assertEquals(available_food.food[0].description, 'ЗАКУСКА СЫРНАЯ, БЛИНЫ, СУХАЯ ЧАСТЬК РАЦИОНУ')

    def test_change_food(self):
        change_food = self.api.change_food(48715620, 1, '', '')

        self.assertEquals(change_food.number, '1')
        self.assertEquals(change_food.train_number, '002aa')
        self.assertEquals(change_food.departure_date, '1910')
        self.assertEquals(change_food.departure_number, 2006004)
        self.assertEquals(change_food.arrival_number, 2004001)
        self.assertEquals(change_food.car_number, 2)
        self.assertEquals(change_food.service_class, '1Э')
        self.assertEquals(change_food.place_number, 4)
        self.assertEquals(change_food.passengers_amount, 1)
        self.assertEquals(change_food.electronic_number, 77304832937966)
        self.assertEquals(change_food.food_code, 'Л')
        self.assertEquals(change_food.food_name, 'ЗАВТРАК-БЛИНЫ/МЯСН')
        self.assertEquals(change_food.food_description, 'ЗАКУСКА МЯСНАЯ, БЛИНЫ, СУХАЯ ЧАСТЬ К РАЦИОНУ')

    def test_refund_amount(self):
        refund_amount = self.api.refund_amount(48715620, [1], 0)

        self.assertEquals(refund_amount.status, 0)
        self.assertEquals(refund_amount.fee,0)
        self.assertEquals(refund_amount.tax_percent,0)
        self.assertEquals(refund_amount.amount, 808350)

        self.assertEquals(refund_amount.blanks[0].ticket_identifier, 5279650)
        self.assertEquals(refund_amount.blanks[0].tariff_nds,0)
        self.assertEquals(refund_amount.blanks[0].service_nds,0)
        self.assertEquals(refund_amount.blanks[0].commission_nds, 18.00)
        self.assertEquals(refund_amount.blanks[0].ads_nds, 18.00)
        self.assertEquals(refund_amount.blanks[0].returning_tariff_nds,0)
        self.assertEquals(refund_amount.blanks[0].returning_service_nds,0)
        self.assertEquals(refund_amount.blanks[0].returning_commission_nds,0)
        self.assertEquals(refund_amount.blanks[0].returning_ads_nds, 2828)
        self.assertEquals(refund_amount.blanks[0].returning_full_ticket_amount, None)
        self.assertEquals(refund_amount.blanks[0].returning_kupe_amount, None)
        self.assertEquals(refund_amount.blanks[0].returning_service_amount, None)
        self.assertEquals(refund_amount.blanks[0].fine_amount, None)
        self.assertEquals(refund_amount.blanks[0].amount, 603110)

    def test_refund(self):
        refund = self.api.refund(48715620, [1], 0)

        self.assertEquals(refund.status, 0)
        self.assertEquals(refund.fee,0)
        self.assertEquals(refund.tax_percent,0)
        self.assertEquals(refund.amount, 808350)
        self.assertEquals(refund.refund_id, 48716452)
        self.assertEquals(refund.refund_date, self.datetime)

        self.assertEquals(refund.blanks[0].ticket_identifier, 5279650)
        self.assertEquals(refund.blanks[0].tariff_nds,0)
        self.assertEquals(refund.blanks[0].service_nds,0)
        self.assertEquals(refund.blanks[0].commission_nds, 18.00)
        self.assertEquals(refund.blanks[0].ads_nds, 18.00)
        self.assertEquals(refund.blanks[0].returning_tariff_nds,0)
        self.assertEquals(refund.blanks[0].returning_service_nds,0)
        self.assertEquals(refund.blanks[0].returning_commission_nds,0)
        self.assertEquals(refund.blanks[0].returning_ads_nds, 2828)
        self.assertEquals(refund.blanks[0].returning_full_ticket_amount, None)
        self.assertEquals(refund.blanks[0].returning_kupe_amount, None)
        self.assertEquals(refund.blanks[0].returning_service_amount, None)
        self.assertEquals(refund.blanks[0].fine_amount, None)
        self.assertEquals(refund.blanks[0].amount, 603110)

    def test_get_catalog(self):
        get_catalog = self.api.get_catalog(ReferenceCode.LOYALTY_CARDS, 1)

        self.assertEquals(get_catalog.loyalty_cards[0].code, 'RzhdB')
        self.assertEquals(get_catalog.loyalty_cards[0].name_ru, 'Начисление баллов "РЖД Бонус"')
        self.assertEquals(get_catalog.loyalty_cards[0].name_en, 'RZD Bonus loyalty program')
        self.assertEquals(get_catalog.loyalty_cards[0].name_de, 'RZhD-Bonus')
        self.assertEquals(get_catalog.loyalty_cards[0].description_ru, 'Начисление баллов осуществляется в течение 30 дней с момента начала поездки. Билет будет оформлен на ФИО владельца карты.')
        self.assertEquals(get_catalog.loyalty_cards[0].description_en, 'Reward miles will be credited within 30 days after your departure. The ticket will be issued for the full name of a cardholder.')
        self.assertEquals(get_catalog.loyalty_cards[0].description_de, 'Die Punkte werden im Laufe von 30 Tagen ab dem Fahrt-Anfang angerechnet. Die Fahrkarte wird auf den Namen des Karteninhabers (der Karteninhaberin) ausgestellt.')

