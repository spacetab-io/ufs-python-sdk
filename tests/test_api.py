import os
import unittest
from ufs_sdk import API
from datetime import datetime
from ufs_sdk.exceptions import UfsTrainListError
from ufs_sdk.wrapper import ReferenceParamsTimeTable, AdditionalInfoTimeTable, TrainTimeTable
from ufs_sdk.wrapper.types import (TimeSw, DirectionGroup, CarCategories, Services, Confirm, ElectronicRegistration,
                                   Test, PrintFlag, RzhdStatus, Registration)
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
            if str('МОСКВА') in url:
                url = 'TimeTableClarify'
            else:
                url = 'TimeTable'
        elif 'Train' in url:
            if str('АГАПОВКА') in url:
                url = 'TrainListClarify'
            elif str('КРЫМ') in url:
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
        self.assertEquals(train_list.data.trains[0].is_logical_train, False)
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

        self.assertEquals(train_list.balance, 30000.00)
        self.assertEquals(train_list.balance_limit, 0.00)

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

        self.assertEquals(car_list_ex.trains[0].number, '00031#031А')
        self.assertEquals(car_list_ex.trains[0].client_number, '00031')
        self.assertEquals(car_list_ex.trains[0].category, True)
        self.assertEquals(car_list_ex.trains[0].train_name, 'Лев Толстой')
        self.assertEquals(car_list_ex.trains[0].route.origin, 'ХЕЛЬСИНКИ')
        self.assertEquals(car_list_ex.trains[0].route.destination, 'МОСКВА')
        self.assertEquals(car_list_ex.trains[0].passenger_departure_time, '03.02')
        self.assertEquals(car_list_ex.trains[0].passenger_arrival_time, '04.02')
        self.assertEquals(car_list_ex.trains[0].passenger_departure_date, '17:23')
        self.assertEquals(car_list_ex.trains[0].origin_parking_time, None)
        self.assertEquals(car_list_ex.trains[0].travel_time, '014:56')
        self.assertEquals(car_list_ex.trains[0].passenger_arrival_date, '09:19')
        self.assertEquals(car_list_ex.trains[0].destination_parking_time, None)
        self.assertEquals(car_list_ex.trains[0].is_electronic_registration, False)
        self.assertEquals(car_list_ex.trains[0].origin_departure_time, True)
        self.assertEquals(car_list_ex.trains[0].route_length, 1073)

        self.assertEquals(car_list_ex.trains[0].cars[0].category, 'ЛЮКС')
        self.assertEquals(car_list_ex.trains[0].cars[0].car_category, None)
        self.assertEquals(car_list_ex.trains[0].cars[0].car_gen_info, '1/2')
        self.assertEquals(car_list_ex.trains[0].cars[0].service_class, None)
        self.assertEquals(car_list_ex.trains[0].cars[0].services, [Services.COND, Services.BED])
        self.assertEquals(car_list_ex.trains[0].cars[0].services_info, None)
        self.assertEquals(car_list_ex.trains[0].cars[0].country_way, None)
        self.assertEquals(car_list_ex.trains[0].cars[0].car_owner, None)
        self.assertEquals(car_list_ex.trains[0].cars[0].car_category_belonging, 'МЖ')
        self.assertEquals(car_list_ex.trains[0].cars[0].ticket_price, 0)
        self.assertEquals(car_list_ex.trains[0].cars[0].min_ticket_price, None)
        self.assertEquals(car_list_ex.trains[0].cars[0].max_service_price, None)
        self.assertEquals(car_list_ex.trains[0].cars[0].service_price, None)
        self.assertEquals(car_list_ex.trains[0].cars[0].is_dynamic_price, False)
        self.assertEquals(car_list_ex.trains[0].cars[0].is_two_place, False)
        self.assertEquals(car_list_ex.trains[0].cars[0].is_four_place, False)

        self.assertEquals(car_list_ex.trains[0].cars[0].car_info.is_electronic_registration, True)
        self.assertEquals(car_list_ex.trains[0].cars[0].car_info.car_num, 11)
        self.assertEquals(car_list_ex.trains[0].cars[0].car_info.free_places, None)
        self.assertEquals(car_list_ex.trains[0].cars[0].car_info.kupe_down_free_places, 12)
        self.assertEquals(car_list_ex.trains[0].cars[0].car_info.kupe_up_free_places, 0)
        self.assertEquals(car_list_ex.trains[0].cars[0].car_info.kupe_down_side_free_places, None)
        self.assertEquals(car_list_ex.trains[0].cars[0].car_info.kupe_up_side_free_places, None)
        self.assertEquals(car_list_ex.trains[0].cars[0].car_info.man_places, None)
        self.assertEquals(car_list_ex.trains[0].cars[0].car_info.women_places, None)
        self.assertEquals(car_list_ex.trains[0].cars[0].car_info.whole_kupe, 12)
        self.assertEquals(car_list_ex.trains[0].cars[0].car_info.mixed_kupe, None)
        self.assertEquals(car_list_ex.trains[0].cars[0].car_info.count_whole_kupe, 0)
        self.assertEquals(car_list_ex.trains[0].cars[0].car_info.linens, None)
        self.assertEquals(car_list_ex.trains[0].cars[0].car_info.free_places_list, ['1Ц', '2Ц', '3Ц', '4Ц', '5Ц', '6Ц', '11Ц', '12Ц', '13Ц', '14Ц', '15Ц', '16Ц'])
        self.assertEquals(car_list_ex.trains[0].cars[0].car_info.car_category, 'Л')
        self.assertEquals(car_list_ex.trains[0].cars[0].car_info.is_two_storey, False)
        self.assertEquals(car_list_ex.trains[0].cars[0].car_info.route_type, None)
        self.assertEquals(car_list_ex.trains[0].cars[0].car_info.table_free_places, None)
        self.assertEquals(car_list_ex.trains[0].cars[0].car_info.playground_free_places, None)
        self.assertEquals(car_list_ex.trains[0].cars[0].car_info.table_playground_free_places, None)
        self.assertEquals(car_list_ex.trains[0].cars[0].car_info.animals_free_places, None)
        self.assertEquals(car_list_ex.trains[0].cars[0].car_info.default_free_places, None)
        self.assertEquals(car_list_ex.trains[0].cars[0].car_info.is_rp_selected, True)
        self.assertEquals(car_list_ex.trains[0].cars[0].car_info.car_arrival_time, None)
        self.assertEquals(car_list_ex.trains[0].cars[0].car_info.car_passenger_arrival_time, None)
        self.assertEquals(car_list_ex.trains[0].cars[0].car_info.place_numbers, None)
        self.assertEquals(car_list_ex.trains[0].cars[0].car_info.folding_place_numbers, None)
        self.assertEquals(car_list_ex.trains[0].cars[0].car_info.animals_place_numbers, None)
        self.assertEquals(car_list_ex.trains[0].cars[0].car_info.mother_place_numbers, None)
        self.assertEquals(car_list_ex.trains[0].cars[0].car_info.children_place_numbers, None)
        self.assertEquals(car_list_ex.trains[0].cars[0].car_info.is_floating, False)
        self.assertEquals(car_list_ex.trains[0].cars[0].car_info.place_type_number, None)
        self.assertEquals(car_list_ex.trains[0].cars[0].car_info.subtype, None)
        self.assertEquals(car_list_ex.trains[0].cars[0].car_info.up_place, None)
        self.assertEquals(car_list_ex.trains[0].cars[0].car_info.down_place, None)
        self.assertEquals(car_list_ex.trains[0].cars[0].car_info.down_side_place, None)
        self.assertEquals(car_list_ex.trains[0].cars[0].car_info.up_side_place, None)
        self.assertEquals(car_list_ex.trains[0].cars[0].car_info.down_near_wc_place, None)
        self.assertEquals(car_list_ex.trains[0].cars[0].car_info.up_near_wc_place, None)
        self.assertEquals(car_list_ex.trains[0].cars[0].car_info.down_side_near_wc_place, None)
        self.assertEquals(car_list_ex.trains[0].cars[0].car_info.up_side_near_wc_place, None)
        self.assertEquals(car_list_ex.trains[0].cars[0].is_discount, False)
        self.assertEquals(car_list_ex.trains[0].cars[0].is_reservation, False)
        self.assertEquals(car_list_ex.trains[0].cars[0].available_tariffs, [1, 9, 10])
        self.assertEquals(car_list_ex.trains[0].cars[0].is_loyalty_cards, None)
        self.assertEquals(car_list_ex.trains[0].cars[0].is_full_kupe, True)
        self.assertEquals(car_list_ex.trains[0].special_conditions, None)
        self.assertEquals(car_list_ex.trains[0].brand, None)
        self.assertEquals(car_list_ex.trains[0].is_suburban_train, False)
        self.assertEquals(car_list_ex.trains[0].departure_time.date, self.datetime)
        self.assertEquals(car_list_ex.trains[0].departure_time.time_offset, '+02:00')
        self.assertEquals(car_list_ex.trains[0].departure_time.time_type, 1)
        self.assertEquals(car_list_ex.trains[0].arrival_time.date, '03:00:00')
        self.assertEquals(car_list_ex.trains[0].arrival_time.time_offset, None)
        self.assertEquals(car_list_ex.trains[0].arrival_time.time_type, 0)
        self.assertEquals(car_list_ex.trains[0].passenger_railway_station.origin_code, 1000001)
        self.assertEquals(car_list_ex.trains[0].passenger_railway_station.destination_code, 2006004)
        self.assertEquals(car_list_ex.trains[0].passenger_departure_station.code, 1000001)
        self.assertEquals(car_list_ex.trains[0].passenger_departure_station.name, 'ХЕЛЬСИНКИ')
        self.assertEquals(car_list_ex.trains[0].passenger_arrival_station.code, 2006004)
        self.assertEquals(car_list_ex.trains[0].passenger_arrival_station.name, 'МОСКВА ОКТЯБРЬСКАЯ')

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
        self.assertEquals(update_order_info.order.order_item.id, 48715620)
        self.assertEquals(update_order_info.order.order_item.status, 0)

        self.assertEquals(update_order_info.order.order_item.blank[0].ticket_identifier, 5164702)
        self.assertEquals(update_order_info.order.order_item.blank[0].electronic_registration, ElectronicRegistration.CONFIRM)
        self.assertEquals(update_order_info.order.order_item.blank[0].print_flag, PrintFlag.NOT_PRINTED)
        self.assertEquals(update_order_info.order.order_item.blank[0].rzhd_status, RzhdStatus.ELECTRONIC_REGISTRATION)
        self.assertEquals(update_order_info.order.order_item.blank[0].food.code, 'Б')
        self.assertEquals(update_order_info.order.order_item.blank[0].food.name, 'ЗАВТРАК-БЛИНЫ/СЫР')
        self.assertEquals(update_order_info.order.order_item.blank[0].food.description, 'ЗАКУСКА СЫРНАЯ, БЛИНЫ, СУХАЯ ЧАСТЬ К РАЦИОНУ')

    def test_electronic_registration(self):
        electronic_registration = self.api.electronic_registration(48715620, Registration.CONFIRM)

        self.assertEquals(electronic_registration.status, 0)

        self.assertEquals(electronic_registration.blank[0].ticket_identifier, 5164702)
        self.assertEquals(electronic_registration.blank[0].electronic_registration, ElectronicRegistration.CONFIRM)

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
        refund_amount = self.api.refund_amount(48715620, 1, 0)

        self.assertEquals(refund_amount.status, 0)
        self.assertEquals(refund_amount.fee, 0.00)
        self.assertEquals(refund_amount.tax_percent, 0.00)
        self.assertEquals(refund_amount.amount, 8083.5)

        self.assertEquals(refund_amount.blanks[0].ticket_identifier, 5279650)
        self.assertEquals(refund_amount.blanks[0].tariff_nds, 0.0)
        self.assertEquals(refund_amount.blanks[0].service_nds, 0.0)
        self.assertEquals(refund_amount.blanks[0].commission_nds, 18.0)
        self.assertEquals(refund_amount.blanks[0].ads_nds, 18.0)
        self.assertEquals(refund_amount.blanks[0].returning_tariff_nds, 0.00)
        self.assertEquals(refund_amount.blanks[0].returning_service_nds, 0.00)
        self.assertEquals(refund_amount.blanks[0].returning_commission_nds, 0.00)
        self.assertEquals(refund_amount.blanks[0].returning_ads_nds, 28.28)
        self.assertEquals(refund_amount.blanks[0].returning_full_ticket_amount, None)
        self.assertEquals(refund_amount.blanks[0].returning_kupe_amount, None)
        self.assertEquals(refund_amount.blanks[0].returning_service_amount, None)
        self.assertEquals(refund_amount.blanks[0].fine_amount, None)
        self.assertEquals(refund_amount.blanks[0].amount, 6031.10)
