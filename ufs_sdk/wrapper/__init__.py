from ufs_sdk.utils import get_array, get_item


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


class RouteParamsTimeTable(object):
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
        self.allowed_doc_types = json.get('AllowedDocTypes')
        # Направление перевозки
        self.direction_group = int(json.get('DirectionGroup'))


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


class TrainsTimeTable(object):
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
        self.route_params = get_item(json.get('PP'), RouteParamsTimeTable)
        # Информация о поезде
        self.trains = get_array(json.get('N'), TrainsTimeTable)


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


class TrainsStationRoute(object):
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
        self.trains = get_array(json.get('N'), TrainsStationRoute)
