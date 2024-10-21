import requests
from bs4 import BeautifulSoup as bs
from bs4 import Tag

from utils.time_functions import find_rasp, find_date
from utils.db_functions import find_user


def edit_week_length(text: str) -> list:
    messages = []
    if len(text) > 4095:
        days = text.split('</blockquote>')
        length = 0
        ind = 0
        for i in range(len(days)):
            if length + len(days[i]) <= 4095:
                length += len(days[i])
                if i == len(days) - 1:
                    messages.append('</blockquote>'.join(days[ind:]) + '</blockquote>')
            else:
                messages.append('</blockquote>'.join(days[ind:i]) + '</blockquote>')
                length = 0
                ind = i
        messages[-1] = messages[-1][:-13]
        # print(messages)
        return messages
    return [text]


def group_validation(group_name: str) -> str:
    r = requests.get('https://bsu.ru/rasp/')
    groups = [el.text.lower() for el in bs(r.text, 'html.parser').find_all('span', class_='rasp_group rasp_link')]
    letters = {'а': 'a', 'б': 'b', 'с': 'c', 'д': 'd', 'е': 'e', 'ф': 'f', 'м': 'm', 'm': 'м'}
    if group_name in groups:
        return group_name
    else:
        for symbol in group_name:
            new_symbol = letters.get(symbol)
            if new_symbol:
                group_name = group_name.replace(symbol, new_symbol)
                break
        return group_name if group_name in groups else ''


def get_lessons(user: dict, old_week: Tag) -> str:
    detailed = user['settings'] == 'Подробное'
    lessons = old_week.find_all('tr')[1:]
    weekday, week = ['', ''], []
    sep = '\n\n'
    types = {
        'ЛК': '✍️',
        'ЛБ': '🧪',
        'ПР': '🛠',
        'ЭК': '☠️',
        'ЗЧ': '😰'
    }

    for el in lessons:
        lesson = {}
        subjects = el.find_all('td')
        for subj in subjects:
            if len(subjects) < 2:
                lesson = {'other': f'<b>{subj.text}</b>\n'}
                week.append(f'{weekday[0]}<blockquote>{sep.join(weekday[1:])}</blockquote>\n')
                weekday = []
                break
            elif 'class' in el.attrs and el['class'][0] == 'rasp_empty':
                lesson = {'other': f'{subj.text} | Окно'}
                break
            elif 'class' in subj.attrs:
                rasp_type = subj['class'][0].replace('rasp_', '')
                if rasp_type == 'subj_type':
                    lesson['subj_type'] = types.get(subj.text)
                else:
                    lesson[rasp_type] = subj.text
            else:
                lesson['teacher'] = subj.text

        if len(lesson) > 1:
            time = lesson['time'].rjust(5, '0')
            aud = lesson['aud'].ljust(4).replace(' ', '  ')
            subj = lesson['subj']
            lesson_str = f'{time} | {aud} | {subj}'
            if detailed:
                teacher, subj_type = lesson['teacher'], lesson['subj_type']
                lesson_str += f'\n{teacher} — {subj_type}'
            lesson = lesson_str
        else:
            lesson = lesson['other']
        weekday.append(lesson)

    week.append(f'{weekday[0]}<blockquote>{sep.join(weekday[1:])}</blockquote>\n')
    return '\n'.join(week[1:])


def get_day(user: dict, soup: bs, day: str) -> str:
    if user['department'] == 'Дневное отделение':
        rasp_weekday, week_parity = find_rasp(day)
        weeks_rasp = soup.find_all('table', class_='rasp_week')
        if len(weeks_rasp) > 0:
            clear_week = get_lessons(user, weeks_rasp[week_parity]).split('</blockquote>')
            if rasp_weekday < len(clear_week) - 1:
                return f'{clear_week[rasp_weekday]}</blockquote>'
        return 'К сожалению, на этот день нет расписания'
    else:
        other_rasp = soup.find_all('table', class_='rasp_drasp')
        if other_rasp:
            full_date, clear_week = find_date(day), get_lessons(user, other_rasp[0]).split('</blockquote>')
            for el in clear_week:
                if full_date in el:
                    return f'{clear_week[0]}</blockquote>'
        return 'К сожалению, на этот день нет расписания'


def get_week(soup: bs, user: dict, week_parity: int) -> str:
    if user["department"] == 'Дневное отделение':
        class_name = 'rasp_week'
    else:
        class_name = 'rasp_drasp'
        week_parity = 0
    rasp = soup.find_all('table', class_=class_name)
    if len(rasp) > 0:
        return get_lessons(user, rasp[week_parity])
    return 'К сожалению, на этот день нет расписания'


async def get_rasp(_id: int, rasp_type: str, week_parity: int | None) -> str:
    user = await find_user(_id)
    req = requests.get(user['rasp_link'])
    soup = bs(req.text, 'html.parser')
    if rasp_type == 'week':
        return get_week(soup, user, week_parity)
    else:
        return get_day(user, soup, rasp_type)


# print(parser(URL, 'Дневное отделен', 'tomorrow'))

# rasp = get_full_rasp({"rasp_link": "https://www.bsu.ru/rasp/?g=09A28", "department": "Дневное отделение",
#                      "settings": "detaile"}, 0)
#
# print(rasp)

# print(get_day({"rasp_link": "https://www.bsu.ru/rasp/?g=09A28", "department": "Дневное отделение",
#                      "settings": "defaul"}, 'today'))
