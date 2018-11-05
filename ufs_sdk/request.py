from datetime import datetime
from xml.etree.ElementTree import Element, SubElement
from .wrapper.types import (BonusCardType, DocType, AvailableTariffs, SegmentType,
                            PlaceDemands, RemoteCheckIn, FullKupe, InOneKupe, Storey,
                            PayType, Lang)

class XML:
    def __init__(self):
        super(XML, self).__init__()

    def sub_el(self, parent, name, text=None, attribs=None):
        sub = SubElement(parent, name, attribs if attribs is not None else {})
        if text is not None:
            sub.text = str(text)
        return sub

class BonusCard(XML):
    _type: BonusCardType
    number: str
    segments: list
    element_name: str

    def __init__(self, _type: BonusCardType, number: str, segments: list = None,
                element_name='BonusCard'):
        super(BonusCard, self).__init__()

        self._type = _type
        self.number = number
        self.segments = segments if segments is not None else [0]

        self.element_name = element_name

    def xml(self, parent) -> SubElement: 
        data = self.sub_el(parent, self.element_name)

        _type = self.sub_el(data, 'CardType', self._type)
        number = self.sub_el(data, 'Number', self.number)

        segments = []
        for item in self.segments:
            segments.append(self.sub_el(data, 'SegmentIndexes', item))

        #segments = self.sub_el(data, 'SegmentIndexes', ','.join([str(item) for item in self.segments]))

        return data


class TariffSegment(XML):
    index: int
    tariff_code: AvailableTariffs

    def __init__(self, index: int, tariff_code: AvailableTariffs):
        super(TariffSegment, self).__init__()

        self.index = index
        self.tariff_code = tariff_code

    def xml(self, parent) -> SubElement:
        data = self.sub_el(parent, 'TariffSegmentLinks')
        sub_data = self.sub_el(data, 'PassengerTariffXml')
        
        self.sub_el(sub_data, 'SegmentIndex', self.index)
        self.sub_el(sub_data, 'TariffCode', self.tariff_code)

        return data

class Passenger(XML):
    doc_type: DocType
    doc_number: str
    last: str
    first: str
    patronymic: str
    birthdate: datetime = datetime.utcnow()#None
    citizenship: str
    gender: str
    tariff_code: AvailableTariffs
    bonus_cards: [BonusCard]
    segments: [TariffSegment]
    back_bonus_cards: [BonusCard]
    cards: [BonusCard]

    def __init__(self, doc_type: DocType, doc_number: str, last: str, first: str, patronymic: str,
                birthdate: datetime, citizenship: str, gender: str, segments: [TariffSegment]=None, 
                tariff_code: AvailableTariffs = AvailableTariffs.FULL,
                bonus_cards: [BonusCard] = None, back_bonus_cards: [BonusCard] = None, 
                cards: [BonusCard] = None):
        super(Passenger, self).__init__()

        self.doc_type = doc_type
        self.doc_number = doc_number
        self.last = last
        self.first = first
        self.patronymic = patronymic
        self.birthdate = birthdate
        self.citizenship = citizenship
        self.gender = gender
        self.tariff_code = tariff_code
        self.segments = segments if segments is not None else []

        self.bonus_cards = bonus_cards if bonus_cards is not None else []
        self.back_bonus_cards = back_bonus_cards if back_bonus_cards is not None else []
        self.cards = cards if cards is not None else []

    def add_segment(self, segment: TariffSegment):
        self.segments.append(segment)

    def xml(self, parent) -> SubElement:
        data = self.sub_el(parent, 'PassengerXml')

        self.sub_el(data, 'DocumentType',  self.doc_type)
        self.sub_el(data, 'DocumentNumber', self.doc_number)

        self.sub_el(data, 'LastName', self.last)
        self.sub_el(data, 'FirstName', self.first)
        self.sub_el(data, 'MiddleName', self.patronymic)

        self.sub_el(data, 'DateOfBirth', self.birthdate.strftime('%d.%m.%Y') if self.birthdate is not None else None)

        self.sub_el(data, 'Citizenship', self.citizenship)

        self.sub_el(data, 'Gender', self.gender)

        #self.sub_el(data, 'TariffCode', self.tariff_code)

        for segment in self.segments:
            segment.xml(data)

        for item in self.bonus_cards:
            item.element_name = 'PassengerCard'
            item.xml(data)

        return data

class Segment(XML):
    origin: int
    destination: int
    departure: datetime
    train_number: str
    car_number: str
    car_type: str
    storey: Storey
    upper: int
    lower: int
    service_class: str
    segment_type: SegmentType = SegmentType.RAILWAY
    place_range: str
    gender: str = 'С'
    demands: PlaceDemands
    reqirements: InOneKupe 
    bedding: bool
    ereg: RemoteCheckIn = RemoteCheckIn.TRY_AUTO_ER
    international_service_class: str
    is_full_compartment: FullKupe
    stan: str
    comment: str

    def __init__(self, origin: int, destination: int, departure: datetime, train_number: str, 
                    car_type: str, service_class: str,  segment_type: SegmentType, ereg: RemoteCheckIn,  
                    car_number: str = None, storey: Storey = None, upper: int = None, lower: int = None, 
                    place_range: str = None, gender: str = None, demands: PlaceDemands = None, 
                    reqirements: InOneKupe = None, bedding: bool = None, 
                    international_service_class: str = None, is_full_compartment: FullKupe = None,
                    stan: str = None, comment: str = None):
        super(Segment, self).__init__()
        
        self.origin = origin
        self.destination = destination
        self.departure = departure
        self.train_number = train_number
        self.car_type = car_type
        self.service_class = service_class
        self.segment_type = segment_type
        self.ereg = ereg

        self.car_number = car_number
        self.storey = storey
        self.upper = upper
        self.lower = lower
        self.place_range = place_range
        self.gender = gender
        self.demands = demands
        self.reqirements = reqirements
        self.bedding = bedding
        self.international_service_class = international_service_class
        self.is_full_compartment = is_full_compartment

        self.stan = stan
        self.comment = comment

    def xml(self, parent) -> SubElement:
        data = self.sub_el(parent, 'BookSegmentXml')

        self.sub_el(data, 'FromStation', self.origin)
        self.sub_el(data, 'ToStation', self.destination)
        
        self.sub_el(data, 'DepartureDate', self.departure.strftime('%d.%m.%Y'))
        self.sub_el(data, 'DepartureTime', self.departure.strftime('%H:%M'))

        self.sub_el(data, 'TrainNumber', self.train_number)
        self.sub_el(data, 'CarNumber', self.car_number)
        self.sub_el(data, 'Type', self.car_type)
        self.sub_el(data, 'Storey', self.storey)
        self.sub_el(data, 'NumberOfUp', self.upper)
        self.sub_el(data, 'NumberOfDown', self.lower)
        self.sub_el(data, 'ServiceClass', self.service_class)
        self.sub_el(data, 'SegmentType', self.segment_type)
        self.sub_el(data, 'Diapason', self.place_range)
        self.sub_el(data, 'Gender', self.gender)
        self.sub_el(data, 'PlaceDemands', self.demands)
        self.sub_el(data, 'PlaceRequirements', self.reqirements)
        self.sub_el(data, 'WithOutBedding', int(self.bedding) if self.bedding is not None else None)
        self.sub_el(data, 'Stan', self.stan)
        self.sub_el(data, 'RemoteCheckIn', self.ereg)
        self.sub_el(data, 'InternationalServiceClass', self.international_service_class)
        self.sub_el(data, 'IsFullCompartment', self.is_full_compartment)
        self.sub_el(data, 'Comment', self.comment)

        return data


class Order(XML):
    segments: [Segment]
    passengers: [Passenger]
    formpay: PayType
    lang: str
    phone: str
    email: str

    def __init__(self, segments, passengers, formpay, lang: str=Lang.RU, 
                    phone: str = None, email: str = None):
        super(Order, self).__init__()

        self.segments = segments
        self.passengers = passengers
        self.formpay = formpay

        self.lang = lang
        self.phone = phone
        self.email = email

    @property
    def xml(self):
        data = Element('BookingXml')

        segments = self.sub_el(data, 'Segments')
        for segment in self.segments:
            segment.xml(segments)

        passengers = self.sub_el(data, 'Passengers')
        for passenger in self.passengers:
            passenger.xml(passengers)

        self.sub_el(data, 'PayType', self.formpay)
        self.sub_el(data, 'Language', self.lang)
        self.sub_el(data, 'Phone', self.phone)
        self.sub_el(data, 'Email', self.email)

        return data
