from ufs_sdk.utils import get_array, get_item


class DateTime(object):
    def __init__(self, json):
        self.date = json.get('Date')
        self.time_offset = json.get('TimeOffset')
        self.time_type = get_item(json.get('TimeType'), int)


class StationTimeTable(object):
    def __init__(self, json):
        # Принадлежность дороге
        self.station_root = json.get('StationRoot')
        # Код станции
        self.station_code = json.get('StationCode')
        # Название станции отправления или станции прибытия пассажира
        self.station_name = json.get('StationName')[0]


class Clarify(object):
    def __init__(self, json):
        # Признак уточнения станции
        self.stations = get_array(json.get('Stations'), StationTimeTable)


class ReferenceParamsTimeTable(object):
    def __init__(self, json):
        # Код справки в системе АСУ «Экспресс-3»
        self.reference_code = get_item(json.get('ReferenceCode'), int)
        # Дата, по которой выдается справка
        self.reference_date = json.get('ReferenceDate')


class RouteParamsTimeTable(object):
    def __init__(self, json):
        # Станции отправления
        self.origin = json.get('StationName')[0]
        # Станции прибытия
        self.destination = json.get('StationName')[1]
        # Код станции отправления пассажира
        self.origin_code = get_item(json.get('OriginCode'), int)
        # Код станции прибытия пассажира
        self.destination_code = get_item(json.get('DestinationCode'), int)
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
        self.origin = json.get('StationName')[0]
        # Станции прибытия
        self.destination = json.get('StationName')[1]
        # Код станции отправления пассажира
        self.origin_code = get_item(json.get('OriginCode'), int)
        # Код станции прибытия пассажира
        self.destination_code = get_item(json.get('DestinationCode'), int)


class AdditionalInfoTimeTable(object):
    def __init__(self, json):
        # Дни следования поезда
        self.train_days_activity = json.get('TrainDaysActivity')


class DepthTrainSales(object):
    def __init__(self, json):
        # Дата, до которой возможна покупка билетов на текущий день
        self.date = json.get('Date')
        # Количество дней продажи билетов, не считая текущую дату
        self.days = get_item(json.get('Days'), int)


class TrainsTimeTable(object):
    def __init__(self, json):
        # Номер поезда
        self.number = json.get('Number')
        # Номер поезда, отображаемый пассажиру. Данный номер поезда печатается в контрольном купоне
        self.client_number = json.get('ClientNumber')
        # Маршрут поезда
        self.route = get_item(json.get('Route'), RouteTimeTable)
        # Время отправления со станции отправления пассажира
        self.passenger_departure_date = json.get('PassengerDepartureDate')
        # Время стоянки на станции отправления пассажира. Элемент не обязательный в случае, если станция отправления является начальной станцией
        self.origin_parking_time = json.get('OriginParkingTime')
        # Время в пути от станции отправления до станции прибытия пассажира
        self.travel_time = json.get('TravelTime')
        # Время прибытия на станцию прибытия пассажира
        self.passenger_arrival_time = json.get('PassengerArrivalTime')
        # Время стоянки на станции прибытия пассажира
        self.destination_parking_time = json.get('DestinationParkingTime')
        # Глубина продажи поезда
        self.depth_train_sales = get_item(json.get('DepthTrainSales'), DepthTrainSales)
        # Дополнительная информация о расписании
        self.additional_info = get_item(json.get('AdditionalInfo'), AdditionalInfoTimeTable)
        # Протяженность маршрута, км
        self.route_length = get_item(json.get('RouteLength'), int)
        # Наименование фирменного поезда
        self.train_name = json.get('TrainName')
        # Время и дата отправления поезда
        self.departure_time = get_item(json.get('DepartureTime'), DateTime)
        # Время и дата прибытия поезда
        self.arrival_time = get_item(json.get('ArrivalTime'), DateTime)


class TimeTable(object):
    def __init__(self, json):
        # Параметры справки
        self.reference_params = get_item(json.get('ReferenceParams'), ReferenceParamsTimeTable)
        # Параметры маршрута
        self.route_params = get_item(json.get('RouteParams'), RouteParamsTimeTable)
        # Информация о поезде
        self.trains = get_array(json.get('Trains'), TrainsTimeTable)

