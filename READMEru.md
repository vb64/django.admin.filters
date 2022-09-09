# Библиотека DjangoAdminDaterangeFilter

Бесплатная, с открытым исходным кодом библиотека DjangoAdminDaterangeFilter позволяет задавать пользовательский интервал дат для фильтров в таблицах админки Django.

  Фильтр с полем input     |  Фильтр с js виджетом
:-------------------------:|:-------------------------:
![фильтр с полем input](img/daterange_ru.png) | ![фильтр с js виджетом](img/picker_ru.png)

Для javascript виджета выбора даты/времени из календаря используется код [проекта date-and-time-picker](https://github.com/polozin/date-and-time-picker) с [внедренным кодом](https://github.com/polozin/date-and-time-picker/pull/4/files), позволяющем выбирать в этом виджете даты ранее текущей.


## Установка

```bash
pip install django-admin-filter-daterange
```

Для подключения DjangoAdminDaterangeFilter к вашему проекту в файле `settings.py` нужно добавить `'django_admin_filter_daterange'` в список `INSTALLED_APPS`.

```python

INSTALLED_APPS = (

...

  'django_admin_filter_daterange',
)
```

Если вы планируете использовать javascript виджет для выбора даты/времени из календаря, также необходимо подключить статические файлы библиотеки.

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
git clone git@github.com:vb64/django.admin.filter.daterange
cd django.admin.filter.daterange
make setup PYTHON_BIN=/usr/bin/python3
```

Собрать файлы медиа и создать базу данных.

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

Открыть в браузере адрес `http://127.0.0.1:8000/` для просмотра сайта примера.
Для входа в админку `http://127.0.0.1:8000/admin/` нужно использовать логин и пароль, заданные при создании суперюзера.
