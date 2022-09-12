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
pip install django-admin-filters
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

## Пример использования

Вы можете запустить работающий на локальном компьютере пример использования библиотеки.

На платформе Windows для этого нужно предварительно установить следующие программы.

-   [Python3](https://www.python.org/downloads/release/python-3712/)
-   GNU [Unix Utils](http://unxutils.sourceforge.net/) для операций через makefile
-   [Git for Windows](https://git-scm.com/download/win) для доступа к репозитарию исходных кодов.

Затем склонировать репозитарий и запустить установку, указав путь на Python 3.

```bash
git clone git@github.com:vb64/django.admin.filters
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
