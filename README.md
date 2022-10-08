# DjangoAdminFilters library
[![GitHub Workflow Status](https://img.shields.io/github/workflow/status/vb64/django.admin.filters/pep257?label=Pep257&style=plastic)](https://github.com/vb64/django.admin.filters/actions?query=workflow%3Apep257)
[![GitHub Workflow Status](https://img.shields.io/github/workflow/status/vb64/django.admin.filters/django3?label=Django%203.2.14%20Python%203.7-3.10&style=plastic)](https://github.com/vb64/django.admin.filters/actions?query=workflow%3Adjango3)
[![GitHub Workflow Status](https://img.shields.io/github/workflow/status/vb64/django.admin.filters/django4?label=Django%204.1.1%20Python%203.8-3.10&style=plastic)](https://github.com/vb64/django.admin.filters/actions?query=workflow%3Adjango4)
[![Codacy Badge](https://app.codacy.com/project/badge/Coverage/926ec3c1141f4230b4d0508497e5561f)](https://www.codacy.com/gh/vb64/django.admin.filters/dashboard?utm_source=github.com&utm_medium=referral&utm_content=vb64/django.admin.filters&utm_campaign=Badge_Coverage)
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/926ec3c1141f4230b4d0508497e5561f)](https://www.codacy.com/gh/vb64/django.admin.filters/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=vb64/django.admin.filters&amp;utm_campaign=Badge_Grade)

The free, open-source DjangoAdminFilters library is designed to filter objects in the Django admin site.
The library provide few filters for this purpose.

-   `MultiChoice`: multi choice selection with checkboxes for CharField and IntegerField fields with 'choices' option
-   `MultiChoiceExt`: extended variant of previous filter, that allows filtering by custom defined properties
-   `DateRange`: set a custom date range using `input` fields
-   `DateRangePicker`: set a custom date range using javascript widget for select datetime from calendar

MultiChoice and MultiChoiceExt | DateRange | DateRangePicker
:------:|:-----:|:----:
![MultiChoice filter](img/multi_choice_en.png) | ![DateRange with input field](img/daterange_en.png) | ![DateRange with js widget](img/picker_en.png)

For javascript widget for DateRangePicker was used code from [date-and-time-picker project](https://github.com/polozin/date-and-time-picker) with merged [pull request](https://github.com/polozin/date-and-time-picker/pull/4/files), that allow to select dates before current.

## Installation

```bash
pip install django-admin-list-filters
```

To connect library to your project, add `django_admin_filters` to the `INSTALLED_APPS` list  in your `settings.py` file.

```python

INSTALLED_APPS = (

...

  'django_admin_filters',
)
```

After that, connect the static files of the library.

```bash
manage.py collectstatic
```

## Initial data

Let's say we have a table in the database. The records contain follows fields.

```python
# models.py
from django.db import models

STATUS_CHOICES = (
  ('P', 'Pending'),
  ('A', 'Approved'),
  ('R', 'Rejected'),
)

class Log(models.Model):
    text = models.CharField(max_length=100)
    timestamp1 = models.DateTimeField(default=None, null=True)
    timestamp2 = models.DateTimeField(default=None, null=True)
    status = models.CharField(max_length=1, default='P', choices=STATUS_CHOICES)
```

## Shared settings for all filters in the library

You can customize the appearance and behavior of filters to suit your needs by inheriting the filter classes from the library and overriding some of the attributes.
All library filters support the following attributes.

```python
from django_admin_filters import MultiChoice

class MyChoicesFilter(MultiChoice):
    FILTER_LABEL = "Select options"
    BUTTON_LABEL = "Apply"
    is_collapsed = False
```

-   FILTER_LABEL: Filter title
-   BUTTON_LABEL: Title for filter apply button
-   is_collapsed: Filter state (collapsed/expanded) on first page load

## MultiChoice filter

To use MultiChoice filter, you need to specify them in the `admin.py` file in the `list_filter` attribute of the corresponding class.

```python
# admin.py
from django.contrib import admin
from django_admin_filters import MultiChoice
from .models import Log

class StatusFilter(MultiChoice):
    FILTER_LABEL = "By status"

class Admin(admin.ModelAdmin):
    list_display = ['text', 'status']
    list_filter = [('status', StatusFilter)]

admin.site.register(Log, Admin)
```

## DateRange and DateRangePicker filters

To use filters with a date interval, you need to specify them in the `admin.py` file in the `list_filter` attribute of the corresponding class.

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

### Customization for DateRange filter

```python
# admin.py
from django_admin_filters import DateRange

class MyDateRange(DateRange):
    FILTER_LABEL = "Data range"
    BUTTON_LABEL = "Set range"
    FROM_LABEL = "From"
    TO_LABEL = "To"
    ALL_LABEL = 'All'
    CUSTOM_LABEL = "custom range"
    NULL_LABEL = "no date"
    DATE_FORMAT = "YYYY-MM-DD HH:mm"

    is_null_option = True

    options = (
      ('1da', "24 hours ahead", 60 * 60 * 24),
      ('1dp', "24 hours in the past", 60 * 60 * -24),
    )
```

You can override the following attributes.

-   `FROM_LABEL`: The label of the start date field.
-   `TO_LABEL`: The label of the end date field.
-   `ALL_LABEL`: The label of the menu item for displaying all records.
-   `CUSTOM_LABEL`: The label of the menu item when date range is set.
-   `NULL_LABEL`: The label of the menu item for displaying records without date.
-   `is_null_option`: Set this attribute to `False` to remove the option to display record without date from the filter menu.
-   `DATE_FORMAT`: Hint about the format of the date and time fields.

You can change the date/time input format to your own.
However, you may need to override the `to_dtime` method as well.
This method is used to convert a user-entered string into a `datetime` value.
By default, the method is defined as follows.

```python
@staticmethod
def to_dtime(text):
    try:
        return datetime.fromisoformat(text)
    except ValueError:
        return None
```

The `options` attribute specifies filter menu items that allow you to select data from the current moment to an offset of a specified number of seconds in the past or future.
Each element of the `options` list contains three values.

-   A unique string to use in the GET request parameters. Except for the strings 'custom' and 'empty' which are used by the filter.
-   The title of the item in the filter menu.
-   Offset in seconds relative to the current moment. A negative value specifies an offset to the past.

### Customization for DateRangePicker filter

The `DateRangePicker` filter with a javascript calendar date/time picker widget is derived from the `DateRange` filter and allows you to override all the attributes described above.
Also, additional attributes can be overridden in `DateRangePicker`.

```python
# admin.py
from django_admin_filters import DateRangePicker

class MyDateRangePicker(DateRangePicker):
    WIDGET_LOCALE = 'en'
    WIDGET_BUTTON_LABEL = "Set"
    WIDGET_WITH_TIME = True

    WIDGET_START_TITLE = 'Start date'
    WIDGET_START_TOP = -350
    WIDGET_START_LEFT = -400

    WIDGET_END_TITLE = 'End date'
    WIDGET_END_TOP = -350
    WIDGET_END_LEFT = -400
```

-   WIDGET_LOCALE: The language code for display the names of the months and days of the week. By default is the value of the `LANGUAGE_CODE` item in your project's `settings.py` file.
-   WIDGET_BUTTON_LABEL: The label of the select button.
-   WIDGET_WITH_TIME: Set this attribute to `False` if you only want to select a date without a time.
-   WIDGET_START_TITLE: The title of the widget when selecting the start date of the interval.
-   WIDGET_START_TOP: The vertical offset of the widget's calendar window when selecting the start date of the interval.
-   WIDGET_START_LEFT: The horizontal offset of the widget's calendar window when selecting the start date of the interval.
-   WIDGET_END_TITLE: The title of the widget when selecting the end date of the interval.
-   WIDGET_END_TOP: The vertical offset of the widget's calendar window when selecting the end date of the interval.
-   WIDGET_END_LEFT: The horizontal offset of the widget's calendar window when selecting the end date of the interval.

## Usage example

You can run an example of using the library on your local host.

On the Windows platform, you must first install the following programs.

-   [Python3](https://www.python.org/downloads/release/python-3712/)
-   GNU [Unix Utils](http://unxutils.sourceforge.net/) for operations via makefile
-   [Git for Windows](https://git-scm.com/download/win) to access the source code repository.

Then clone the repository and run the installation, specifying the path to Python 3.

```bash
git clone git@github.com:vb64/django.admin.filters.git
cd django.admin.filters
make setup PYTHON_BIN=/usr/bin/python3
```

Collect static files and create a database.

```bash
make static
make db
```

Create a database superuser by specifying a login and password for it.

```bash
make superuser
```

Run example.

```bash
make example
```

Open `http://127.0.0.1:8000/admin/` in a browser to view the example site.
To enter the admin panel you need to use the login and password that were set when creating the superuser.
