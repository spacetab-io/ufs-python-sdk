from ufs_sdk.utils import get_array, get_item, get_bool_item, get_list_from_string


class DateTime(object):
    def __init__(self, json):
        self.date = json.get('Date')
        self.time_offset = json.get('TimeOffset')
        self.time_type = get_item(json.get('TimeType'), int)


class StationTimeTable(object):
    def __init__(self, json):
        # Принадлежность дороге
        self.station_root = json.get('PD')
        # Код станции
        self.station_code = json.get('CC')
        # Название станции отправления или станции прибытия пассажира
        self.station_name = json.get('C')[0]


class Clarify(object):
    def __init__(self, json):
        # Признак уточнения станции
        self.stations = get_array(json.get('SC'), StationTimeTable)


class ReferenceParamsTimeTable(object):
    def __init__(self, json):
        # Код справки в системе АСУ «Экспресс-3»
        self.reference_code = get_item(json.get('K'), int)
        # Дата, по которой выдается справка
        self.reference_date = json.get('D')


class RouteParams(object):
    def __init__(self, json):
        # Станции отправления
        self.origin = json.get('C')[0]
        # Станции прибытия
        self.destination = json.get('C')[1]
        # Код станции отправления пассажира
        self.origin_code = get_item(json.get('C1'), int)
        # Код станции прибытия пассажира
        self.destination_code = get_item(json.get('C2'), int)
        # Код станции отправления пассажира
        self.from_code = get_item(json.get('FromCode'), int)
        # Код станции прибытия пассажира
        self.to_code = get_item(json.get('ToCode'), int)
        # Допустимые типы документов
        self.allowed_doc_types = get_list_from_string(json.get('AllowedDocTypes'), str)
        # Направление перевозки
        self.direction_group = get_item(json.get('DirectionGroup'), int)


class RouteTimeTable(object):
    def __init__(self, json):
        # Станции отправления
        self.origin = json.get('C')[0]
        # Станции прибытия
        self.destination = json.get('C')[1]
        # Код станции отправления пассажира
        self.origin_code = get_item(json.get('C1'), int)
        # Код станции прибытия пассажира
        self.destination_code = get_item(json.get('C2'), int)


class AdditionalInfoTimeTable(object):
    def __init__(self, json):
        # Дни следования поезда
        self.train_days_activity = json.get('DW')


class DepthTrainSales(object):
    def __init__(self, json):
        # Дата, до которой возможна покупка билетов на текущий день
        self.date = json.get('Date')
        # Количество дней продажи билетов, не считая текущую дату
        self.days = get_item(json.get('Days'), int)


class TrainTimeTable(object):
    def __init__(self, json):
        # Номер поезда
        self.number = json.get('N1')
        # Номер поезда, отображаемый пассажиру. Данный номер поезда печатается в контрольном купоне
        self.client_number = json.get('N2')
        # Маршрут поезда
        self.route = get_item(json.get('NP'), RouteTimeTable)
        # Время отправления со станции отправления пассажира
        self.passenger_departure_date = json.get('T1')
        # Время стоянки на станции отправления пассажира. Элемент не обязательный в случае, если станция отправления является начальной станцией
        self.origin_parking_time = json.get('T2')
        # Время в пути от станции отправления до станции прибытия пассажира
        self.travel_time = json.get('T3')
        # Время прибытия на станцию прибытия пассажира
        self.passenger_arrival_time = json.get('T4')
        # Время стоянки на станции прибытия пассажира
        self.destination_parking_time = json.get('T5')
        # Глубина продажи поезда
        self.depth_train_sales = get_item(json.get('DepthTrainSales'), DepthTrainSales)
        # Дополнительная информация о расписании
        self.additional_info = get_item(json.get('J'), AdditionalInfoTimeTable)
        # Протяженность маршрута, км
        self.route_length = get_item(json.get('L'), int)
        # Наименование фирменного поезда
        self.train_name = json.get('NN')
        # Время и дата отправления поезда
        self.departure_time = get_item(json.get('DepartureTime'), DateTime)
        # Время и дата прибытия поезда
        self.arrival_time = get_item(json.get('ArrivalTime'), DateTime)


class TimeTable(object):
    def __init__(self, json):
        # Параметры справки
        self.reference_params = get_item(json.get('Z2'), ReferenceParamsTimeTable)
        # Параметры маршрута
        self.route_params = get_item(json.get('PP'), RouteParams)
        # Информация о поезде
        self.trains = get_array(json.get('N'), TrainTimeTable)


class AdditionalInfoStationRoute(object):
    def __init__(self, json):
        # Описание содержимого справки
        self.reference_content = json.get('S1')
        # Наименование или код станции отправления пассажира
        self.station_name = json.get('C')[0]
        # Дата отправления пассажира
        self.passenger_departure_time = json.get('D1')
        # Дата формирования справки
        self.documents_formation_time = json.get('D2')


class TrainStationRoute(object):
    def __init__(self, json):
        # Номер поезда
        self.number = json.get('N1')
        # Номер поезда, отображаемый пассажиру. Данный номер поезда печатается в контрольном купоне
        self.client_number = json.get('N2')
        # Маршрут поезда
        self.route = get_item(json.get('NP'), RouteTimeTable)
        # Время отправления со станции отправления пассажира
        self.passenger_departure_date = json.get('T1')
        # Время в пути от станции отправления до станции прибытия пассажира
        self.travel_time = json.get('T3')
        # Время прибытия на станцию прибытия пассажира
        self.passenger_arrival_time = json.get('T4')
        # Дни следования поезда
        self.train_days_activity = json.get('DW')


class RouteParamsStationRoute(object):
    def __init__(self, json):
        # Информация о поезде
        self.trains = get_array(json.get('N'), TrainStationRoute)


class Station(object):
    def __init__(self, xml):
        # Код станции пересадки
        self.code = xml.find('./Code').text
        # Название станции пересадки
        self.name = xml.find('./Name').text
        # Количество вариантов пересадок на этой станции
        self.option_count = xml.find('./OptionCount').text
        # Минимальное время в пути, задаваемое в формате «Д:ЧЧ:ММ:СС»
        self.min_trip_time = xml.find('./MinTripTime').text
        # Максимальное время в пути, задаваемое в формате «Д:ЧЧ:ММ:СС»
        self.max_trip_time = xml.find('./MaxTripTime').text
        # Минимальное время стыковки, задаваемое в формате «Д:ЧЧ:ММ:СС»
        self.min_arrival_wait_time = xml.find('./MinArrivalWaitTime').text
        # Максимальное время стыковки, задаваемое в формате «Д:ЧЧ:ММ:СС»
        self.max_arrival_wait_time = xml.find('./MaxArrivalWaitTime').text
        # Признак мультивокзальной станции
        self.is_multi_station = xml.find('./IsMultiStation').text


class AdditionalInfoTrainList(object):
    def __init__(self, xml):
        # Признак, который разрешает в метод TrainListTransfer отправлять все станции пересадки
        self.is_allowed_multi_station_search = xml.find('./IsAllowedMultiStationSearch')
        if self.is_allowed_multi_station_search is not None:
            self.is_allowed_multi_station_search = self.is_allowed_multi_station_search.text
        else:
            self.is_allowed_multi_station_search = False
        # Информация о станциях пересадки
        self.stations = get_array(xml.findall('./Stations/Station'), Station)

        self.xml = xml


class GeneralInformation(object):
    def __init__(self, json):
        # Код справки в системе «Экспресс-3»
        self.reference_code = get_item(json.get('K'), int)
        # Тип справки
        self.reference_type = json.get('TS')
        # Параметры маршрута пассажира
        self.route_params = get_item(json.get('PP'), RouteParams)
        # Шифры ВЦ, в которых найдены места"""
        self.cipher = json.get('WM')


class CarInfoTrainList(object):
    def __init__(self, json):
        # Количество свободных мест без определения верхних и нижних
        self.free_places = get_item(json.get('M4'), int)
        # Количество нижних купейных мест
        self.kupe_down_free_places = get_item(json.get('M5'), int)
        # Количество верхних купейных мест
        self.kupe_up_free_places = get_item(json.get('M6'), int)
        # Количество нижних боковых мест
        self.kupe_down_side_free_places = get_item(json.get('M7'), int)
        # Количество верхних боковых мест
        self.kupe_up_side_free_places = get_item(json.get('M8'), int)
        # Мужские места
        self.man_places = get_item(json.get('X1'), int)
        # Женские места
        self.women_places = get_item(json.get('X2'), int)
        # Целые купе
        self.whole_kupe = get_item(json.get('X3'), int)
        # Смешанные купе
        self.mixed_kupe = get_item(json.get('X4'), int)
        # Категория вагона
        self.car_category = json.get('KV')
        # Количество целых купе
        self.count_whole_kupe = get_item(json.get('KU'), int)


class Fee(object):
    def __init__(self, json):
        self.min = get_item(json.get('min'), int)
        self.max = get_item(json.get('max'), int)


class CarTrainList(object):
    def __init__(self, json):
        # Категория вагона
        self.category = json.get('KV')
        # Категория вагона для отображения пассажиру
        self.car_category = json.get('KV1')
        # Класс обслуживания вагона
        self.service_class = json.get('CO')
        # Список услуг
        self.services = get_list_from_string(json.get('CO_SRV'), str)
        # Государство/дорога принадлежности вагона
        self.country_way = json.get('W2')
        # Владелец вагона
        self.car_owner = json.get('VB')
        # Признак категории вагона
        self.car_category_belonging = json.get('R')
        # Стоимость билета. Разделитель точка. Один знак после разделителя
        self.ticket_price = get_item(json.get('TF'), float)
        # Минимальная стоимость сервиса. Разделитель точка. Один знак после разделителя
        self.min_ticket_price = get_item(json.get('TF1'), float)
        # Стоимость максимальная. Разделитель точка. Один знак после разделителя
        self.max_service_price = get_item(json.get('TF2'), float)
        # Стоимость сервиса. Разделитель точка. Один знак после разделителя
        self.service_price = get_item(json.get('TF3'), float)
        # Признак стоимости за два места
        self.is_two_place = get_bool_item(json.get('DM'))
        # Признак стоимости за 4 места
        self.is_four_place = get_bool_item(json.get('QM'))
        # Информация о вагоне (Таблица 53)
        self.car_info = get_item(json.get('CV'), CarInfoTrainList)
        # Признак участия поезда в программе «Динамическое ценообразование»
        self.is_dynamic_price = get_bool_item(json.get('UD'))
        # Признак того, что на данную категорию вагонов снижена стоимость билетов
        self.is_discount = get_bool_item(json.get('Discount'))
        # Возможность трехчасового бронирования
        self.reservation = json.get('Reservation')
        # Вознаграждение агента
        self.client_fee = get_item(json.get('ClientFee'), Fee)


class PassengerRailwayStation(object):
    def __init__(self, json):
        # Код станции отправления пассажира
        self.origin_code = get_item(json.get('C1'), int)
        # Код станции прибытия пассажира
        self.destination_code = get_item(json.get('C2'), int)


class PassengerStation(object):
    def __init__(self, json):
        # Код станции пересадки
        self.code = get_item(json.get('Code'), int)
        # Название станции пересадки
        self.name = json.get('Name')


class SpecialConditions(object):
    def __init__(self, json):
        self.comment = json.get('G1')


class TrainTrainList(object):
    def __init__(self, json):
        # Числовая часть номера поезда
        self.number_part = get_item(json.get('trainNum'), int)
        # Признак логического поезда. True показывает, что в этом поезде могут быть вагоны, которые следуют
        # с одним номером поезда, а другие с другим.
        self.is_logical_train = get_bool_item(json.get('isLogicalTrain'))
        # Номер поезда
        self.number = json.get('N1')
        # Номер поезда, отображаемый пассажиру. Данный номер поезда печатается в контрольном купоне
        self.client_number = json.get('N2')
        # Категория поезда
        self.category = [item for item in json.get('KN')]
        # Наименование фирменного поезда
        self.train_name = json.get('NN')
        # Маршрут поезда
        self.route = get_item(json.get('NP'), RouteTimeTable)
        # Дата отправления пассажира в формате «ДД.ММ»
        self.passenger_departure_time = json.get('D')
        # Дата прибытия поезда в формате «ДД.ММ»
        self.passenger_arrival_time = json.get('D1')
        # Время отправления со станции отправления пассажира
        self.passenger_departure_date = json.get('T1')
        # Время стоянки на станции отправления пассажира. Элемент не обязательный в случае, если станция отправления является начальной станцией
        self.origin_parking_time = json.get('T2')
        # Время в пути от станции отправления до станции прибытия пассажира
        self.travel_time = json.get('T3')
        # Время прибытия на станцию прибытия пассажира
        self.passenger_arrival_date = json.get('T4')
        # Время стоянки на станции прибытия пассажира
        self.destination_parking_time = json.get('T5')
        # Признак того, что на поезд возможна электронная регистрация. Если в ответе тег ER отображается, то на поезд возможна ЭР
        self.is_electronic_registration = get_bool_item(json.get('ER'))
        # Дата отправления поезда с начальной станции в формате «ДД.ММ»
        self.origin_departure_time = json.get('DZ')
        # Протяженность маршрута, км
        self.route_length = get_item(json.get('LL'), int)
        # Информация о вагонах определенной категории
        self.cars = get_array(json.get('CK'), CarTrainList)
        # Уведомление пассажира об особых условиях поездки
        self.special_conditions = get_item(json.get('GA'), SpecialConditions)
        # Бренд поезда
        self.brand = json.get('BRN')
        # Признак пригородного поезда
        self.is_suburban_train = get_bool_item(json.get('IsSuburbanTrain'))
        # Признак пересечения границы Если в ответе тег CrossBorder отображается, то на поезд пересекает границу РФ
        self.cross_border = json.get('CrossBorder')
        # Время и дата отправления поезда
        self.departure_time = get_item(json.get('DepartureTime'), DateTime)
        # Время и дата прибытия поезда
        self.arrival_time = get_item(json.get('ArrivalTime'), DateTime)
        # Информация о вокзале отправления и прибытия пассажира
        self.passenger_railway_station = get_item(json.get('VOK'), PassengerRailwayStation)
        # Информация о вокзале отправления пассажира
        self.passenger_departure_station = get_item(json.get('PassengerDepartureStation'), PassengerStation)
        # Информация о вокзале прибытия пассажира
        self.passenger_arrival_station = get_item(json.get('PassengerArrivalStation'), PassengerStation)


class TrainList(object):
    def __init__(self, json):
        # Общая информация по запросу
        self.general_information = get_item(json.get('Z3'), GeneralInformation)
        # Информация о поезде
        self.trains = get_array(json.get('N'), TrainTrainList)
        # Признак неполной (урезанной по времени) справки. Его наличие означает, что показаны не все поезда.
        # Чтобы просмотреть все, необходимо указать более узкий диапазон времени отправления или прибытия
        self.is_full_reference = get_bool_item(json.get('U', False))


class RouteCarListEx(object):
    def __init__(self, json):
        # Станции отправления
        self.origin = json.get('C')[0]
        # Станции прибытия
        self.destination = json.get('C')[1]


class PlacesCarListEx(object):
    def __init__(self, json):
        self.amount = json.get('Amount')
        self.places = json.get('Places')


class CarInfoCarListEx(object):
    def __init__(self, json):
        # Признак того, что на поезд возможна электронная регистрация.
        # Если в ответе тег ER отображается, то на поезд возможна ЭР
        self.is_electronic_registration = get_bool_item(json.get('ER'))
        # Номер вагона
        self.car_num = get_item(json.get('VH'), int)
        # Количество свободных мест без определения верхних и нижних
        self.free_places = get_item(json.get('M4'), int)
        # Количество нижних купейных мест
        self.kupe_down_free_places = get_item(json.get('M5'), int)
        # Количество верхних купейных мест
        self.kupe_up_free_places = get_item(json.get('M6'), int)
        # Количество нижних боковых мест
        self.kupe_down_side_free_places = get_item(json.get('M7'), int)
        # Количество верхних боковых мест
        self.kupe_up_side_free_places = get_item(json.get('M8'), int)
        # Мужские места
        self.man_places = get_item(json.get('X1'), int)
        # Женские места
        self.women_places = get_item(json.get('X2'), int)
        # Целые купе
        self.whole_kupe = get_item(json.get('X3'), int)
        # Смешанные купе
        self.mixed_kupe = get_item(json.get('X4'), int)
        # Количество целых купе
        self.count_whole_kupe = get_item(json.get('KU'), int)
        # Выбор постельного белья Если данный тег вернулся, то есть возможность выбрать/отказаться от белья.
        # Если данного тега нет, то нет возможности выбора бель
        self.linens = get_item(json.get('BL'), int)
        # Номера свободных мест (через запятую). К номеру места может быть добавлен символ для гендерных вагонов
        self.free_places_list = get_list_from_string(json.get('H'), str)
        # Категория вагона
        self.car_category = json.get('KV')
        # Признак двухэтажного вагона
        self.is_two_storey = get_bool_item(json.get('TwoStorey'))
        # Описание типа маршрута Может принимать значение БП - беспересадочный вагон. Данный вагон может выйти в составе одного поезда, а приехать в пункт назначения в составе другого поезда
        self.route_type = json.get('AA')
        # Номера свободных мест у стола.
        self.table_free_places = json.get('MP')
        # Номера свободных мест рядом с детской площадкой
        self.playground_free_places = json.get('MV')
        # Номера свободных мест у стола рядом с детской площадкой
        self.table_playground_free_places = json.get('MB')
        # Номера свободных мест рядом с местами для пассажиров с животными.
        self.animals_free_places = json.get('MD')
        # Номера свободных обычных мест (не у стола)
        self.default_free_places = json.get('MN')
        # Признак выбора РП.
        self.is_rp_selected = get_bool_item(json.get('PIT'))
        # Дата прибытия вагона в формате «ДД.ММ». Тег является обязательным для беспересадочного вагона
        self.car_arrival_time = json.get('D1')
        # Время прибытия вагона на станцию прибытия пассажира Тег является обязательным для беспересадочного вагона
        self.car_passenger_arrival_time = json.get('T4')
        # Номера мест в отсеке
        self.place_numbers = json.get('MCP')
        # Номера откидных мест
        self.folding_place_numbers = json.get('MFP')
        # Номера мест для пассажиров с животными.
        self.animals_place_numbers = json.get('MPP')
        # Номера мест для матери и ребенка
        self.mother_place_numbers = json.get('MMB')
        # Номера мест для пассажиров с детьми
        self.children_place_numbers = json.get('MPC')
        # Признак плавающего поезда (переправа по средствам парома)
        self.is_floating = get_bool_item(json.get('PLP'))
        # Код типа мест
        self.place_type_number = json.get('HK')
        # Подтип вагона
        self.subtype = json.get('PT')
        # Верхние купейные места
        self.up_place = get_item(json.get('UpPlace'), PlacesCarListEx)
        # Нижние купейные места
        self.down_place = get_item(json.get('DownPlace'), PlacesCarListEx)
        # Нижние боковые места
        self.down_side_place = get_item(json.get('DownSidePlace'), PlacesCarListEx)
        # Верхние боковые места
        self.up_side_place = get_item(json.get('UpSidePlace'), PlacesCarListEx)
        # Нижние купейние места у туалета (места 33, 35)
        self.down_near_wc_place = get_item(json.get('DownNearWcPlace'), PlacesCarListEx)
        # Верхние купейние места у туалета (места 34, 36)
        self.up_near_wc_place = get_item(json.get('UpNearWcPlace'), PlacesCarListEx)
        # Нижнее боковое место у туалета (место 37)
        self.down_side_near_wc_place = get_item(json.get('DownSideNearWcPlace'), PlacesCarListEx)
        # Верхнее боковое место у туалета (место 38)
        self.up_side_near_wc_place = get_item(json.get('UpSideNearWcPlace'), PlacesCarListEx)
        # Схема вагона
        self.schema = json.get('SCHEMA')


class CarCarListEx(object):
    def __init__(self, json):
        # Категория вагона
        self.category = json.get('KV')
        # Категория вагона для отображения пассажиру
        self.car_category = json.get('KV1')
        # Информация о вагоне. Записывается в виде «X/Y», где X- класс обслуживания вагона, У – количество мест в купе
        # Является обязательным для международного направления DirectionGroup = 1 и DirectionGroup =2
        self.car_gen_info = json.get('MKL')
        # Класс обслуживания вагона
        self.service_class = json.get('CO')
        # Список услуг
        self.services = get_list_from_string(json.get('CO_SRV'), str)
        # Список услуг
        self.services_info = get_list_from_string(json.get('CO_DESC'), str)
        # Государство/дорога принадлежности вагона
        self.country_way = json.get('W2')
        # Владелец вагона
        self.car_owner = json.get('VB')
        # Признак категории вагона
        self.car_category_belonging = json.get('R')
        # Стоимость билета. Разделитель точка. Один знак после разделителя
        self.ticket_price = get_item(json.get('TF'), float)
        # Минимальная стоимость сервиса. Разделитель точка. Один знак после разделителя
        self.min_ticket_price = get_item(json.get('TF1'), float)
        # Стоимость максимальная. Разделитель точка. Один знак после разделителя
        self.max_service_price = get_item(json.get('TF2'), float)
        # Стоимость сервиса. Разделитель точка. Один знак после разделителя
        self.service_price = get_item(json.get('TF3'), float)
        # Признак участия поезда в программе «Динамическое ценообразование»
        self.is_dynamic_price = get_bool_item(json.get('UD'))
        # Признак стоимости за два места
        self.is_two_place = get_bool_item(json.get('DM'))
        # Признак стоимости за 4 места
        self.is_four_place = get_bool_item(json.get('QM'))
        # Информация о вагоне (Таблица 53)
        self.car_info = get_item(json.get('CV'), CarInfoCarListEx)
        # Признак того, что на данную категорию вагонов снижена стоимость билетов
        self.is_discount = get_bool_item(json.get('Discount'))
        # Возможность трехчасового бронирования
        self.is_reservation = get_bool_item(json.get('Reservation'))
        # Список действующих тарифов для данного вагона.
        # Тег обязателен для DirectionGroup=0,2
        self.available_tariffs = get_list_from_string(json.get('AvailableTariffs'), int)
        # Возможность применения карт лояльности при оформлении билетов в данный вагон.
        self.is_loyalty_cards = json.get('LoyaltyCards')
        # Признак «выкуп купе целиком».
        # Если в ответе тег FullKupe отображается, то в данном вагоне возможен выкуп всего купе целиком.
        self.is_full_kupe = get_bool_item(json.get('FullKupe'))


class TrainCarListEx(object):
    def __init__(self, json):
        # Номер поезда
        self.number = json.get('N1')
        # Номер поезда, отображаемый пассажиру. Данный номер поезда печатается в контрольном купоне
        self.client_number = json.get('N2')
        # Категория поезда
        self.category = json.get('KN')
        # Наименование фирменного поезда
        self.train_name = json.get('NN')
        # Маршрут поезда
        self.route = get_item(json.get('NP'), RouteCarListEx)
        # Дата отправления пассажира в формате «ДД.ММ»
        self.passenger_departure_time = json.get('D')
        # Дата прибытия поезда в формате «ДД.ММ»
        self.passenger_arrival_time = json.get('D1')
        # Время отправления со станции отправления пассажира
        self.passenger_departure_date = json.get('T1')
        # Время стоянки на станции отправления пассажира. Элемент не обязательный в случае,
        # если станция отправления является начальной станцией
        self.origin_parking_time = json.get('T2')
        # Время в пути от станции отправления до станции прибытия пассажира
        self.travel_time = json.get('T3')
        # Время прибытия на станцию прибытия пассажира
        self.passenger_arrival_date = json.get('T4')
        # Время стоянки на станции прибытия пассажира
        self.destination_parking_time = json.get('T5')
        # Признак того, что на поезд возможна электронная регистрация. Если в ответе тег ER отображается, то на поезд возможна ЭР
        self.is_electronic_registration = get_bool_item(json.get('ER'))
        # Дата отправления поезда с начальной станции в формате «ДД.ММ»
        self.origin_departure_time = json.get('DZ')
        # Протяженность маршрута, км
        self.route_length = get_item(json.get('LL'), int)
        # Информация о вагонах определенной категории
        self.cars = get_array(json.get('CK'), CarCarListEx)
        # Уведомление пассажира об особых условиях поездки
        self.special_conditions = get_item(json.get('GA'), SpecialConditions)
        # Бренд поезда
        self.brand = json.get('BRN')
        # Признак пригородного поезда
        self.is_suburban_train = get_bool_item(json.get('IsSuburbanTrain'))
        # Время и дата отправления поезда
        self.departure_time = get_item(json.get('DepartureTime'), DateTime)
        # Время и дата прибытия поезда
        self.arrival_time = get_item(json.get('ArrivalTime'), DateTime)
        # Информация о вокзале отправления и прибытия пассажира
        self.passenger_railway_station = get_item(json.get('VOK'), PassengerRailwayStation)
        # Информация о вокзале отправления пассажира
        self.passenger_departure_station = get_item(json.get('PassengerDepartureStation'), PassengerStation)
        # Информация о вокзале прибытия пассажира
        self.passenger_arrival_station = get_item(json.get('PassengerArrivalStation'), PassengerStation)


class Blank(object):
    def __init__(self, json):
        # Идентификатор билета в заказе в шлюзе
        self.ticket_identifier = get_item(json.get('ID'), int)
        # Номер билета в заказе в АСУ «Экспресс-3»
        self.ticket_number = get_item(json.get('TicketNum'), int)


class Food(object):
    def __init__(self, json):
        # Код РП.
        self.code = json.get('data')
        # Название РП
        self.name = json.get('Name')
        # Описание РП
        if 'Description' in json.keys():
            self.description = json.get('Description')
        else:
            self.description = json.get('Desc')


class BlankUpdateOrderInfo(object):
    def __init__(self, json):
        # Идентификатор билета в заказе в шлюзе
        self.ticket_identifier = get_item(json.get('ID'), int)
        # Признак наличия электронной регистрации
        self.electronic_registration = get_item(json.get('RemoteCheckIn'), int)
        # Признак того, что оригинал билета распечатан
        self.print_flag = get_item(json.get('PrintFlag'), int)
        # Статус билета в АСУ «Экспресс-3»
        self.rzhd_status = get_item(json.get('RzhdStatus'), int)
        # 
        self.food = get_item(json.get('Food'), Food)


class OrderItem(object):
    def __init__(self, json):
        # Идентификатор заказа
        self.id = get_item(json.get('Id'), int)
        # Текущий статус операции: «0» - успешная операция «1»- неуспешная операция
        self.status = get_item(json.get('Status'), int)
        # воспользоваться  услугой смены РП. Атрибут «timeOffset="+ЧЧ:ММ"» содержит информацию
        # о часовом поясе для данного элемента, где "+ЧЧ:ММ" разница в часах и минутах от
        # UTC(Всемирное координированное время) конкретного места
        self.change_food_before = get_item(json.get('ChangeFoodBefore'), DateTime)
        # Информация о билете заказа
        self.blank = get_array(json.get('Blank'), BlankUpdateOrderInfo)


class Order(object):
    def __init__(self, json):
        # Номер заказа в системе «УФС»
        self.id = get_item(json.get('Id'), int)
        # Идентификатор родительской транзакции
        self.root_id = get_item(json.get('RootTransId'), int)
        #
        if json.get('OrderItems') is not None:
            self.order_item = get_item(json['OrderItems'].get('OrderItem'), OrderItem)
        else:
            self.order_item = None


class BlankElectronicRegistration(object):
    def __init__(self, json):
        # Идентификатор билета в заказе в шлюзе
        self.ticket_identifier = get_item(json.get('ID'), int)
        # Признак наличия электронной регистрации
        self.electronic_registration = get_item(json.get('RemoteCheckIn'), int)


class BlankRefund(object):
    def __init__(self, json):
        # Атрибут ID N Да Идентификатор билета в системе «УФС»
        self.ticket_identifier = get_item(json.get('ID'), int)
        # Ставка НДС с тарифа (в процентах)
        self.tariff_nds = get_item(json.get('STV1'), float)
        # Ставка НДС с сервиса (в процентах)
        self.service_nds = get_item(json.get('STV2'), float)
        # Ставка НДС с комиссионного сбора (в процентах)
        self.commission_nds = get_item(json.get('STV3'), float)
        # Ставка НДС с рекламационногосбора (сбор за возврат) (в процентах)
        self.ads_nds = get_item(json.get('STV4'), float)
        # Сумма возвращаемого НДС со стоимости перевозки по ставке STV1
        self.returning_tariff_nds = get_item(json.get('ETF4'), float)
        # Сумма возвращаемого НДС со стоимости сервисных услуг по ставке STV2
        self.returning_service_nds = get_item(json.get('ETF5'), float)
        # Сумма возвращаемого НДС со стоимости комиссионного сбора по ставке STV3
        self.returning_commission_nds = get_item(json.get('ETFC'), float)
        # Сумма взимаемого НДС со стоимости комиссионного сбора за возврат по ставке STV4
        self.returning_ads_nds = get_item(json.get('ETFB'), float)
        # Сумма возвращаемой стоимости билетной части
        self.returning_full_ticket_amount = get_item(json.get('ESB'), float)
        # Сумма возвращаемой стоимости плацкарты
        self.returning_kupe_amount = get_item(json.get('ESP'), float)
        # Сумма возвращаемой стоимости сервисных услуг
        self.returning_service_amount = get_item(json.get('ESS'), float)
        # Сумма штрафа за возврат
        self.fine_amount = get_item(json.get('ESKV'), float)
        # Сумма к возврату по данному билету
        self.amount = get_item(json.get('Amount'), float)


class Cards(object):
    def __init__(self, json):
        self.code = json.get('Code')
        self.name_ru = json.get('NameRU')
        self.name_en = json.get('NameEN')
        self.name_de = json.get('NameDE')
        self.description_ru = json.get('DescriptionRU')
        self.description_en = json.get('DescriptionEN')
        self.description_de = json.get('DescriptionDE')


class PassDoc(object):
    def __init__(self, doc_type: str, doc_number, birth_data: str, tariff_code: str, country_iso: str='-',
                 sex: str='-', last_name: str='-', first_name: str='-', patronymic: str='-', card_number: int='-'):

        self.pass_doc = '%s%s/%s=%s=%s/%s*%s/%s/%s/%s' % (doc_type, doc_number, last_name, first_name, patronymic, birth_data,
                                                          tariff_code, country_iso, sex, card_number)


class PassengerInfo(object):
    def __init__(self, json):
        # Тип и номер документа
        self.doc = json.get('PS')
        # Фамилия, имя, отчество
        self.fio = json.get('IZ')
        # Уникальный идентификатор пассажира
        self.identifier = get_item(json.get('ID'), int)
        # Пол пассажира
        self.sex = json.get('FM')
        # Гражданство пассажира
        self.citizenship = json.get('GR')
        # Дата рождения в формате ddMMyyyy
        self.birth_date = json.get('GD')


class TicketInfo(object):
    def __init__(self, json):
        # Да Порядковый номер билета в заказе
        self.ticket_number = get_item(json.get('PR'), int)
        # Да Стоимость билета с учетом НДС
        self.ticket_price = get_item(json.get('TF'), float)
        # НДС со стоимости перевозки по электронному билету
        self.tariff_nds = get_item(json.get('TF4'), float)
        # НДС со стоимости сервиса по электронному билету
        self.service_nds = get_item(json.get('TF5'), float)
        # Стоимость билетной части по ЭБ
        self.ticket_eb_price = get_item(json.get('STB'), float)
        # Стоимость плацкарты по ЭБ
        self.ticket_platzkart_price = get_item(json.get('STP'), float)
        # НДС со стоимости комиссионного сбора и дополнительнвх услуг
        self.ads_nds = get_item(json.get('TFB'), float)
        # Ставка НДС с тарифа (в процентах)
        self.percent_tariff_nds = get_item(json.get('STV1'), float)
        # Ставка НДС с сервиса (в процентах)
        self.percent_service_nds = get_item(json.get('STV2'), float)
        # Ставка НДС с комиссионного сбора (в процентах)
        self.commission_nds = get_item(json.get('STV3'), float)
        # Информация о льготе или спецтарифе
        self.privilege_info = get_item(json.get('DL'), int)
        # Категория билета (Таблица 98)
        self.ticket_category = json.get('GT')
        # Ярус места Значение отсутствует для безденежных билетов.
        # Атрибут description содержит описание занимаемого места
        self.place_tier = None if json.get('CM') is None else json['CM'].get('data')
        self.place_tier_description = None if json.get('CM') is None else json['CM'].get('description')
        # Информация о пассажире (Таблица 103)
        self.passenger_info = get_item(json.get('PI'), PassengerInfo)
        # Да Список мест. Записывается в виде:
        #   1) «ааа» - номер занимаемого места,
        #   2) «aaa, bbb, ccc» – перечисление занимаемых мест,
        #   3) «aaa-ccc» - диапазон занимаемых мест, где aaa, bbb, ccc – занимаемые места (произвольное строковое значение)
        self.place_list = json.get('H')
        # Storey EN Нет Требование к этажности вагона (Таблица 104)
        self.storey = get_item(json.get('Storey'), int)
        # IDBlank N Да Идентификатор бланка в системе «УФС»
        self.blank_id = get_item(json.get('IDBlank'), int)
        # PlaceCount N Да Количество мест, отведенных пассажиру
        self.place_count = get_item(json.get('PlaceCount'), int)
        # PIT B Нет Признак выбора РП
        self.is_rp_selected = json.get('PIT')


class ExternalData(object):
    def __init__(self, json):
        # Уникальный ключ, по которому выбирается значение из словаря
        self.key = json.get('key')
        # Значение уникального ключа
        self.value = get_item(json.get('value'), int)


class Warnings(object):
    def __init__(self, json):
        # code N Да Код предупреждения
        self.code = get_item(json.get('code'), int)
        # text C Да Описание предупреждения
        self.text = json.get('text')
        # ExternalData S Да (Таблица 100)
        self.external_data = get_item(None if json.get('ExternalData') is None else json['ExternalData'].get('Data'), ExternalData)


class PrintPoints(object):
    def __init__(self, json):
        # Название станции
        self.station = json.get('Station')
        # Время в пути от ближайшей точки распечатки ЭБ до станции отправления
        self.run_time = json.get('RunTime')
        # Направление движения до ближайшей точки распечатки ЭБ:
        # Opposite – точка распечатки находится до станции отправления,
        # Forward – точка распечатки находится впереди по маршруту.
        self.direction = json.get('Direction')
