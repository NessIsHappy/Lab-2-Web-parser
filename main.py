import requests
import json
import matplotlib.pyplot as plt
import argparse


def find_teacher(teacher_name: str) -> None:

    # Пока ничего не делает
    url = 'https://ruz.spbstu.ru/search/teacher?q=' + teacher_name
    payload = {'first_name': teacher_name}
    r = requests.post(url, data=json.dumps(payload))
    print(r.headers)


def get_timetable() -> dict[str, int]:

    # Делаем запрос
    response = requests.get('https://ruz.spbstu.ru/api/v1/ruz/teachers/2423/scheduler')
    data = response.json()
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

    lessons_cnt = {'Понедельник': 0,
                   'Вторник': 0,
                   'Среда': 0,
                   'Четверг': 0,
                   'Пятница': 0,
                   'Суббота': 0,
                   'Воскресенье': 0}
    i = 0
    cnt = 0

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
            cnt += 1
        lessons_cnt[weekdays[day['weekday']]] = cnt
        cnt = 0
        i += 1
    return lessons_cnt


def get_plot(dictionary) -> None:

    # График: количество занятий/день недели
    weekdays = ['Пон', 'Втор', 'Ср', 'Чет', 'Пят', 'Суб', 'Воскр']
    x = weekdays
    y = []
    for day in dictionary:
        y.append(dictionary[day])
    plt.bar(x, y, label='Расписание')
    plt.xlabel('Дни недели')
    plt.ylabel('Количество занятий')
    plt.title('')
    plt.legend()
    plt.show()


def main():

    parser = argparse.ArgumentParser(description='Вывод расписания преподавателя')
    parser.add_argument('name', type=str, help='Имя преподавателя')
    args = parser.parse_args()

    dictionary_for_plot = get_timetable()
    get_plot(dictionary_for_plot)


if __name__ == '__main__':
    main()
