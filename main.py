import requests


def print_json():

    # Делаем запрос
    r = requests.get('https://ruz.spbstu.ru/api/v1/ruz/teachers/2423/scheduler')
    data = r.json()
    # print(data)

    # Проверка четности недели
    if data['week']['is_odd']:
        print('Нечетная неделя')
    else:
        print('Четная неделя')

    weekdays = {1: 'Понедельник',
                2: 'Вторник',
                3: 'Среда',
                4: 'Четверг',
                5: 'Пятница',
                6: 'Суббота',
                7: 'Воскресенье'}

    # Вывод дня, даты, дисциплины, времени (от и до), преподователя и аудитории
    for day in data['days']:
        print('-' * (len(weekdays[day['weekday']]) + len(day['date'])))
        print(weekdays[day['weekday']], day['date'])
        for lesson in day['lessons']:
            print('-' * (len(weekdays[day['weekday']]) + len(day['date'])))
            print("Дисциплина: {0} ({1})"
                  .format(lesson['subject'], lesson['typeObj']['name']))
            print("Время: {0} - {1}".format(lesson['time_start'], lesson['time_end']))
            print("Преподаватель: {0}".format(lesson['teachers'][0]['full_name']))
            print("Аудитория: {0}".format(lesson['auditories'][0]['name']))


print_json()
