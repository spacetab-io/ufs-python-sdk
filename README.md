Ufs SDK [![CircleCI](https://circleci.com/gh/tmconsulting/ufs-python-sdk.svg?style=svg)](https://circleci.com/gh/tmconsulting/ufs-python-sdk)
----------------

Данное SDK позволяет получить доступ к методам Ufs и исправляет недостатки их системы.
* [Установка](#Установка)
* [Подключение](#Подключение)
* [Методы](#Методы)
* [Contact us](#contact-us)
* [License](#license)


## Установка
```
pip3 install ufs_sdk
```

## Подключение

Для подключения необходимо иметь логин, пароль и терминал.

```python
from ufs_sdk import API

api = API('username', 'password', 'terminal')

```

Далее для работы понадобятся enum структуры и обёртка для PassDoc(для метода BuyTickets)

```python
from ufs_sdk.wrapper.types import (...)
from ufs_sdk.wrapper import PassDoc
```

## Методы
### [TimeTable](https://github.com/tmconsulting/ufs-python-sdk/blob/develop/ufs_sdk/api.py#L19)
#### Запрос:
- **from** - Наименование или код станции отправления (7 символов)
- **to** - Наименование или код станции прибытия (7 символов)
- **day** - День отправления от 1 до 31
- **month** - Месяц отправления от 1 до 12
- **[time_sw](https://github.com/tmconsulting/ufs-python-sdk/blob/develop/ufs_sdk/wrapper/types.py#L2)** - Влияет на применение ограничивающих параметров Time_from и Time_to
- **time_from** - Левая граница временного диапазона (отправления или прибытия)
- **time_to** - Правая граница временного диапазона (отправления или прибытия)
- **suburban** - Признак получения расписания пригородных поездов

Пример запроса:
```python
time_table = api.time_table('МОСКВА', 'САНКТ-ПЕТЕРБУРГ', 24, 12, TimeSw.NO_SW)
```

#### Ответ:
- **is_clarify** - Признак уточнения станции. Если True, то переменная data - объект типа [Clarify](https://github.com/tmconsulting/ufs-python-sdk/blob/develop/ufs_sdk/wrapper/__init__.py#L21) иначе [TimeTable](https://github.com/tmconsulting/ufs-python-sdk/blob/develop/ufs_sdk/wrapper/__init__.py#L113)
- **train_point** - Признак начальной или конечной станции следования
- **data** - объект типа [Clarify](https://github.com/tmconsulting/ufs-python-sdk/blob/develop/ufs_sdk/wrapper/__init__.py#L21) или [TimeTable](https://github.com/tmconsulting/ufs-python-sdk/blob/develop/ufs_sdk/wrapper/__init__.py#L113)

### [StationRoute](https://github.com/tmconsulting/ufs-python-sdk/blob/develop/ufs_sdk/api.py#L26)
#### Запрос:
- **from** - Наименование или код станции отправления (7 символов)
- **day** - День отправления от 1 до 31
- **month** - Месяц отправления от 1 до 12
- **use_static_schedule** - Признак обращения в статическую базу полугодового расписания. Если тег принимает значение «0», то информация от АСУ «Экспресс-3».
- **suburban** - Признак получения расписания пригородных поездов

Пример запроса:
```python
station_route = api.station_route(4043, 5, 8, True, True)
 ```

#### Ответ:
- **[additional_info](https://github.com/tmconsulting/ufs-python-sdk/blob/develop/ufs_sdk/wrapper/__init__.py#L123)** - УФС слишком крутые, им не надо описание данного поля. Нам, видимо, тоже...
- **[route_params](https://github.com/tmconsulting/ufs-python-sdk/blob/develop/ufs_sdk/wrapper/__init__.py#L153)** - Параметры маршрута


### [TrainList](https://github.com/tmconsulting/ufs-python-sdk/blob/develop/ufs_sdk/api.py#L32)
#### Запрос:
- **from** - Наименование или код станции отправления (7 символов)
- **to** - Наименование или код станции прибытия (7 символов)
- **day** - День отправления от 1 до 31
- **month** - Месяц отправления от 1 до 12
- **advert_domain** - Доменное имя адверта
- **[time_sw](https://github.com/tmconsulting/ufs-python-sdk/blob/develop/ufs_sdk/wrapper/types.py#L2)** - Влияет на применение ограничивающих параметров Time_from и Time_to
- **[lang](https://github.com/tmconsulting/ufs-python-sdk/blob/develop/ufs_sdk/wrapper/types.py#L23)** - Язык
- **time_from** - Левая граница временного диапазона (отправления или прибытия)
- **time_to** - Правая граница временного диапазона (отправления или прибытия)
- **[train_with_seat](https://github.com/tmconsulting/ufs-python-sdk/blob/develop/ufs_sdk/wrapper/types.py#L29)** - Признак отображения поездов без свободных мест. Если параметр не передан или передано значение Train_with_seat=1, то в выдачи вернутся только поезда со свободными местами.
- **join_train_complex** - Признак отображения маршрутов с пересадками. Если параметр не передан или передано значение false, то в выдачи вернутся только поезда без пересадок
- **[grouping_type](https://github.com/tmconsulting/ufs-python-sdk/blob/develop/ufs_sdk/wrapper/types.py#L36)** - Признак группировки поездов. Если значение не передано, то группировка поездов осуществляется по типу вагона
- **[join_trains](https://github.com/tmconsulting/ufs-python-sdk/blob/develop/ufs_sdk/wrapper/types.py#L51)** - Признак склейки поездов. Если значение не передано, то в выдаче список поездов возвращается со склейкой
- **[search_option](https://github.com/tmconsulting/ufs-python-sdk/blob/develop/ufs_sdk/wrapper/types.py#L58)** - Вариант поиска

Пример запроса:
```python
train_list = api.train_list('МОСКВА', 'АГАПОВКА', 24, 12)
 ```


#### Ответ:
- **is_clarify** - Признак уточнения станции. Если True, то переменная data - объект типа [Clarify](https://github.com/tmconsulting/ufs-python-sdk/blob/develop/ufs_sdk/wrapper/__init__.py#L21) иначе [TrainList](https://github.com/tmconsulting/ufs-python-sdk/blob/develop/ufs_sdk/wrapper/__init__.py#L357) + balance и balance_limit
- **train_point** - Признак начальной или конечной станции следования
- **data** - объект типа [Clarify](https://github.com/tmconsulting/ufs-python-sdk/blob/develop/ufs_sdk/wrapper/__init__.py#L21) или [TrainList](https://github.com/tmconsulting/ufs-python-sdk/blob/develop/ufs_sdk/wrapper/__init__.py#L113)
- **balance** - Информация о балансе
- **balance_limit** - Актуальный кредит Агента в ЖД шлюзе.

### [CarListEx](https://github.com/tmconsulting/ufs-python-sdk/blob/develop/ufs_sdk/api.py#L43)
#### Запрос:
- **from** - Наименование или код станции отправления (7 символов)
- **to** - Наименование или код станции прибытия (7 символов)
- **day** - День отправления от 1 до 31
- **month** - Месяц отправления от 1 до 12
- **train** - Номер поезда
- **time** - Время отправления поезда
- **[lang](https://github.com/tmconsulting/ufs-python-sdk/blob/develop/ufs_sdk/wrapper/types.py#L23)** - Язык
- **type_car** - Тип вагона
- **advert_domain** - Доменное имя адверта
- **[grouping_type](https://github.com/tmconsulting/ufs-python-sdk/blob/develop/ufs_sdk/wrapper/types.py#L36)** - Признак группировки поездов. Если значение не передано, то группировка поездов осуществляется по типу вагона

Пример запроса:
```python
station_route = api.car_list_ex(4043, 5, 8, True, True)
 ```

#### Ответ:
- **[general_information](https://github.com/tmconsulting/ufs-python-sdk/blob/develop/ufs_sdk/wrapper/__init__.py#L193)** - Общая информация по запросу
- **[trains](https://github.com/tmconsulting/ufs-python-sdk/blob/develop/ufs_sdk/wrapper/__init__.py#L521)** - Информация о поезде

### [BuyTicket](https://github.com/tmconsulting/ufs-python-sdk/blob/develop/ufs_sdk/api.py#L51)
#### Запрос:
- **from** - Наименование или код станции отправления (7 символов)
- **to** - Наименование или код станции прибытия (7 символов)
- **day** - День отправления от 1 до 31
- **month** - Месяц отправления от 1 до 12
- **train** - Номер поезда (от 3 до 5 цифр и одна-две буквы)
- **type_car** - Тип вагона
- **[pass_doc](https://github.com/tmconsulting/ufs-python-sdk/blob/develop/ufs_sdk/wrapper/__init__.py#L687)** - Документ пассажира, по которому оформляется билет
- **[in_one_kupe](https://github.com/tmconsulting/ufs-python-sdk/blob/develop/ufs_sdk/wrapper/types.py#L266)** - Признак поиска мест только в одном купе. Значения «2» и «3» имеют смысл только в случае плацкартного вагона – в остальных случаях их указание некорректно.
- **[remote_check_in](https://github.com/tmconsulting/ufs-python-sdk/blob/develop/ufs_sdk/wrapper/types.py#L291)** - Признак установки электронной регистрации
- **[pay_type](https://github.com/tmconsulting/ufs-python-sdk/blob/develop/ufs_sdk/wrapper/types.py#L300)** - Тип оплаты электронного билета
- **n_car** - Номер вагона (две-три цифры) Обязателен в случае покупки билет в QM/DM вагоны
- **service_class** - Класс обслуживания вагона
- **sex** - Тип купе (мужское/женское/смешанное)
- **diapason** - Требуемый диапазон мест в вагоне
- **n_up** - Требуемое количество верхних мест
- **n_down** - Требуемое количество нижних мест
- **[bedding](https://github.com/tmconsulting/ufs-python-sdk/blob/develop/ufs_sdk/wrapper/types.py#L277)** - Признак того, включать ли в стоимость постельное белье (только для плацкартных вагонов), отказ от постельного белья доступен только для ограниченного количества направлений
- **stan** - Идентификатор заказа в веб-системе партнера. Бывает полезен для обеспечения взаимно-однозначного соответствия заказов во взаимодействующих системах
- **advert_domain** - Доменное имя адверта
- **phone** - Необходимо для выполнения клиентом последующих операций с заказом посредством SMS-сообщений.
- **[lang](https://github.com/tmconsulting/ufs-python-sdk/blob/develop/ufs_sdk/wrapper/types.py#L23)** - Язык
- **id_cust** - Id клиента
- **[storey](https://github.com/tmconsulting/ufs-python-sdk/blob/develop/ufs_sdk/wrapper/types.py#L307)**
- **time** - Время отправления поезда
- **comment** - Комментарии к заказу (длина не более 128 символов). Если передается больше 128 символов, то остальные символы отрезаются и не сохраняются. После символов «! # &» комментарий отрезается и не сохраняется.
- **[placedemands](https://github.com/tmconsulting/ufs-python-sdk/blob/develop/ufs_sdk/wrapper/types.py#L316)** - Требования к местам
- **international_service_class** - Информация о вагоне. Записывается в виде «X/Y», где X- класс обслуживания вагона, У – количество мест в купе Тег может быть заполнен для DirectionGroup = 1 и DirectionGroup =2 Тег является обязательным: 1) Если код тарифа Tariff (Таблица 94)для пассажира соответствует тарифам Senior или Junior 2) Для оформления пассажира в internationalServiceClass=1/1, если internationalServiceClass=1/1 не передан, то идет оформление билета по internationalServiceClass=1/2
- **[full_kupe](https://github.com/tmconsulting/ufs-python-sdk/blob/develop/ufs_sdk/wrapper/types.py#L284)** - Возможность выкупа купе целиком

Пример запроса:
```python
pass_doc = PassDoc('ЗП', 'ЗЗ934647165', '01051956', '1', 'KEN', first_name='Вася', last_name='Пупкин')
buy_tickets = api.buy_ticket(2000000, 1000001, 2, 3, '032A', 'М', pass_doc, InOneKupe.NOT_SIDE,
                             RemoteCheckIn.TRY_AUTO_ER, PayType.CASH)
 ```

#### Ответ:
- **[general_information](https://github.com/tmconsulting/ufs-python-sdk/blob/develop/ufs_sdk/wrapper/__init__.py#L193)** - Общая информация по запросу
- **[trains](https://github.com/tmconsulting/ufs-python-sdk/blob/develop/ufs_sdk/wrapper/__init__.py#L521)** - Информация о поезде

### [ConfirmTicket](https://github.com/tmconsulting/ufs-python-sdk/blob/develop/ufs_sdk/api.py#L69)
#### Запрос:
- **id_trans** - Номер транзакции в системе «УФС»
- **[confirm](https://github.com/tmconsulting/ufs-python-sdk/blob/develop/ufs_sdk/wrapper/types.py#L193)** - Признак подтверждения / отмены резервирования заказа
- **site_fee** - Комиссия с клиента за оформленный заказ
- **[lang](https://github.com/tmconsulting/ufs-python-sdk/blob/develop/ufs_sdk/wrapper/types.py#L23)** - Язык

Пример запроса:
```python
confirm_ticket = api.confirm_ticket(48715626, Confirm.CONFIRM, 0)
 ```

#### Ответ:
- **status** - Статус операции
- **transaction_id** - Номер транзакции в системе «УФС»
- **confirm_time_limit** - Дата и время, до которого можно подтвердить заказ.([DateTime](https://github.com/tmconsulting/ufs-python-sdk/blob/develop/ufs_sdk/wrapper/__init__.py#L4))
- **[electronic_registration](https://github.com/tmconsulting/ufs-python-sdk/blob/develop/ufs_sdk/wrapper/types.py#L202)** - Признак установки электронной регистрации
- **order_number** - Номер заказа в АСУ «Экспресс-3»
- **electronic_registration_expire** - Дата и время, до которого можно пройти электронную регистрацию и вернуть билет с ЭР в системе «УФС».([DateTime](https://github.com/tmconsulting/ufs-python-sdk/blob/develop/ufs_sdk/wrapper/__init__.py#L4))
- **[blank](https://github.com/tmconsulting/ufs-python-sdk/blob/develop/ufs_sdk/wrapper/__init__.py#L574)** - Информация о бланке заказа
- **[is_test](https://github.com/tmconsulting/ufs-python-sdk/blob/develop/ufs_sdk/wrapper/types.py#L223)** - Рекомендуется сверять значение этого признака со статусом терминала, использованного в запросе (значения не должны противоречить друг другу).
- **reservation** - Отложенная оплата.

### [UpdateOrderInfo](https://github.com/tmconsulting/ufs-python-sdk/blob/develop/ufs_sdk/api.py#L74)
#### Запрос:
- **id_trans** - Номер транзакции в системе «УФС»

Пример запроса:
```python
update_order_info = api.update_order_info(48715626)
```

#### Ответ:
- **status** - Текущий статус операции
- **[blank](https://github.com/tmconsulting/ufs-python-sdk/blob/develop/ufs_sdk/wrapper/__init__.py#L595)** - Информация о билете заказа
- **change_food_before** - Дата и время, до которого можно воспользоваться услугой смены РП([DateTime](https://github.com/tmconsulting/ufs-python-sdk/blob/develop/ufs_sdk/wrapper/__init__.py#L4))
- **order** - Информация о заказе

### [UpdateOrderInfo](https://github.com/tmconsulting/ufs-python-sdk/blob/develop/ufs_sdk/api.py#L74)
#### Запрос:
- **id_trans** - Номер транзакции в системе «УФС»

Пример запроса:
```python
update_order_info = api.update_order_info(48715626)
```

#### Ответ:
- **status** - Текущий статус операции
- **[blank](https://github.com/tmconsulting/ufs-python-sdk/blob/develop/ufs_sdk/wrapper/__init__.py#L595)** - Информация о билете заказа
- **change_food_before** - Дата и время, до которого можно воспользоваться услугой смены РП([DateTime](https://github.com/tmconsulting/ufs-python-sdk/blob/develop/ufs_sdk/wrapper/__init__.py#L4))
- **order** - Информация о заказе

### [ElectronicRegistration](https://github.com/tmconsulting/ufs-python-sdk/blob/develop/ufs_sdk/api.py#L78)
#### Запрос:
- **id_trans** - Номер транзакции в системе «УФС»
- **[reg](https://github.com/tmconsulting/ufs-python-sdk/blob/develop/ufs_sdk/wrapper/types.py#L256)** - Признак запрашиваемого действия:
- **id_blank** - Идентификаторы электронных билетов в системе «УФС», на которые необходимо установить/отменить электронную регистрацию (указываются через запятую)

Пример запроса:
```python
electronic_registration = api.electronic_registration(48715620, Registration.CONFIRM)
```

#### Ответ:
- **status** - Текущий статус операции
- **[blank](https://github.com/tmconsulting/ufs-python-sdk/blob/develop/ufs_sdk/wrapper/__init__.py#L636)** - Информация о билете заказа

### [GetTicketBlank](https://github.com/tmconsulting/ufs-python-sdk/blob/develop/ufs_sdk/api.py#L83)
#### Запрос:
- **id_trans** - Номер транзакции в системе «УФС»
- **[format](https://github.com/tmconsulting/ufs-python-sdk/blob/develop/ufs_sdk/wrapper/types.py#L348)** - Формат вывода

Пример запроса:
```python
get_ticket_blank = api.get_ticket_blank(1, TicketFormat.HTML)
```

#### Ответ:
У объект ответа есть поле content, которое хранит либо html код, либо pdf файл, а так же метод save_blank, который позволяет сохранить pdf/html файл по указанному пути

### [AvailableFood](https://github.com/tmconsulting/ufs-python-sdk/blob/develop/ufs_sdk/api.py#L88)
#### Запрос:
- **id_trans** - Номер транзакции в системе «УФС»
- **advert_domain** - Доменное имя адверта
- **[lang](https://github.com/tmconsulting/ufs-python-sdk/blob/develop/ufs_sdk/wrapper/types.py#L23)** - Язык

Пример запроса:
```python
available_food = api.available_food(48715620, '')
```

#### Ответ:
- **change_food_before** - Дата и время, до которого можно воспользоваться услугой смены РП.([DateTime](https://github.com/tmconsulting/ufs-python-sdk/blob/develop/ufs_sdk/wrapper/__init__.py#L4))
- **[food](https://github.com/tmconsulting/ufs-python-sdk/blob/develop/ufs_sdk/wrapper/__init__.py#L582)** - Список доступных РП

### [ChangeFood](https://github.com/tmconsulting/ufs-python-sdk/blob/develop/ufs_sdk/api.py#L93)
#### Запрос:
- **id_trans** - Номер транзакции в системе «УФС»
- **blanks_id** - Идентификатор бланка в системе «УФС»
- **food_allowance_code** - Код РП
- **advert_domain** - Доменное имя адверта
- **[lang](https://github.com/tmconsulting/ufs-python-sdk/blob/develop/ufs_sdk/wrapper/types.py#L23)** - Язык

Пример запроса:
```python
change_food = api.change_food(48715620, 1, '', '')
```

#### Ответ:
- **number** - Порядковый номер документа
- **train_number** - Номер поезда
- **departure_date** - Дата отправления поезда
- **departure_number** - од станции отправления
- **arrival_number** - Код станции прибытия
- **car_number** - Номер вагона
- **service_class** - Класс обслуживания
- **place_number** - Номера мест
- **passengers_amount** - Количество пассажиров
- **food_code** - Код РП
- **food_name** - Название РП
- **food_description** - Описание РП

### [RefundAmount](https://github.com/tmconsulting/ufs-python-sdk/blob/develop/ufs_sdk/api.py#L100)
#### Запрос:
- **id_trans** - Номер транзакции в системе «УФС»
- **id_blank** - Идентификаторы билетов в системе «УФС», для которых необходимо произвести возврат (указываются через запятую)
- **doc** - Номер документа, удостоверяющего личность
- **[lang](https://github.com/tmconsulting/ufs-python-sdk/blob/develop/ufs_sdk/wrapper/types.py#L23)** - Язык

Пример запроса:
```python
refund_amount = api.refund_amount(48715620, 1, 0)
```

#### Ответ:
- **status** - Статус операции
- **fee** - Сумма сервисного сбора за возврат
- **tax_percent** - Величина комиссионного сбора УФС в %, В случае, если комиссия является фиксированной величиной, то передается в данном параметре «0»
- **amount** - Общая сумма к возврату
- **[blanks](https://github.com/tmconsulting/ufs-python-sdk/blob/develop/ufs_sdk/wrapper/__init__.py#L644)** - Информация о билете заказа

### [Refund](https://github.com/tmconsulting/ufs-python-sdk/blob/develop/ufs_sdk/api.py#L105)
#### Запрос:
- **id_trans** - Номер транзакции в системе «УФС»
- **id_blank** - Идентификаторы билетов в системе «УФС», для которых необходимо произвести возврат (указываются через запятую)
- **doc** - Номер документа, удостоверяющего личность
- **stan** - Уникальный идентификатор операции (транзакции), необходимый, в частности, для получения информации о транзакции в случае потери ответа (таймаут, разрыв связи и т.п.)
- **[lang](https://github.com/tmconsulting/ufs-python-sdk/blob/develop/ufs_sdk/wrapper/types.py#L23)** - Язык

Пример запроса:
```python
refund = api.refund(48715620, 1, 0)
```

#### Ответ:
- **status** - Статус операции: «0» – успешная
- **refund_id** - Номер транзакции возврата
- **refund_date** - Время осуществления возврата
- **fee** - Сумма сервисного сбора за возврат
- **tax_percent** - Величина комиссионного сбора УФС в %, В случае, если комиссия является фиксированной величиной, то передается в данном параметре «0»
- **amount** - Общая сумма к возврату
- **[blanks](https://github.com/tmconsulting/ufs-python-sdk/blob/develop/ufs_sdk/wrapper/__init__.py#L644)** - Информация о билете заказа

### [GetCatalog](https://github.com/tmconsulting/ufs-python-sdk/blob/develop/ufs_sdk/api.py#L110)
#### Запрос:
- **[code](https://github.com/tmconsulting/ufs-python-sdk/blob/develop/ufs_sdk/wrapper/types.py#L261)** - Код справочника
- **[all_languages](https://github.com/tmconsulting/ufs-python-sdk/blob/develop/ufs_sdk/wrapper/types.py#L359)** - Признак ответа на всех языках.
- **[lang](https://github.com/tmconsulting/ufs-python-sdk/blob/develop/ufs_sdk/wrapper/types.py#L23)** - Язык
- **is_description** - Признак выдачи описания справочника

Пример запроса:
```python
get_catalog = api.get_catalog(ReferenceCode.LOYALTY_CARDS, 1)
```

#### Ответ:
- **[loyalty_cards](https://github.com/tmconsulting/ufs-python-sdk/blob/develop/ufs_sdk/wrapper/__init__.py#L676)** - Справочник Классов обслуживания
- **[co_services](https://github.com/tmconsulting/ufs-python-sdk/blob/develop/ufs_sdk/wrapper/__init__.py#L676)** - Справочник карт лояльности

### Contact us.

If you have any issues or questions regarding the API or the SDK it self, you are welcome to create an issue, or
You can write an Email to `artyom.slobodyan@gmail.com` or `roquie0@gmail.com`

### License.

SDK is released under the [MIT License](./LICENSE).
