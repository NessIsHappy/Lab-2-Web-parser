import requests
import json
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
import argparse


def find_teacher(teacher_name: str) -> str:

    # Получаем HTML по запросу и находим в нем часть со скриптом
    url = requests.get('https://ruz.spbstu.ru/search/teacher?q=' + teacher_name)
    soup = BeautifulSoup(url.text, 'html.parser')
    data = soup.findAll('script')

    # Находим window.__INITIAL_STATE__
    string = data[3].text

    # Извлекаем оттуда строку, которая будет словарем с нужной информацией
    begin = string.find('faculties') - 2
    end = len(string) - 3
    string = string[begin:end]
    dictionary = json.loads(string)

    # Получаем id, нужен для работы get_timetable()
    elem = dictionary['searchTeacher']['data'][0]
    teacher_id = elem['id']
    return str(teacher_id)


def get_timetable(teacher_id: str) -> dict[str, int]:

    # Делаем запрос
    response = requests.get('https://ruz.spbstu.ru/api/v1/ruz/teachers/' + teacher_id + '/scheduler')
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

    teacher_id = find_teacher(args.name)
    dictionary_for_plot = get_timetable(teacher_id)
    get_plot(dictionary_for_plot)


if __name__ == '__main__':
    main()
