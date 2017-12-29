
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


class LoyaltyCards:
    # Начисление баллов "РЖД Бонус"
    RZHD_BONUS_SCORING = 'RzhdB'
    # Дорожная карта
    RZHD_MAP = 'RzhdU'
    # Скидка по карте "РЖД Бонус"
    RZHD_BONUS_DISCOUNT = 'RzhdSU'


class CarCategories:
    # Купейный вагон РИЦ (KV = КУПЕ)
    KUPE = 'РИЦ'
    # Мягкий вагон РИЦ (KV=МЯГК)
    SOFT = 'РИЦ'
    # Мягкий вагон Вагон Люкс (KV=МЯГК)
    SOFT_LUX = 'ЛЮКС'
    # Вагон класса люкс Вагон СВ (KV = ЛЮКС)
    LUX = 'СВ'


class AvailableTariffs:
    # Полный
    FULL = 1
    # Детский (до 10 лет)
    CHILD_TO_10 = 2
    # Детский без места (до 5 лет)
    CHILD_WITHOUT_PLACE_TO_5 = 3
    # SENIOR (60+) в Сапсан
    SENIOR_SAPSAN = 4
    # SENIOR (от 60 лет) ГЕНИАЛЬНО
    SENIOR = 5
    # JUNIOR (от 12 до 26 лет)
    JUNIOR = 6
    # Детский (до 12 лет)
    CHILD_TO_12 = 7
    # Детский без места (до 4 лет)
    CHILD_WITHOUT_PLACE_TO_4 = 8
    # Детский (до 17 лет)
    CHILD_TO_17 = 9
    # Детский без места (до 6 лет)
    CHILD_WITHOUT_PLACE_TO_6 = 10
    # Детский (до 7 лет)
    CHILD_TO_7 = 11
    # Детский без места(до 10 лет)
    CHILD_WITHOUT_PLACE_TO_10 = 12
    # Детский (от 10 до 17 лет)
    CHILD_FROM_10_TO_17 = 13
    # Школьник (для учащихся от 10 лет)
    SCHOOLBOY_FROM_10 = 14
    # Детский без места (для детей до 12 лет)
    CHILD_WITHOUT_PLACE_TO_12 = 15
    # Детский без места (для детей до 6 лет) ЧТО ? В ЧЁМ ТУТ РАЗНИЦА С ПУНКТОМ ВЫШЕ ? УФСМАТЬВАШУ
    CHILD_2_WITHOUT_PLACE_TO_6 = 16
    # Молодежный ЮНИОР (для лиц от 10 до 21 года)
    JUNIOR_FROM_10_TO_21 = 17
    # Праздничный
    FESTIVE = 18
    # Свадебный
    WEDDING = 19
    # Семейный
    FAMILY = 20


class PlaceTypeNumber:
    # Нижний ярус
    TOP = 'Н'
    # Верхний ярус
    BOTTOM = 'В'
    # Средний ярус
    MIDDLE = 'С'
    # (для сидячих вагонов) Для пассажира с животным
    ANIMALS = 'Ж'
    # (для сидячих вагонов) Для матери и ребенка
    MOTHER_CHILD = 'М'
    # (для сидячих вагонов) Для пассажира с детьми
    CHILDREN = 'Р'
    # (для сидячих вагонов) Для инвалидов
    INVALID = 'И'
    # (для сидячих вагонов) Переговорная
    MEETING_ROOM = 'Г'
    # (для сидячих вагонов) Не у стола
    NOT_TABLE = 'Н'
    # (для сидячих вагонов) У стола
    TABLE = 'П'
    # (для сидячих вагонов) У детской площадки
    PLAYGROUND = 'В'
    # (для сидячих вагонов) У стола рядом с детской площадкой
    TABLE_PLAYGROUND = 'Б'
    # (для сидячих вагонов) Рядом с местами для пассажиров с животными
    BESIDE_ANIMALS = 'Д'
    # (для сидячих) Откидное
    FOLDING = 'О'
    # (для сидячих вагонов) Отсек (купе) в поезде Ласточка
    SITTING_KUPE = 7
