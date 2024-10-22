from datetime import datetime, timedelta
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
    if day == 'Завтра':
        rasp_day = datetime.now() + timedelta(days=1)
    else:
        rasp_day = datetime.now()
    # date = datetime.strftime(rasp_day, '%A (%e %B)').lower().lstrip()
    date = datetime.strftime(rasp_day, '%e %B').lower().lstrip()

    # if date[-2] in 'йь':
    #     date = date.replace(date[-2], 'я')
    # else:
    #     date[-1:] = 'а)'

    if date[-1] in 'йь':
        date = date.replace(date[-1], 'я')
    else:
        date[-1] = 'а'
    return date
