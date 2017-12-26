
class TimeSw:
    NO_SW = 0
    TRAIN_DISPATCH = 1
    TRAIN_ARRIVAL = 2


class DirectionGroup:
    INTERNAL = 0
    RUSSIAN_FINLAND = 1
    EAST_WEST = 2


class Lang:
    RU = 'Ru'
    EN = 'En'
    DE = 'De'


class TrainWithSeat:
    # Получение информации о поездах со свободными местами
    FREE_PLACE = 1
    # Получение информации обо всех поездах
    ALL = 0


class GrouppingType:
    # Группировка поездов по типу вагона
    TYPE = 0
    # Группировка поездов по типу вагона и по классу обслуживания
    TYPE_AND_SERVICE = 1
    # Группировка по типу вагона и по признакам QM/DM
    TYPE_AND_QM_DM = 2
    # Группировка по типу мест и цене
    PLACE_TYPE_AND_PRICE = 3
    # Группировка по номеру вагона и цене
    CAR_NUMBER_AND_PRICE = 4
    # Без группировки
    NONE = 5


class JoinTrains:
    # Получение списка поездов со склейкой
    WITH_BONDING = 0
    # Получение списка поездов без склеивания. Используется в случае, если в одном и том же поезде разные вагоны имеют разное время прибытия
    WITHOUT_BONDING = 1


class SearchOption:
    # Обычный поиск
    DEFAULT = 0
    # Включить в поиск маршруты в Крымский федеральный округ
    CRIMEA = 1
    # Включить в поиск мультимодальные перевозки
    MULTIMODAL = 2
    # Включить в поиск маршруты в Крымский федеральный округ и мультимодальные перевозки
    CRIMEA_AND_MULTIMODAL = 3
    # Включить в поиск маршруты с пересадкой
    TRANSFER = 4
    # Включить в поиск маршруты в Крымский федеральный округ и маршруты с пересадкой
    CRIMEA_AND_TRANSFER = 5
    # Включить в поиск мультимодальные перевозки и маршруты спересадкой
    MULTIMODAL_AND_TRANSFER = 6
    # Включить в поиск маршруты в Крымский федеральный округ, маршруты с пересадкой и мультимодалные перевозки
    ALL = 7


class AllowedDocType:
    PASSPORT = 'ПН'
    BIRTH_CERTIFICATE = 'СР'
    MILITARY_ID = 'ВБ'
    PASSPORT_SEAMAN = 'ПМ'
    RUSSIAN_FOREIGN_PASSPORT = 'ЗП'
    FOREIGN_PASSPORT = 'ЗЗ'


class Services:
    EAT = 'EAT'
    PAP = 'PAP'
    TV = 'TV'
    TRAN = 'TRAN'
    COND = 'COND'
    BED = 'BED'
    SAN = 'SAN'
    WIFI = 'WIFI'


class CarCategories:
    # Купейный вагон РИЦ (KV = КУПЕ)
    KUPE = 'РИЦ'
    # Мягкий вагон РИЦ (KV=МЯГК)
    SOFT = 'РИЦ'
    # Мягкий вагон Вагон Люкс (KV=МЯГК)
    SOFT_LUX = 'ЛЮКС'
    # Вагон класса люкс Вагон СВ (KV = ЛЮКС)
    LUX = 'СВ'
