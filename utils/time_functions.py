from datetime import datetime, timedelta
from bs4 import ResultSet
import locale

locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')


def time_validation(time: str) -> str | bool:
    time_arr = time.split(':')
    if len(time_arr) == 2:
        hours, minutes = time_arr[0], time_arr[1]
        if hours.isdigit() and int(hours) < 24 and minutes.isdigit() and int(minutes) < 60:
            return hours.rjust(2, '0') + ':' + minutes.rjust(2, '0')
    else:
        return False


def find_rasp(day: str) -> (int, int):
    week_parity = datetime.today().isocalendar().week % 2 == 1
    today = datetime.today().weekday()
    if day == 'Завтра':
        rasp_weekday = (today + 1) % 7
        if rasp_weekday == 0:
            week_parity = not week_parity
    else:
        rasp_weekday = today
    return rasp_weekday, int(week_parity)


def find_date(day: str) -> str:
    if day.startswith('Неделя'):
        week_dates = []
        curr_week = find_rasp('Сегодня')[1]
        today = datetime.today()
        start_of_week = today - timedelta(days=today.weekday())
        if int(day[-1]) != curr_week:
            start_of_week += timedelta(days=7)
        for i in range(7):
            weekday_date = start_of_week + timedelta(days=i)
            weekday = datetime.strftime(weekday_date, '%A (%e %B)').capitalize().lstrip().replace('( ', '(')
            week_dates.append(weekday)
        return '\n'.join(week_dates)
    elif day == 'Завтра':
        rasp_day = datetime.today() + timedelta(days=1)
    else:
        rasp_day = datetime.today()

    date = datetime.strftime(rasp_day, '%A (%e %B)').capitalize().lstrip().replace('( ', '(')
    return date


def find_dates_other(lessons: ResultSet) -> (ResultSet, int):
    today = datetime.today()
    index = -1
    for i in range(len(lessons)):
        if 'valign' not in lessons[i].attrs:
            month, weekday = lessons[i].text.split(', ')
            lessons[i].string.replace_with(f'{weekday.capitalize()} ({month})')
            text = lessons[i].text.title()
            date = text[0].lower() + text[1:] + ' 2024'
            if len(lessons[i].text.split(' ')[1]) == 2:
                date = date.replace('(', '(0')
            date = datetime.strptime(date, '%A (%d %B) %Y')
            if today > date:
                index = i
                if date != today:
                    index += 1
    return lessons, index

#
# def find_date_other(dates: list) -> list:
#     for i in range(len(dates)):
#         month, weekday = dates[i].split(', ')
#         dates[i] = f'{weekday.capitlize()} ({month})'
#     return dates

