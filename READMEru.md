# Библиотека DjangoAdminFilters

Бесплатная, с открытым исходным кодом библиотека DjangoAdminFilters позволяет использовать несколько дополнительных фильтров в таблицах админки Django.

-   `DateRange`: позволяет задавать пользовательский интервал дат с использованием полей `input`
-   `DateRangePicker`: позволяет задавать пользовательский интервал дат с использованием javascript виджета выбора даты/времени из календаря

  Фильтр DateRange     |  Фильтр DateRangePicker
:-------------------------:|:-------------------------:
![фильтр с полем input](img/daterange_ru.png) | ![фильтр с js виджетом](img/picker_ru.png)

Для javascript виджета используется код [проекта date-and-time-picker](https://github.com/polozin/date-and-time-picker) с внедренным [кодом](https://github.com/polozin/date-and-time-picker/pull/4/files), позволяющем выбирать в этом виджете даты ранее текущей.

## Установка

```bash
pip install django-admin-list-filters
```

Для подключения библиотеки к проекту нужно добавить `django_admin_filters` в список `INSTALLED_APPS` в файле `settings.py`.

```python

INSTALLED_APPS = (

...

  'django_admin_filters',
)
```

После этого подключить статические файлы библиотеки.

```bash
manage.py collectstatic
```

## Использование

Допустим, у нас в БД имеется таблица, записи которой содержат поля типа `datetime`.

```python
# models.py
from django.db import models

class Log(models.Model):
    text = models.CharField(max_length=100)
    timestamp1 = models.DateTimeField(default=None, null=True)
    timestamp2 = models.DateTimeField(default=None, null=True)
```

Для использования фильтров с интервалом дат нужно в файле `admin.py` указать их в атрибуте `list_filter` соответствующего класса.

```python
# admin.py
from django.contrib import admin
from django_admin_filters import DateRange, DateRangePicker
from .models import Log

class Admin(admin.ModelAdmin):
    list_display = ['text', 'timestamp1', 'timestamp2']
    list_filter = (('timestamp1', DateRange), ('timestamp2', DateRangePicker))

admin.site.register(Log, Admin)
```

## Настройка

Вы можете настроить внешний вид и поведение фильтров под свои требования путем наследования классов фильтров из библиотеки и переопределения некоторых атрибутов.

```python
# admin.py
from django_admin_filters import DateRange

class MyDateRange(DateRange):
    FILTER_LABEL = "Интервал данных"
    FROM_LABEL = "От"
    TO_LABEL = "До"
    ALL_LABEL = 'Все'
    CUSTOM_LABEL = "пользовательский"
    NULL_LABEL = "без даты"
    BUTTON_LABEL = "Задать интервал"
    DATE_FORMAT = "YYYY-MM-DD HH:mm"

    is_null_option = True

    options = (
      ('1da', "24 часа вперед", 60 * 60 * 24),
      ('1dp', "последние 24 часа", 60 * 60 * -24),
    )
```

Можно переопределять следующие атрибуты.

-   `FILTER_LABEL`: Заголовок фильтра.
-   `FROM_LABEL`: Текст у поля начальной даты.
-   `TO_LABEL`: Текст у поля конечной даты.
-   `ALL_LABEL`: Текст пункта меню фильтра для отображения всех записей.
-   `CUSTOM_LABEL`: Текст пункта меню фильтра при использовании интервала дат.
-   `BUTTON_LABEL`: Текст кнопки установки интервала дат.
-   `NULL_LABEL`: Текст пункта меню фильтра для отображения записей без даты.
-   `is_null_option`: Установите этот атрибут в `False`, чтобы убрать из меню фильтра пункт отображения записей без даты.
-   `DATE_FORMAT`: Текст подсказки о формате полей даты и времени.

Вы можете изменить формат ввода даты/времени на собственный.
Но при этом вам возможно будет необходимо также переопределить метод `to_dtime`.
Этот метод используется для преобразования введенной пользователем строки в значение `datetime`.
По умолчанию метод определен следующим образом.

```python
@staticmethod
def to_dtime(text):
    try:
        return datetime.fromisoformat(text)
    except ValueError:
        return None
```

Атрибут `options` задает пункты меню фильтра, позволяющие выбирать данные от текущего момента до смещения на заданное количество секунд в прошлом либо будущем.
Каждый элемент списка `options` содержит три значения.

-   Уникальная строка для использования в параметрах GET запроса. Кроме строк 'custom' и 'empty', которые используются фильтром.
-   Заголовок пункта в меню фильтра.
-   Смещение в секундах относительно текущего момента. Отрицательное значение задает смещение в прошлое.

Фильтр `DateRangePicker` с javascript виджетом выбора даты/времени из календаря является производным от фильтра `DateRange` и позволяет переопределять все описанные выше атрибуты.
Кроме того, в `DateRangePicker` можно переопределить дополнительные атрибуты.

```python
class MyDateRangePicker(DateRangePicker):
    WIDGET_LOCALE = 'ru'
    WIDGET_BUTTON_LABEL = "Выбрать"
    WIDGET_WITH_TIME = True

    WIDGET_START_TITLE = 'Начальная дата'
    WIDGET_START_TOP = -350
    WIDGET_START_LEFT = -400

    WIDGET_END_TITLE = 'Конечная дата'
    WIDGET_END_TOP = -350
    WIDGET_END_LEFT = -400
```

-   WIDGET_LOCALE: Код языка, на котором виджет будет отображать названия месяцев и дней недели. По умолчанию используется значение параметра `LANGUAGE_CODE` файла `settings.py` вашего проекта.
-   WIDGET_BUTTON_LABEL: Текст кнопки выбора виджета.
-   WIDGET_WITH_TIME: Установите значение этого атрибута в `False`, если вам требуется только выбор даты без времени.
-   WIDGET_START_TITLE: Заголовок виджета при выборе начальной даты интервала.
-   WIDGET_START_TOP: Смещение по вертикали окна календаря виджета при выборе начальной даты интервала.
-   WIDGET_START_LEFT: Смещение по горизонтали окна календаря виджета при выборе начальной даты интервала.
-   WIDGET_END_TITLE: Заголовок виджета при выборе конечной даты интервала.
-   WIDGET_END_TOP: Смещение по вертикали окна календаря виджета при выборе конечной даты интервала.
-   WIDGET_END_LEFT: Смещение по горизонтали окна календаря виджета при выборе конечной даты интервала.

## Пример использования

Вы можете запустить работающий на локальном компьютере пример использования библиотеки.

На платформе Windows для этого нужно предварительно установить следующие программы.

-   [Python3](https://www.python.org/downloads/release/python-3712/)
-   GNU [Unix Utils](http://unxutils.sourceforge.net/) для операций через makefile
-   [Git for Windows](https://git-scm.com/download/win) для доступа к репозитарию исходных кодов.

Затем склонировать репозитарий и запустить установку, указав путь на Python 3.

```bash
git clone git@github.com:vb64/django.admin.filters.git
cd django.admin.filters
make setup PYTHON_BIN=/usr/bin/python3
```

Подключить статические файлы библиотеки и создать базу данных.

```bash
make static
make db
```

Создать суперюзера базы данных, указав для него логин и пароль.

```bash
make superuser
```

Запустить пример.

```bash
make example
```

Открыть в браузере адрес `http://127.0.0.1:8000/admin/` для просмотра сайта примера.
Для входа в админку нужно использовать логин и пароль, заданные при создании суперюзера.
